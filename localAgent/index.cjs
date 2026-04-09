const { app, BrowserWindow, ipcMain } = require("electron");
const { getOllamaResponse } = require("./src/server/agentrouter.js")
const { insertMessage } = require("./src/server/db/databasehandler.js")
const path = require("path");

let win
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
app.whenReady().then(()=> {
    ipcMain.handle('ollama:chat',async (_event,message) => {
        //console.log(typeof message,message);
        return await getOllamaResponse(message)
    });
    ipcMain.handle("message-cache",async (_event,message) => {
        return await insertMessage(message)
    })
    createwin()
})

app.on('window-all-closed', () => {
    if (process.platform !== "darwin") app.quit();
})
