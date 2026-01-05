import express from "express";
import fetch from "node-fetch";

const app = express();
const PORT = process.env.PORT || 8000;

// 🔹 health check route (Koyeb ke liye)
app.get("/", (req, res) => {
  res.send("Bot is alive");
});

// 🔹 Telegram Bot logic (example)
const BOT_TOKEN = process.env.BOT_TOKEN;

async function sendMessage(chatId, text) {
  const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
  await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text }),
  });
}

// 🔹 webhook / polling ka logic yahan hota hai
// (jo tum already use kar rahe ho)

// 🔹 server start (MANDATORY for Koyeb)
app.listen(PORT, () => {
  console.log("Server running on port", PORT);
});
