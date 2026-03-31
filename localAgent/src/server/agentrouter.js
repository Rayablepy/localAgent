
import { ChatOllama } from "@langchain/ollama"

const agent = new ChatOllama({
    model:"llama3",
    temperature: 0,
    maxRetries:2,
})

export async function getOllamaResponse(message) {
    const response = await agent.invoke([
        ["system", "You are a local AI agent running on user machines. You will assist them with any needs and wants using the tools that will be at your disposal(tools not yet implemented)"],
        ["user",message]
    ]);
    //console.log(response)
    return response.content;
}


