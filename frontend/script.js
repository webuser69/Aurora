
const Theme = document.getElementById("Theme");
const Menu = document.getElementById("Menu");
const input = document.getElementById("input");
const sound = document.getElementById("Mute");
const container = document.getElementById("container");

let dark = false;
let Mute = false;

// Dark/light
function theme() {
  dark = !dark;
  document.body.setAttribute("data-theme", dark ? "dark" : "light");
  Theme.textContent = dark ? "☀️" : "🌙";
}

// Mute/unmute
function mute() {
  Mute = !Mute;
  sound.textContent = Mute ? "🔇" : "🔊";
}

// plus menu
function menu(){
  Menu.style.display = Menu.style.display === "flex" ? "none" : "flex";
}

function takePhoto() {
  alert("this feature will come soon");
}

function addPhoto() {
  alert("This feature not yet implimented");
}

function addFile() {
  alert("This feature not yet implimented");
}

// Add msg to chat
function addmsg(text, sender) {
  const msg = document.createElement("div");
  msg.className = `msg ${sender}`;
  msg.textContent = text;
  container.appendChild(msg);
  container.scrollTop = container.scrollHeight;
}

// Sending message to backend 
async function MsgtoServer(msg) {
  try{
     const res = await fetch("http://localhost:5500/message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg, Mute })
    });

    const { response } = await res.json();
    return response;
  }catch{
    return "Server error. try gain";
  }
}

// handel sending msg
async function send() {
  const msg = input.value.trim(); // User Message
  if (!msg) return;

  input.value = "";
  addmsg(msg, "user");

  const reply = await MsgtoServer(msg); // Aurora reply 
  addmsg(reply, "aurora");
  if(!Mute) speak(reply);
}

// Enter button
input.addEventListener("keydown", e => {
  if (e.key === "Enter") send();
});

// // microphone
// function voice() {
//   alert("this will come soon");
// }

// voice input through microphone
function voice() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-US";
  
  input.placeholder = "Listening... 🎤"; // UPDATED
  recognition.start();

  recognition.onresult = (event) => {
    input.placeholder = "Send a message..."; // RESET
    input.value = event.results[0][0].transcript;
    send(); // AUTO SUBMIT
  };

  recognition.onerror = (event) => {
    input.placeholder = "Send a message..."; // RESET
    alert("Voice error: " + event.error);
  };

  recognition.onend = () => {
    input.placeholder = "Send a message..."; // RESET even if user stops speaking
  };
}
