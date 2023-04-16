let chat = document.getElementById('chat');
chat.scrollTop = chat.scrollHeight - chat.clientHeight;

let isTyping = 0

const typing = '<div id="typing" class="message stark"><div class="typing typing-1"></div><div class="typing typing-2"></div><div class="typing typing-3"></div></div>'

let input_message = document.getElementById('input_message')
let icon_send = document.getElementById('icon_send')
let icon_audio = document.getElementById('icon_audio')
let status = document.getElementById('status')

let time_message = document.querySelectorAll('.timeMessage')

time_message.forEach(function (elem){
    elem.innerHTML = getCurrentTime()
});

//Speech recognition
const SpeechRecognition = window.SpeechRecognition || webkitSpeechRecognition;
const SpeechGrammarList = window.SpeechGrammarList || webkitSpeechGrammarList;
const SpeechRecognitionEvent = window.SpeechRecognitionEvent || webkitSpeechRecognitionEvent;


const recognition = new SpeechRecognition();
const speechRecognitionList = new SpeechGrammarList();

recognition.grammars = speechRecognitionList;
recognition.continuous = false;
//recognition.lang = "en-US";
recognition.lang = "IT-IT";
recognition.interimResults = false;
recognition.maxAlternatives = 1;



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

icon_audio.addEventListener('click',()=>{
  recognition.start();
  icon_audio.style.color = "red";
})

recognition.onresult = (event) => {
  const response = event.results[0][0].transcript;
  send_message(response)
  icon_audio.style.color = '#999';
};

recognition.onerror = (event) => {
  console.log(`Error occurred in recognition: ${event.error}`);
};


const send_message = function (value){
    if(typeof value === 'object')
        value = input_message.value;
    icon_audio.classList.remove('d-none')
    icon_send.classList.add('d-none')
    console.log(value)
    chat.innerHTML = chat.innerHTML + '<div class="message parker">'+value+'<div class="timeMessage">'+getCurrentTime()+'</div></div>'
    input_message.value = ''
    setTimeout(()=>{manageMessage(1)},500)
    chat.scrollTop = chat.scrollHeight - chat.clientHeight;
}

icon_send.addEventListener('click', send_message)
input_message.addEventListener('keypress', (e)=>{
     if (e.key === 'Enter' && input_message.value !== "") {
      send_message(input_message.value)
    }
})



function getCurrentTime(){
    let date = new Date(Date.now());
    let minutes = date.getMinutes() < 10 ? "0"+date.getMinutes() : date.getMinutes();
    return date.getHours() +':'+ minutes;
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

