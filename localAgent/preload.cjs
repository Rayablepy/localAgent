const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("AgentAPI", {
    getOllamaResponse: (message) =>
        ipcRenderer.invoke("ollama:chat", message)
});

contextBridge.exposeInMainWorld("CachingAPI", {
    persistMessageCycle: (cachePayload) =>
        ipcRenderer.invoke("chat:persist-cycle", cachePayload)
});
