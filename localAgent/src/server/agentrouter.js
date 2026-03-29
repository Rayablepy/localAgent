import { tool } from "@langchain/core/tools";
import { ChatOllama } from "@langchain/ollama";
import * as z from "zod";

const test_tool = tool(
    async ({ name })=> {
        return `test_tool describes name as ${name}`;
    },
    {
        name:"test",
        description: "Test description",
        schema: z.object({
            test:  z.string().describe("return some text prepended to the name variable passed in")
        }),
    });

const agent = new ChatOllama({
    model:"llama3.1:8b",
    temperature: 0,
    maxRetries:2,
})
const agentwithtool = agent.bindTools([test_tool]);

export async function getOllamaResponse(message) {
    const response = await agentwithtool.invoke([
        ["system", "You are a local AI agent running on user machines. You will assist them with any needs and wants using the tools that will be at your disposal(tools not yet implemented)"],
        ["user",message]
    ]);
    return response.tool_calls;
}


