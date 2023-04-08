let chat = document.getElementById('chat');
chat.scrollTop = chat.scrollHeight - chat.clientHeight;

let isTyping = 0

const typing = '<div id="typing" class="message stark"><div class="typing typing-1"></div><div class="typing typing-2"></div><div class="typing typing-3"></div></div>'

let input_message = document.getElementById('input_message')
let icon_send = document.getElementById('icon_send')
let icon_audio = document.getElementById('icon_audio')
let status = document.getElementById('status')

input_message.addEventListener('input', ()=>{
    if(input_message.value !== ""){
        icon_send.classList.remove('d-none')
        icon_audio.classList.add('d-none')
    }
    else{
        icon_audio.classList.remove('d-none')
        icon_send.classList.add('d-none')
    }


})


icon_send.addEventListener('click', ()=>{
    icon_audio.classList.remove('d-none')
    icon_send.classList.add('d-none')
    chat.innerHTML = chat.innerHTML + '<div class="message parker">'+input_message.value+'<div class="timeMessage">'+getCurrentTime()+'</div></div>'
    input_message.value = ''
    setTimeout(()=>{manageMessage(1)},500)
    chat.scrollTop = chat.scrollHeight - chat.clientHeight;

})

function getCurrentTime(){
    let date = new Date(Date.now());
    return date.getHours() +':'+ date.getMinutes();
}

function manageTyping(trigger){
    let message_typing = document.getElementById('typing')
    if(message_typing !== null){
        message_typing.remove()
        status.innerHTML = 'Online'

    }
    if(trigger === 1){
        chat.innerHTML = chat.innerHTML + typing
        status.innerHTML = 'Typing...'
        chat.scrollTop = chat.scrollHeight - chat.clientHeight;
    }
}

function manageMessage(trigger = 0){

    manageTyping(trigger)
    isTyping++
    setTimeout(()=>{
        if(isTyping === 1){
            manageTyping(0)
            chat.innerHTML = chat.innerHTML + '<div class="message stark"> Hola <div class="timeMessage">'+getCurrentTime()+'</div>'
            chat.scrollTop = chat.scrollHeight - chat.clientHeight;
        }
        isTyping--
    }, 1000)

}

