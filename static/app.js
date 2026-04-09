const form = document.getElementById("questionForm");
const input = document.getElementById("questionInput");
const askBtn = document.getElementById("askBtn");
const eightBall = document.getElementById("eightBall");
const triangle = document.getElementById("triangle");
const answerText = document.getElementById("answerText");

// Start with the "8" showing
answerText.classList.add("initial");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const question = input.value.trim();
  if (!question) return;

  // Disable while loading
  askBtn.disabled = true;
  askBtn.textContent = "...";
  input.disabled = true;

  // Reset display and shake
  answerText.className = "";
  answerText.classList.add("initial");
  answerText.textContent = "8";
  eightBall.classList.add("shaking");

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();

    // Wait for shake animation to finish
    await new Promise((r) => setTimeout(r, 900));

    eightBall.classList.remove("shaking");

    if (data.error) {
      answerText.textContent = data.error;
    } else {
      answerText.textContent = data.answer;
    }

    answerText.className = "reveal";
  } catch {
    await new Promise((r) => setTimeout(r, 900));
    eightBall.classList.remove("shaking");
    answerText.textContent = "The spirits are unavailable.";
    answerText.className = "reveal";
  } finally {
    askBtn.disabled = false;
    askBtn.textContent = "Ask";
    input.disabled = false;
    input.value = "";
    input.focus();
  }
});
