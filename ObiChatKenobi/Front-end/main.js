let chat = document.getElementById('chat');
chat.scrollTop = chat.scrollHeight - chat.clientHeight;

let isTyping = 0

const typing = '<div id="typing" class="message stark"><div class="typing typing-1"></div><div class="typing typing-2"></div><div class="typing typing-3"></div></div>'

let input_message = document.getElementById('input_message')
let icon_send = document.getElementById('icon_send')
let icon_audio = document.getElementById('icon_audio')
let status = document.getElementById('status')

let time_message = document.querySelectorAll('.timeMessage')

let play_message = document.querySelectorAll('.play_text')

time_message.forEach(function (elem) {
    elem.innerHTML = getCurrentTime()
});

function speak_message(e) {
    let text = e.parentNode.children.item(0).innerHTML
    console.log(text)
    if ('speechSynthesis' in window) {
        let voices = getVoices();
        speak(text, voices[3]);
    } else {
        console.log(' Speech Synthesis Not Supported');
    }
}


//Speech recognition
const SpeechRecognition = window.SpeechRecognition || webkitSpeechRecognition;
const SpeechGrammarList = window.SpeechGrammarList || webkitSpeechGrammarList;
const SpeechRecognitionEvent = window.SpeechRecognitionEvent || webkitSpeechRecognitionEvent;


const recognition = new SpeechRecognition();
const speechRecognitionList = new SpeechGrammarList();

recognition.grammars = speechRecognitionList;
recognition.continuous = false;
recognition.lang = "en-US";
//recognition.lang = "IT-IT";
recognition.interimResults = false;
recognition.maxAlternatives = 1;


input_message.addEventListener('input', () => {
    if (input_message.value !== "") {
        icon_send.classList.remove('d-none')
        icon_audio.classList.add('d-none')
    } else {
        icon_audio.classList.remove('d-none')
        icon_send.classList.add('d-none')
    }


})

icon_audio.addEventListener('click', () => {
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


const send_message = function (value) {
    if (typeof value === 'object')
        value = input_message.value;
    icon_audio.classList.remove('d-none')
    icon_send.classList.add('d-none')
    console.log(value)
    chat.innerHTML = chat.innerHTML + '<div class="message parker"><span>' + value + '</span><div class="timeMessage">' + getCurrentTime() + '</div><i onclick="speak_message(this)" class="play_text uil uil-play"></i></div>'
    input_message.value = ''
    setTimeout(() => {
        manageMessage(1,value)
    }, 500)
    chat.scrollTop = chat.scrollHeight - chat.clientHeight;
}

icon_send.addEventListener('click', send_message)
input_message.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && input_message.value !== "") {
        send_message(input_message.value)
    }
})

/*Text to speech*/
function getVoices() {
    let voices = speechSynthesis.getVoices();

    if (!voices.length) {
        let utterance = new SpeechSynthesisUtterance("");
        speechSynthesis.speak(utterance);
        voices = speechSynthesis.getVoices();
    }
    return voices;
}

function speak(text, voice, rate = 1, pitch = 2, volume = 1) {
    // create a SpeechSynthesisUtterance to configure the how text to be spoken
    let speakData = new SpeechSynthesisUtterance();
    speakData.volume = volume; // From 0 to 1
    speakData.rate = rate; // From 0.1 to 10
    speakData.pitch = pitch; // From 0 to 2
    speakData.text = text;
    speakData.lang = 'en';
    speakData.voice = voice;

    // pass the SpeechSynthesisUtterance to speechSynthesis.speak to start speaking
    speechSynthesis.speak(speakData);

}

function getCurrentTime() {
    let date = new Date(Date.now());
    let minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
    return date.getHours() + ':' + minutes;
}

function manageTyping(trigger) {
    let message_typing = document.getElementById('typing')
    if (message_typing !== null) {
        message_typing.remove()
        status.innerHTML = 'Online'

    }
    if (trigger === 1) {
        chat.innerHTML = chat.innerHTML + typing
        status.innerHTML = 'Typing...'
        chat.scrollTop = chat.scrollHeight - chat.clientHeight;
    }
}

function manageMessage(trigger = 0,value) {

    manageTyping(trigger)
    isTyping++
    setTimeout(() => {
        if (isTyping === 1) {
            manageTyping(0)
            fetch('http://127.0.0.1:8000/getMsg/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json'
                },
                body:'{"speechRecognitionHypotesis":"'+value+'"}',
            }).then(response => response.json())
                .then(response => chat.innerHTML = chat.innerHTML + '<div class="message stark"><span>' + JSON.stringify(response["Message"]) + '</span><div class="timeMessage">' + getCurrentTime() + '</div><i onclick="speak_message(this)" class="play_text uil uil-play"></i></div>')
                .then(response => chat.scrollTop = chat.scrollHeight - chat.clientHeight)

        }
        isTyping--
    }, 1000)

}
