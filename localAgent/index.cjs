const { app, BrowserWindow, ipcMain } = require("electron");
const { getOllamaResponse } = require("./src/server/agentrouter.js")
const { insertionFulfilled } = require("./src/server/chatmemory/chatmemoryservice.js")
const { messagelogdetails } = require("./src/client/chatmemorycache.js")
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
app.whenReady().then(async () => {
    //backend -> frontend
    ipcMain.handle('ollama:chat', async (_event, message) => {
        //console.log(typeof message,message);
        return await getOllamaResponse(message);
    });
    ipcMain.handle('CachingAPI-insertionpromise:BO', async(_event) => {
        return await insertionFulfilled();
    })
    //frontend -> backend
    ipcMain.handle('CachingAPI-insertionpromise:FO', async(_event) => {
        return messagelogdetails();
    })
    createwin()
})

app.on('window-all-closed', () => {
    if (process.platform !== "darwin") app.quit();
})
