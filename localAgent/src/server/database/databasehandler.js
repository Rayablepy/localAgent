import Database from "better-sqlite3";
import path from "path";
import {fileURLToPath} from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const dbpath = path.join(__dirname,"identifier.sqlite");
const db = new Database(dbpath);

const insertMessageStatement = db.prepare(
    "INSERT INTO messages (role, CONTENT) VALUES (?, ?)"
);

const insertMessagesTransaction = db.transaction((message) => {
    insertMessageStatement.run(message.role, message.content);
});

export async function insertMessage(message){
    try {
        insertMessagesTransaction(message);
        return true;
    }
    catch(error){
        console.error("Failed to insert message into SQLite", error);
        return false;
    }
}