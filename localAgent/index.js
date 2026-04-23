import { app, BrowserWindow, ipcMain } from "electron";
import { getOllamaResponse } from './src/server/agentrouter.js'
import { insertMessage } from "./src/server/database/databasehandler.js";
import path from "path";
import process from "process";
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

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
    ipcMain.handle('database:messages',async (_event,message) => {
        return await insertMessage(message)
    })
    createwin()
})

app.on('window-all-closed', () => {
    if (process.platform !== "darwin") app.quit();
})
