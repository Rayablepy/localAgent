const { app, BrowserWindow } = require("electron");
const path = require("path");

let win
function createwin() {
    win = new BrowserWindow({
        width:1000,
        height:1000
    })

    const url = "http://localhost:5173/"

    win.loadURL(url);
    win.on('closed', () => (win=null));
}

app.on('ready', createwin);



