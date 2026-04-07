import { obtainData,insertData } from '../db/databasehandler.js';
import messagelog from '/localAgent/src/client/Home.jsx'

const insertionresponse = await insertData("INSERT INTO messages (role,content) VALUES ('user','some text')");
console.log(insertionresponse);
console.log(messagelog.content[0])
const dataresponse = await obtainData("SELECT * FROM messages");
console.log(dataresponse);



