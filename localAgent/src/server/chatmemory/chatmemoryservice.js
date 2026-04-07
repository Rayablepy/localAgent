import obtainData from '../db/databasehandler.js';
const dataresponse = await obtainData('SELECT * FROM messages');
console.log(dataresponse);