// Medicine Search Suggestions
const input = document.getElementById('medicineInput');
const suggestionsList = document.getElementById('suggestionsList');

if (input) {
  input.addEventListener('input', () => {
    const query = input.value.trim();
    if (query.length < 2) {
      suggestionsList.style.display = 'none';
      return;
    }
    fetch(`/medicine_suggestions?q=${encodeURIComponent(query)}`)
      .then(response => response.json())
      .then(suggestions => {
        suggestionsList.innerHTML = '';
        if (suggestions.length === 0) {
          suggestionsList.style.display = 'none';
          return;
        }
        suggestions.forEach(name => {
          const li = document.createElement('li');
          li.textContent = name;
          li.classList.add('list-group-item', 'list-group-item-action');
          li.style.cursor = 'pointer';
          li.addEventListener('click', () => {
            input.value = name;
            suggestionsList.style.display = 'none';
          });
          suggestionsList.appendChild(li);
        });
        suggestionsList.style.display = 'block';
      })
      .catch(() => {
        suggestionsList.style.display = 'none';
      });
  });

  // Hide suggestions when clicking outside
  document.addEventListener('click', (e) => {
    if (!input.contains(e.target) && !suggestionsList.contains(e.target)) {
      suggestionsList.style.display = 'none';
    }
  });
}

// Voice Recognition for Symptoms Input
const voiceBtn = document.getElementById("voiceBtn");
const symptomsInput = document.getElementById("symptomsInput");
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (voiceBtn && SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.lang = "en-US";
  recognition.interimResults = false;

  voiceBtn.addEventListener("click", () => {
    recognition.start();
    voiceBtn.innerText = "🎙 Listening...";
  });

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    symptomsInput.value = transcript;
    voiceBtn.innerText = "🎤";
  };

  recognition.onerror = () => {
    voiceBtn.innerText = "🎤";
    alert("Voice recognition error. Please try again.");
  };

  recognition.onend = () => {
    voiceBtn.innerText = "🎤";
  };
} else if (voiceBtn) {
  voiceBtn.style.display = "none"; // Hide if not supported
}
