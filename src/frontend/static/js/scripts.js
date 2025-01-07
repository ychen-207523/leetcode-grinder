document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("addQuestionForm");
  const getRandomQuestionBtn = document.getElementById("getRandomQuestion");
  const messageDiv = document.getElementById("message");
  const randomQuestionDiv = document.getElementById("randomQuestion");
  const aiChat = document.getElementById("sendChat")

  // Add question form submission
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const questionData = {
      id: document.getElementById("id").value,
      title: document.getElementById("title").value,
      difficulty: document.getElementById("difficulty").value,
      url: document.getElementById("url").value,
    };

    try {
      const response = await fetch("/add-question", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(questionData),
      });

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.style.color = "green";
      } else {
        messageDiv.textContent = result.error || "An error occurred.";
        messageDiv.style.color = "red";
      }
    } catch (error) {
      messageDiv.textContent = "Failed to add question. Please try again.";
      messageDiv.style.color = "red";
    }
  });

  // Fetch and display a random question
  const fetchRandomQuestion = async () => {
    try {
      const response = await fetch("/get-random-question");
      const data = await response.json();

      if (response.ok) {
        randomQuestionDiv.innerHTML = `
          <p><strong>Title:</strong> ${data.title}</p>
          <p><strong>Difficulty:</strong> ${data.difficulty}</p>
          <p><a href="${data.url}" target="_blank">View Problem</a></p>
        `;
      } else {
        randomQuestionDiv.textContent = data.error || "No question available.";
        randomQuestionDiv.style.color = "red";
      }
    } catch (error) {
      randomQuestionDiv.textContent = "Failed to fetch a random question.";
      randomQuestionDiv.style.color = "red";
    }
  };

  // Attach the fetchRandomQuestion function to the button
  getRandomQuestionBtn.addEventListener("click", fetchRandomQuestion);

  const fetchAiResponse = async (message) => {
    const chatInput = document.getElementById("chatInput").value;
    const chatResponseDiv = document.getElementById("chatResponse");
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: chatInput }),
        });

        const data = await response.json();

        if (response.ok) {
            chatResponseDiv.textContent = data.response;
        } else {
            chatResponseDiv.textContent = data.error || "An error occurred.";
        }
    } catch (error) {
        chatResponseDiv.textContent = "Failed to connect to ChatGPT.";
    }
  }
  aiChat.addEventListener("click", fetchAiResponse);
});
