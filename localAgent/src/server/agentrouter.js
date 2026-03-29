import ollama from 'ollama';

export async function getOllamaResponse(message) {
    const response = await ollama.chat({
        model: 'llama3',
        messages: [
            {role: "system", content: "You are a local AI agent running on user machines. You will assist them with any needs and wants using the tools that will be at your disposal(tools not yet implemented)"},
            { role: "user", content: message }
        ]
    });

    return response.message.content;
}


