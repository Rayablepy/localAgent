const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("AgentAPI", {
    getOllamaResponse: (message) =>
        ipcRenderer.invoke("ollama:chat", message)
});

contextBridge.exposeInMainWorld("CachingAPI", {
    //backend to frontend
    insertionFulfilled: () => {
        ipcRenderer.send("CachingAPI-insertionpromise:BO") //BO stands for backend origin
    },
    //frontend to backend
    sendCache: () => {
        ipcRenderer.send("CachingAPI-insertionpromise:FO") //FO stands for frontend origin
    }
});