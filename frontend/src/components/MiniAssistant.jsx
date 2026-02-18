
import { useEffect, useRef, useState } from "react";

function MiniAssistant({ setActiveTab, solveEquation, result }) {
  console.log("MiniAssistant Mounted");
  const [isOpen, setIsOpen] = useState(false);
  const [active, setActive] = useState(false);
  const [transcript, setTranscript] = useState("");

  const recognitionRef = useRef(null);
console.log("SpeechRecognition available:", !!(window.SpeechRecognition || window.webkitSpeechRecognition));

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  useEffect(() => {
    if (!SpeechRecognition) {
      console.log("Speech Recognition not supported");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onresult = (event) => {
      const speech =
        event.results[event.results.length - 1][0].transcript.toLowerCase();

      setTranscript(speech);

      // Wake word
      if (speech.includes("hey mini")) {
        activateAssistant();
        return;
      }

      // Only process commands when active
      if (active) {
        handleCommand(speech);
      }
    };

    recognition.onend = () => {
      // Restart only if component still mounted
      try {
        recognition.start();
      } catch (err) {}
    };

    recognition.start();
    recognitionRef.current = recognition;

    return () => {
      recognition.stop();
    };
  }, [active]);

  // 🔊 Speech Output
  const speak = (text) => {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    window.speechSynthesis.speak(utterance);
  };

  const activateAssistant = () => {
    setIsOpen(true);
    setActive(true);
    speak("Hello. I am Mini. How can I help you?");
  };

  const deactivateAssistant = () => {
    setActive(false);
    speak("Going back to sleep.");
  };

  const handleCommand = (speech) => {
    if (speech.includes("text mode")) {
      setActiveTab("text");
      speak("Switched to text mode");
    }

    if (speech.includes("image mode")) {
      setActiveTab("image");
      speak("Switched to image mode");
    }

    if (speech.includes("voice mode")) {
      setActiveTab("voice");
      speak("Switched to voice mode");
    }

    if (speech.includes("draw mode")) {
      setActiveTab("draw");
      speak("Switched to draw mode");
    }

    if (speech.includes("solve")) {
      solveEquation();
      speak("Solving your equation");
    }

    if (speech.includes("read result") && result?.solution) {
      speak(`The solution is ${result.solution}`);
    }

    if (speech.includes("read steps") && result?.steps) {
      const allSteps = result.steps
        .map((s) => s.description)
        .join(". ");
      speak(allSteps);
    }

    if (speech.includes("help")) {
      speak(
        "You can say text mode, image mode, voice mode, draw mode, solve equation, read result, read steps, or say sleep."
      );
    }

    if (speech.includes("sleep")) {
      deactivateAssistant();
    }
  };

  return (
    <div className="assistant-float">
      {!isOpen && (
        <button
          className="assistant-circle"
          onClick={() => {
            setIsOpen(true);
            setActive(true);
            speak("Mini activated. How can I help you?");
          }}
        >
          🤖
        </button>
      )}

      {isOpen && (
        <div className="assistant-panel">
          <div className="assistant-header">
            <span>Mini Assistant</span>
            <button onClick={() => setIsOpen(false)}>✕</button>
          </div>

          <div className="assistant-body">
            <p className="assistant-status">
              {active
                ? "🟢 Active — Listening"
                : "🟡 Passive — Say 'Hey Mini'"}
            </p>

            {transcript && (
              <p className="assistant-transcript">
                Heard: {transcript}
              </p>
            )}

            <button
              className="assistant-action stop"
              onClick={deactivateAssistant}
            >
              Sleep
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default MiniAssistant;
