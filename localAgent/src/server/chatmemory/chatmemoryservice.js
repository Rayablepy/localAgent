import { insertMessage } from '../db/databasehandler.js';
import { messagelog } from '/localAgent/src/client/chatmemorycache.js';

export let insertionFulfilled = false
if (messagelog.content.length === 2 || messagelog.role.length === 2){
    const insertionPromise = await insertMessage(messagelog);
    if (insertionPromise) {
        insertionFulfilled = true
    }
    else {
        insertionFulfilled = false
    }
}




