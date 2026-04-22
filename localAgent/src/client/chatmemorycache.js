let messagelog = {
    role:[],
    content:[]
}

export function messagelogdetails() {
    return {
        role: [...messagelog.role],
        content: [...messagelog.content]
    };
}

export function addmessage(role,msg){
    messagelog.role.push(role)
    messagelog.content.push(msg)
}

export function isMessageCycleComplete() {
    return messagelog.role.length === 2 && messagelog.content.length === 2;
}

export function voidmessage() {
    messagelog.role = [];
    messagelog.content = [];
}
