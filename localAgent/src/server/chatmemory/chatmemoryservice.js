
//local imports
import { insertMessage } from '../db/databasehandler.js';
//external imports
import { messagelogdetails } from '/localAgent/src/client/chatmemorycache.js';

export async function insertionFulfilled() {
    if (messagelogdetails.content.length === 2 || messagelogdetails.role.length === 2) {
        const insertionPromise = await insertMessage(messagelogdetails);
        return !!insertionPromise;
    }
}



