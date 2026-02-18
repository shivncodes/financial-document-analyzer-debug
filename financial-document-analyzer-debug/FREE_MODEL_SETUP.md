# 🆓 Free Model Setup Guide

## Option 1: Groq (RECOMMENDED - Easiest & Free)

**Why Groq?**
- ✅ Completely FREE
- ✅ Very fast inference
- ✅ High rate limits (30 requests/minute)
- ✅ No installation needed
- ✅ Works immediately

### Setup Steps:

1. **Get your FREE API key:**
   - Visit: https://console.groq.com/
   - Sign up (it's free!)
   - Go to API Keys section
   - Create a new API key
   - Copy the key

2. **Add to your `.env` file:**
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Restart the server:**
   ```bash
   ./run.sh
   ```

4. **That's it!** The code will automatically use Groq.

---

## Option 2: Ollama (Local, Unlimited, Free)

**Why Ollama?**
- ✅ Completely FREE
- ✅ Runs locally on your machine
- ✅ No API rate limits
- ✅ No internet required after setup
- ✅ Privacy - data stays on your machine

### Setup Steps:

1. **Install Ollama:**
   ```bash
   brew install ollama
   ```

2. **Start Ollama:**
   ```bash
   ollama serve
   ```
   (Keep this terminal open)

3. **Download a model (in a new terminal):**
   ```bash
   ollama pull llama3.2
   # or
   ollama pull mistral
   ```

4. **Update your `.env` file:**
   ```bash
   OLLAMA_API_KEY=""  # Leave empty for local
   # Or set base_url if Ollama is on a different port
   ```

5. **Update `agents.py` to use Ollama:**
   Change the model to: `"ollama/llama3.2"` or `"ollama/mistral"`

---

## Option 3: Google Gemini (Free Tier)

**Note:** You've already tried this and hit quota limits. It works but has restrictions.

- ✅ Free tier available
- ❌ Rate limits (you hit these)
- ❌ Daily quota limits

If you want to use Gemini when quota resets:
```bash
GEMINI_API_KEY=your_key_here
```

---

## Quick Comparison

| Feature | Groq | Ollama | Gemini |
|---------|------|--------|--------|
| Cost | FREE | FREE | FREE (tier) |
| Speed | ⚡ Very Fast | 🐢 Slower | ⚡ Fast |
| Rate Limits | High (30/min) | Unlimited | Low (you hit these) |
| Installation | None | Required | None |
| Internet | Required | Not needed | Required |
| Privacy | API call | Local | API call |

---

## Recommendation

**Start with Groq** - it's the easiest and works immediately!

1. Get API key: https://console.groq.com/
2. Add to `.env`: `GROQ_API_KEY=your_key`
3. Restart server: `./run.sh`
4. Done! 🎉

