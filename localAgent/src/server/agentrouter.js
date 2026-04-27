import { ChatOllama } from "@langchain/ollama"
import { getchatmemory_tool } from "./tools/getchatmemory.js";

const agent = new ChatOllama({
    model:"qwen3.5:0.8b",
    temperature: 0,
    maxRetries:2,
}).bindTools([
    getchatmemory_tool,
])

//TODO run ollama pull on qwen model above and copy name to getchatmemory tool
export async function getOllamaResponse(message) {
    const response = await agent.invoke([
        ["system", "You are a local AI agent running on user machines. You will assist them with any needs and wants using the tools that will be at your disposal(tools not yet implemented)"],
        ["user",message]
    ]);
    //console.log(response)
    return response.content;
}


