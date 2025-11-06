const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    const voiceBtn = document.getElementById('voiceBtn');
    const voiceStatus = document.getElementById('voiceStatus');
    const voiceStatusText = document.getElementById('voiceStatusText');

    voiceBtn.addEventListener('click', startVoiceRecognition);

    function startVoiceRecognition() {
        recognition.start();
        voiceStatus.classList.remove('hidden');
        voiceStatusText.textContent = 'Listening... Speak now!';
        voiceBtn.disabled = true;
        voiceBtn.classList.add('opacity-50');
    }

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        voiceStatusText.textContent = `You said: "${transcript}"`;
        
        processVoiceCommand(transcript);
        
        setTimeout(() => {
            voiceStatus.classList.add('hidden');
        }, 3000);
    };

    recognition.onerror = function(event) {
        voiceStatusText.textContent = 'Error occurred. Please try again.';
        voiceStatus.classList.remove('hidden');
        
        setTimeout(() => {
            voiceStatus.classList.add('hidden');
        }, 3000);
        
        voiceBtn.disabled = false;
        voiceBtn.classList.remove('opacity-50');
    };

    recognition.onend = function() {
        voiceBtn.disabled = false;
        voiceBtn.classList.remove('opacity-50');
    };

    function processVoiceCommand(command) {
        const lowerCommand = command.toLowerCase();
        
        if (lowerCommand.includes('recommend') || lowerCommand.includes('suggest') || lowerCommand.includes('find')) {
            const keywords = extractKeywords(lowerCommand);
            document.getElementById('interests').value = keywords;
            getRecommendations();
        } 
        else if (lowerCommand.includes('search')) {
            const searchTerm = extractSearchTerm(lowerCommand);
            document.getElementById('searchQuery').value = searchTerm;
            searchBooks();
        }
        else if (lowerCommand.includes('browse') || lowerCommand.includes('show all')) {
            browseAllBooks();
        }
        else {
            document.getElementById('interests').value = command;
            getRecommendations();
        }
        
        speak('Finding books for you');
    }

    function extractKeywords(command) {
        const removeWords = ['recommend', 'suggest', 'find', 'books', 'about', 'on', 'me', 'show', 'get', 'please'];
        let words = command.split(' ').filter(word => !removeWords.includes(word));
        return words.join(' ');
    }

    function extractSearchTerm(command) {
        return command.replace(/search\s+(for\s+)?/i, '').trim();
    }

    function speak(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;
            speechSynthesis.speak(utterance);
        }
    }
} else {
    document.getElementById('voiceBtn').disabled = true;
    document.getElementById('voiceBtn').innerHTML = '<i class="fas fa-microphone-slash mr-2"></i>Voice Not Supported';
    console.warn('Speech Recognition not supported in this browser');
}

