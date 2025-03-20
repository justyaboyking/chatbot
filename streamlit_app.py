// background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('Message received in background script:', message);

    if (message.type === 'analyzeAnswers') {
        const question = message.question;
        const choices = message.choices;

        fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                choices: choices
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Send the result back to the content script that sent the message
            chrome.tabs.sendMessage(sender.tab.id, {
                success: true,
                correctAnswerIndex: data.correctAnswerIndex
            });
            sendResponse({
                success: true,
                correctAnswerIndex: data.correctAnswerIndex
            });

        })
        .catch(error => {
            console.error('Error:', error);
            // Send the error back to the content script that sent the message
            chrome.tabs.sendMessage(sender.tab.id, {
                success: false,
                error: error.message
            });
            sendResponse({
                success: false,
                error: error.message
            });
        });

        return true; // Keep the message channel open for async response
    }
});

console.log('BookWidgets Helper background script initialized');
