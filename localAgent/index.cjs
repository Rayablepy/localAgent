const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { pathToFileURL } = require("url");

let win;
let getOllamaResponse;
let persistMessageCycle;

async function loadBackendModules() {
    const agentRouterModule = await import(
        pathToFileURL(path.join(__dirname, "src/server/agentrouter.js")).href
    );
    const chatMemoryServiceModule = await import(
        pathToFileURL(path.join(__dirname, "src/server/chatmemory/chatmemoryservice.js")).href
    );

    getOllamaResponse = agentRouterModule.getOllamaResponse;
    persistMessageCycle = chatMemoryServiceModule.persistMessageCycle;
}

function createwin() {
    win = new BrowserWindow({
        width:1000,
        height:1000,
        webPreferences: {
            preload: path.join(__dirname, "preload.cjs"),
            contextIsolation: true, //set by default(may change later)
            nodeIntegration: false
        }
    })

    const url = "http://localhost:5173/"

    win.loadURL(url);
    win.on('closed', () => (win=null));
}
app.whenReady().then(async () => {
    await loadBackendModules();

    ipcMain.handle('ollama:chat', async (_event, message) => {
        return await getOllamaResponse(message);
    });
    ipcMain.handle('chat:persist-cycle', async (_event, cachePayload) => {
        return await persistMessageCycle(cachePayload);
    });

    createwin();
});

app.on('window-all-closed', () => {
    if (process.platform !== "darwin") app.quit();
});
