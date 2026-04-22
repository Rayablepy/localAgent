import Database from "better-sqlite3";
import path from "path";
import {fileURLToPath} from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const dbpath = path.join(__dirname,"finalsqlite")
const db = new Database(dbpath);

const insertMessageStatement = db.prepare(
    "INSERT INTO messages (role, CONTENT) VALUES (?, ?)"
);

const insertMessagesTransaction = db.transaction((messages) => {
    for (const message of messages) {
        insertMessageStatement.run(message.role, message.content);
    }
});

function insertMessage(messages){
    try {
        insertMessagesTransaction(messages);
        return true;
    }
    catch(error){
        console.error("Failed to insert message cycle into SQLite", error);
        return false;
    }
}

export { insertMessage };
