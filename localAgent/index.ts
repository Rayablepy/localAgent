import { app, BrowserWindow, ipcMain } from "electron";
import { getOllamaResponse } from "./src/server/agentrouter.js";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
let win: BrowserWindow | null = null;

function createWin() {
    win = new BrowserWindow({
        width: 1000,
        height: 1000,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            contextIsolation: true,
            nodeIntegration: false,
        },
    });

    const devServerUrl = process.env.VITE_DEV_SERVER_URL;

    if (devServerUrl) {
        win.loadURL(devServerUrl);
    } else {
        win.loadFile(path.join(__dirname, "../dist/index.html"));
    }

    win.on("closed", () => {
        win = null;
    });
}

app.whenReady().then(() => {
    ipcMain.handle("ollama:chat", async (_event, message: string) => {
        return await getOllamaResponse(message);
    });
    createWin();
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
});
