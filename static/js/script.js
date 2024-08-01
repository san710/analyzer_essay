document.addEventListener('DOMContentLoaded', function() {
    let essayTextarea = document.getElementById('essay');
    let contextTextarea = document.getElementById('context');
    let analyzeButton = document.getElementById('analyze');
    let startEssayButton = document.getElementById('startEssay');
    let wordCountDisplay = document.getElementById('wordCount');
    let warningDisplay = document.getElementById('warning');
    let analysisResults = document.getElementById('analysisResults');
    let timerDisplay = document.getElementById('timer');

    let startTime = null;
    let timerInterval = null;
    let analyzed = false;

    const updateWordCount = () => {
        let wordCount = essayTextarea.value.split(/\s+/).filter(word => word.length > 0).length;
        wordCountDisplay.textContent = wordCount;
        if (wordCount > 350) {
            warningDisplay.textContent = "You have reached the 350-word limit. You cannot add more words.";
            essayTextarea.value = essayTextarea.value.split(/\s+/).slice(0, 350).join(" ");
        } else if (wordCount > 340) {
            warningDisplay.textContent = "You are approaching the 350-word limit. You will not be able to add more words.";
        } else {
            warningDisplay.textContent = "";
        }
    };

    essayTextarea.addEventListener('input', updateWordCount);

    const startEssay = () => {
        if (!analyzed) {
            startTime = Date.now();
            analyzeButton.disabled = false;
            startEssayButton.disabled = true;
            timerInterval = setInterval(updateTimer, 1000);
        }
    };

    const updateTimer = () => {
        let elapsedTime = Math.floor((Date.now() - startTime) / 1000);
        let remainingTime = Math.max(0, 20 * 60 - elapsedTime);
        let minutes = Math.floor(remainingTime / 60);
        let seconds = remainingTime % 60;
        timerDisplay.textContent = `Remaining Time: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            analyzeButton.disabled = true;
        }
    };

    startEssayButton.addEventListener('click', startEssay);

    const highlightErrors = (text, errors) => {
        let highlightedText = "";
        let lastIndex = 0;
        errors.forEach(error => {
            highlightedText += text.substring(lastIndex, error.offset);
            highlightedText += `<span class="highlighted">${text.substring(error.offset, error.offset + error.length)}</span>`;
            lastIndex = error.offset + error.length;
        });
        highlightedText += text.substring(lastIndex);
        return highlightedText;
    };

    analyzeButton.addEventListener('click', () => {
        if (essayTextarea.value.split(/\s+/).filter(word => word.length > 0).length > 350) {
            warningDisplay.textContent = "The essay exceeds the 350-word limit.";
            return;
        }

        let elapsedTime = Math.floor((Date.now() - startTime) / 1000);
        let remainingTime = Math.max(0, 20 * 60 - elapsedTime);
        clearInterval(timerInterval);
        analyzed = true;
        analyzeButton.disabled = true;

        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: essayTextarea.value,
                context: contextTextarea.value
            })
        })
        .then(response => response.json())
        .then(data => {
            analysisResults.innerHTML = `
                <h2>Analysis Results</h2>
                <h3>Original Text:</h3>
                <p>${highlightErrors(data.original_text, data.errors)}</p>
                <h3>Context:</h3>
                <p>${contextTextarea.value}</p>
                <h3>Errors:</h3>
                <ul>${data.errors.map(error => `<li>${error.message} (Offset: ${error.offset})</li>`).join('')}</ul>
                <h3>Topics:</h3>
                <ul>${data.topics.map(topic => `<li>${topic}</li>`).join('')}</ul>
                <h3>Grammar Score:</h3>
                <p>${data.grammar_score}</p>
                <h3>Relevance Score:</h3>
                <p>${data.relevance_score}</p>
                <h3>Total Score:</h3>
                <p>${data.total_score}</p>
                <h3>Final Remaining Time:</h3>
                <p>${Math.floor(remainingTime / 60).toString().padStart(2, '0')}:${(remainingTime % 60).toString().padStart(2, '0')}</p>
            `;
        });
    });
});
