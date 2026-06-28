const chatBox = document.getElementById("chat-box");

async function sendMessage() {

    const input = document.getElementById("message");

    const message = input.value.trim();

    if(message==="") return;

    chatBox.innerHTML += `
        <p><strong>You:</strong> ${message}</p>
    `;

    input.value="";

    const response = await fetch("/chat",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            message:message
        })

    });

    const data = await response.json();

    chatBox.innerHTML += `
        <p><strong>CareerPilot AI:</strong> ${data.reply}</p>
    `;

    speak(data.reply);

    chatBox.scrollTop=chatBox.scrollHeight;

}


function startListening(){

    if(!('webkitSpeechRecognition' in window)){

        alert("Speech Recognition not supported.");

        return;

    }

    const recognition=new webkitSpeechRecognition();

    recognition.lang="en-US";

    recognition.start();

    recognition.onresult=function(event){

        const transcript=event.results[0][0].transcript;

        document.getElementById("message").value=transcript;

        sendMessage();

    };

}


function speak(text){

    const speech=new SpeechSynthesisUtterance(text);

    speech.lang="en-US";

    speech.rate=1;

    speech.pitch=1;

    window.speechSynthesis.speak(speech);

}