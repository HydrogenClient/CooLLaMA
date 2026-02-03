let conversationHistory = [];

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const message = req.body?.message;
  if (!message) return res.status(400).json({ error: "Message is required" });

  const HF_API_TOKEN = process.env.HF_API_TOKEN || "";
  if (!HF_API_TOKEN) return res.status(500).json({ error: "HF_API_TOKEN not set" });

  conversationHistory.push(`User: ${message}`);
  if (conversationHistory.length > 10) conversationHistory.shift();

  const prompt = `
You are CooLLaMA, a fun and helpful chatbot.
Answer clearly and cheerfully.

${conversationHistory.join("\n")}
CooLLaMA:
`;

  try {
    const response = await fetch("https://api-inference.huggingface.co/models/tiiuae/gemini-2-2b", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${HF_API_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ inputs: prompt }),
    });

    if (!response.ok) {
      const text = await response.text();
      console.error("HF API error:", text);
      return res.status(500).json({ response: "Hugging Face API error" });
    }

    const data = await response.json();
    const botResponse = data?.[0]?.generated_text?.replace(prompt, "").trim() || "Sorry, I couldn't respond.";

    conversationHistory.push(`CooLLaMA: ${botResponse}`);
    if (conversationHistory.length > 10) conversationHistory.shift();

    res.status(200).json({ response: botResponse });

  } catch (err) {
    console.error("Server error:", err);
    res.status(500).json({ response: "Internal server error" });
  }
}