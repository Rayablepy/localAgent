import { obtainData,insertData } from '../db/databasehandler.js';
import { messagelog } from '/localAgent/src/client/Home.jsx'

const usercontent = messagelog.content[0];
const aicontent = messagelog.content[1];

const insertionresponse = await insertData('INSERT INTO messages (role,content) VALUES ("user","some text")');
console.log(insertionresponse);

const dataresponse = await obtainData('SELECT * FROM messages');
console.log(dataresponse);



