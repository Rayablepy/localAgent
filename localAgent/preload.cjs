const { contextBridge, ipcRenderer } = require("electron");
//const { getOllamaResponse } = require("/src/server/agentrouter.js")

contextBridge.exposeInMainWorld("AgentAPI", {
    getOllamaResponse: (message) =>
        ipcRenderer.invoke("ollama:chat", message)
});

contextBridge.exposeInMainWorld("CachingAPI", {
    insertMessage: (message) => {
        ipcRenderer.invoke("message-cache",message)
    }
})