export let messagelog = {
    role:[],
    content:[]
}

export function addmessage(role,msg){
    messagelog.role.push(role)
    messagelog.content.push(msg)
}
export function voidmessage() {
    if (messagelog.role.length === 2 || messagelog.content.length === 2) {
        messagelog.role = [];
        messagelog.content = []
    }
}