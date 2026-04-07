import { obtainData,insertData } from '../db/databasehandler.js';

const insertionresponse = await insertData('INSERT INTO messages (role,content) VALUES ("user","Some text")');
console.log(insertionresponse);

const dataresponse = await obtainData('SELECT * FROM messages');
console.log(dataresponse);



