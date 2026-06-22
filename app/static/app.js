const form = document.querySelector("#calculator-form");
const promptInput = document.querySelector("#prompt");
const reasoning = document.querySelector("#reasoning");
const tool = document.querySelector("#tool");
const answer = document.querySelector("#answer");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  reasoning.textContent = "Understanding the task...";
  tool.textContent = "-";
  answer.textContent = "-";

  try {
    const response = await fetch("/api/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: promptInput.value }),
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Unable to calculate that request.");
    }

    reasoning.textContent = payload.reasoning;
    tool.textContent = payload.tool;
    answer.textContent = payload.answer;
  } catch (error) {
    reasoning.textContent = error.message;
    tool.textContent = "-";
    answer.textContent = "-";
  }
});
