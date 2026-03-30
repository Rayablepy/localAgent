import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("AgentAPI", {
    getOllamaResponse: (message: string) =>
        ipcRenderer.invoke("ollama:chat", message),
});
