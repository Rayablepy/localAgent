import { SqlDatabase } from "@langchain/classic/sql_db";
import { DataSource } from "typeorm";
import { dbpath } from "../database/databasehandler.js";
import { tool } from "langchain";
import { SystemMessage } from "langchain"
import * as y from "yup"
import { ChatOllama } from "@langchain/ollama"

let db;

async function langchain_getdb() {
    if (!db) {
        const datasource = new DataSource({type:"sqlite",database:dbpath});
        db = await SqlDatabase.fromDataSourceParams({ appDataSource:datasource});
    }
    return db;
}

async function langchain_getschema(){
    const db = await langchain_getdb();
    return await db.getTableInfo()
}

//ensure llm query is safe(constants and function from https://docs.langchain.com/oss/javascript/langchain/sql-agent)
const DENY_RE = /\b(INSERT|UPDATE|DELETE|ALTER|DROP|CREATE|REPLACE|TRUNCATE)\b/i;

function sanitizeSqlQuery(q) {
  let query = String(q ?? "").trim();

  const semis = [...query].filter((c) => c === ";").length;
  if (semis > 1 || (query.endsWith(";") && query.slice(0, -1).includes(";"))) {
    throw new Error("multiple statements not allowed.")
  }
  query = query.replace(/;+\s*$/g, "").trim();

  if (!query.toLowerCase().startsWith("select")) {
    throw new Error("Only SELECT statements are allowed")
  }
  if (DENY_RE.test(query)) {
    throw new Error("DML/DDL detected. Only read-only queries are permitted.")
  }
  return query;
}

const agent_executeQuery = tool(
    async ({q}) => {
        const query = sanitizeSqlQuery(q);
        try{
            const result = await db.run(query);
            return typeof result === "string" ? result : JSON.stringify(result,null,2);
        }
        catch(err){
            throw new Error(err?.message ?? String(err))
        }
    },
    {
        name:"execute_query",
        description:"Executes a read-only SQLite SELECT query and returns its results",
        schema: y.object({
            query: y.string().describe("Read-only SQLite SELECT query")
        }),
    }
);

//prompt extracted from https://docs.langchain.com/oss/javascript/langchain/sql-agent
const SQL_SystemPrompt = async() => new SystemMessage(`You are a careful SQLite analyst.
Authoritative schema (do not invent columns/tables):
${await langchain_getschema()}
You will receive a detailed prompt from another agent that directly interacts with a user.Create an SQLite query,following the rules below, when you are required to by this agent, in order to get necessary data.
Rules:
- Think step-by-step.
- When you need data, call the tool \`execute_sql\` with ONE SELECT query.
- Read-only only; no INSERT/UPDATE/DELETE/ALTER/DROP/CREATE/REPLACE/TRUNCATE.
- If the tool returns 'Error:', revise the SQL and try again.
- Limit the number of attempts to 5.

Return the results as a js object with an accurate label under the field "name", and results in an array under the field "results"
`);

const SQL_agent = new ChatOllama(  {
    model:"qwen3.5:0.8b",
    temperature: 0,
    maxRetries:2,
}).bindTools([
    agent_executeQuery,
]);

async function SQL_agent_response(message) {
    const response = await SQL_agent.invoke([
        ["system", {SQL_SystemPrompt}],
        ["outer_agent", message],
    ]);
    return response.content;
}

export const getchatmemory_tool = tool(
    async({prompt}) => {
        await SQL_agent_response(prompt)
    },
    {
        name: "getconversationinfo",
        description: "Get conversation info as needed in the form of a summary by an external agent that has access to the database",
        schema: y.object({
            prompt: y.string().describe("Create a prompt for the external SQL agent to use to return to you the relevant info from the database")
        })
    }
)
