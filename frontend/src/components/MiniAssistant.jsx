import { useState, useRef } from "react";

function MiniAssistant({
  setActiveTab,
  solveEquation,
  setEquation,
}) {
  const [listening, setListening] = useState(false);

  // 🔥 Use ref instead of state for confirmation flow
  const awaitingStepResponseRef = useRef(false);

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  // ===================== SPEAK =====================
  const speak = (text, callback) => {
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;

    utterance.onend = () => {
      if (callback) callback();
    };

    window.speechSynthesis.speak(utterance);
  };

  // ===================== LISTEN =====================
  const startListening = () => {
    if (!SpeechRecognition) {
      alert("Speech recognition not supported.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      console.log("🎤 Listening...");
      setListening(true);
    };

    recognition.onresult = (event) => {
      const speech = event.results[0][0].transcript
        .toLowerCase()
        .trim();

      console.log("Heard:", speech);
      handleCommand(speech);
    };

    recognition.onend = () => {
      console.log("🛑 Stopped listening");
      setListening(false);
    };

    recognition.start();
  };

  // ===================== HANDLE COMMAND =====================
  const handleCommand = async (speech) => {
    console.log("Command:", speech);

    // 🔥 STEP CONFIRMATION FLOW (using ref)
    if (awaitingStepResponseRef.current) {
      awaitingStepResponseRef.current = false;

      const positive = /(yes|yeah|yep|sure|okay|ok|please|go ahead)/i;
      const negative = /(no|nope|not now|stop)/i;

      if (positive.test(speech)) {
        speakSteps();
      } else if (negative.test(speech)) {
        speak("Thank you. Call me if you need help again.");
      } else {
        speak("Please say yes or no.", () => {
          awaitingStepResponseRef.current = true;
          startListening();
        });
      }

      return;
    }

    // ================= MODE SWITCH =================
    if (speech.includes("text mode")) {
      setActiveTab("text");
      document.getElementById("solver")?.scrollIntoView({
        behavior: "smooth",
      });
      speak("Switched to text mode.");
      return;
    }

    if (speech.includes("image mode")) {
      setActiveTab("image");
      speak("Switched to image mode.");
      return;
    }

    if (speech.includes("voice mode")) {
      setActiveTab("voice");
      speak("Switched to voice mode.");
      return;
    }

    if (speech.includes("draw mode")) {
      setActiveTab("draw");
      speak("Switched to draw mode.");
      return;
    }

    // ================= SOLVE =================
    if (speech.startsWith("solve")) {
      const expression = speech.replace("solve", "").trim();

      if (!expression) {
        speak("Please say the equation after solve.");
        return;
      }

      setActiveTab("text");
      setEquation(expression);

      document.getElementById("solver")?.scrollIntoView({
        behavior: "smooth",
      });

      speak(`Solving ${expression}`);

      const solvedData = await solveEquation(expression);

      if (solvedData?.solution) {
        speak(`The answer is ${solvedData.solution}`, () => {
          speak("Would you like me to hear the steps?", () => {
            awaitingStepResponseRef.current = true;
            startListening();
          });
        });
      }

      return;
    }

    speak("I did not understand that.");
  };

  // ================= SPEAK STEPS =================
  const speakSteps = async () => {
    const solvedData = await solveEquation();

    if (!solvedData?.steps) {
      speak("No steps available.");
      return;
    }

    let text = "";

    solvedData.steps.forEach((step) => {
      text += `Step ${step.step}. ${step.description}. `;
    });

    speak(text);
  };

  // ================= BUTTON CLICK =================
  const handleClick = () => {
    speak("Hey! How can I help you?", () => {
      startListening();
    });
  };

  return (
    <div className="assistant-container">
      <button
        className={`assistant-button ${listening ? "active" : ""}`}
        onClick={handleClick}
      >
        🎤
      </button>
    </div>
  );
}

export default MiniAssistant;
