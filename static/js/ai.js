
// Chat functionality
const chatMessages = document.querySelector('.chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', () => {
    const userMessage = userInput.value;

    // Send the user's message to the AI (simplified example)
    const aiResponse = getAIResponse(userMessage);

    // Display the user's message
    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('user-message');
    userMessageDiv.textContent = userMessage;
    chatMessages.appendChild(userMessageDiv);  


    // Display the AI's response
    const aiResponseDiv = document.createElement('div');
    aiResponseDiv.classList.add('ai-response');
    aiResponseDiv.textContent = aiResponse;
    chatMessages.appendChild(aiResponseDiv);

    userInput.value = '';
});

async function getAIResponse(userMessage) {
    try {
        const response = await fetch('https://your-api-endpoint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Add authentication headers if needed
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.message; // Assuming the API returns a JSON object with a 'message' property
    } catch (error) {
        console.error('Error fetching AI response:', error);
        return 'An error occurred. Please try again later.';
    }
}