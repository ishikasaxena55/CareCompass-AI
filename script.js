
const API_URL = "http://127.0.0.1:8000/navigate";

const form = document.getElementById("care-form");
const concern = document.getElementById("concern");
const submitBtn = document.getElementById("submit-btn");

document.querySelectorAll(".topic").forEach(button => {
  button.addEventListener("click", () => {
    concern.value = button.dataset.prompt;
    concern.focus();
  });
});

form.addEventListener("submit", async event => {
  event.preventDefault();

  const userInput = concern.value.trim();
  if (!userInput) return;

  submitBtn.disabled = true;
  submitBtn.textContent = "Please wait...";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_input: userInput,
        language: document.getElementById("language").value,
        location: document.getElementById("location").value.trim(),
        conversation_history: []
      })
    });

    if (!response.ok) {
      throw new Error("Backend error: " + response.status);
    }

    const data = await response.json();
    showResult(data);

  } catch (error) {
    showResult({
      summary: "Backend connection problem",
      guidance: "Check that the backend is running on port 8000.",
      next_steps: [
        "Open http://127.0.0.1:8000/health",
        "Check the VS Code terminal for errors."
      ],
      notice: "No medical assessment was made."
    });
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Explore care options ↗";
  }
});

function showResult(data) {
  document.getElementById("results").hidden = false;

  document.getElementById("result-summary").textContent =
    data.summary || data.message || "Care guidance";

  document.getElementById("result-guidance").textContent =
    data.guidance || data.response || data.advice || "";

  const list = document.getElementById("result-steps");
  list.replaceChildren();

  (data.next_steps || data.resources || []).forEach(item => {
    const li = document.createElement("li");
    li.textContent =
      typeof item === "string" ? item : JSON.stringify(item);
    list.appendChild(li);
  });

  document.getElementById("result-notice").textContent =
    data.notice || "Demo only; not a diagnosis.";

  document.getElementById("results").scrollIntoView({
    behavior: "smooth"
  });
}

// Emergency buzzer
let audioContext = null;
let oscillator = null;
let gainNode = null;
let alarmTimer = null;

const alarmStatus = document.getElementById("alarm-status");

function stopAlarm() {
  if (alarmTimer) clearInterval(alarmTimer);
  alarmTimer = null;

  if (oscillator) {
    try {
      oscillator.stop();
    } catch (error) {}
    oscillator = null;
  }

  if (gainNode) {
    try {
      gainNode.disconnect();
    } catch (error) {}
    gainNode = null;
  }

  if (audioContext) {
    audioContext.close().catch(() => {});
    audioContext = null;
  }

  alarmStatus.textContent = "Alarm is off.";
}

document.getElementById("buzzer-btn").addEventListener("click", async () => {
  stopAlarm();

  try {
    const AudioContextClass =
      window.AudioContext || window.webkitAudioContext;

    if (!AudioContextClass) {
      throw new Error("Audio is not supported");
    }

    audioContext = new AudioContextClass();
    await audioContext.resume();

    oscillator = audioContext.createOscillator();
    gainNode = audioContext.createGain();

    oscillator.type = "square";
    oscillator.frequency.value = 880;
    gainNode.gain.value = 0.1;

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    oscillator.start();

    let high = true;

    alarmTimer = setInterval(() => {
      if (!oscillator || !audioContext) return;

      high = !high;
      oscillator.frequency.setValueAtTime(
        high ? 880 : 660,
        audioContext.currentTime
      );
    }, 400);

    alarmStatus.textContent =
      "Alarm sounding. Press Stop alarm to stop.";

  } catch (error) {
    alarmStatus.textContent =
      "Alarm could not start. Check your browser audio settings.";
  }
});

document.getElementById("stop-btn").addEventListener("click", stopAlarm);

document.querySelector(".call-btn").addEventListener("click", () => {
  alarmStatus.textContent =
    "Your device may open the phone dialer. Confirm the call there.";
});
