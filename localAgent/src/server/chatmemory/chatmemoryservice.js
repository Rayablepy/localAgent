import { insertMessage } from '../db/databasehandler.js';

function isValidMessageCycle(cachePayload) {
    if (!cachePayload) {
        return false;
    }

    const { role, content } = cachePayload;

    if (!Array.isArray(role) || !Array.isArray(content)) {
        return false;
    }

    if (role.length !== 2 || content.length !== 2) {
        return false;
    }

    return role.every((entry) => typeof entry === 'string' && entry.trim().length > 0)
        && content.every((entry) => typeof entry === 'string' && entry.trim().length > 0);
}

export async function persistMessageCycle(cachePayload) {
    if (!isValidMessageCycle(cachePayload)) {
        return false;
    }

    const messages = cachePayload.role.map((role, index) => ({
        role,
        content: cachePayload.content[index]
    }));

    return insertMessage(messages);
}


