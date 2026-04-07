import { DatabaseSync } from "node:sqlite";
import path from "path";
import {fileURLToPath} from "url";
//import fs from "fs";

//because of module js, __dirname has to be manually created
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const dbpath = path.join(__dirname,"finalsqlite")
const db = new DatabaseSync(dbpath);
//const schema = fs.readFileSync('./finalschema.sql','utf8')
/*
try {
    db.exec(schema);
    console.log("Database successfully created");

}
catch (error) {
    console.error(error);
}
*/
async function obtainData(query){
    const response=db.prepare(query);
    if (response.all.length>0) {
        return (response.all)
    }
    else {
        return ("No content returned from query")
    }
}

async function insertData(query){
    try {
        db.run(query);
        return ("insertion successful")
    }
    catch(error){
        return (error)
    }
}

export { obtainData,insertData };
