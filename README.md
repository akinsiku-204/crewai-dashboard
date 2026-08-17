# 🤖 AI Dashboard Generator — Powered by CrewAI

Upload any CSV file and three AI agents automatically:
1. **Analyze** your data (column types, stats, patterns)
2. **Choose** the best charts (bar, line, pie, scatter)
3. **Write** plain-English insights about your data

---

## ⚡ Quick Setup (5 Steps)

### Step 1 — Install Python
Make sure you have Python 3.10–3.13 installed.
Check: `python --version`
Download: https://www.python.org/downloads/

---

### Step 2 — Install dependencies
Open a terminal inside this folder and run:

```bash
pip install -r requirements.txt
```

This installs Flask, CrewAI, Pandas, and dotenv. (~2-5 minutes)

---

### Step 3 — Get a FREE API Key (Groq — recommended)

1. Go to https://console.groq.com
2. Sign up for free (no credit card needed)
3. Click **API Keys** → **Create API Key**
4. Copy the key (starts with `gsk_...`)

---

### Step 4 — Add your API key

Open the `.env` file in a text editor and replace the placeholder:

**For Groq (free):** uncomment the Groq lines:
```
OPENAI_API_KEY=gsk_your-actual-key-here
OPENAI_BASE_URL=https://api.groq.com/openai/v1
OPENAI_MODEL_NAME=llama3-70b-8192
```

**For OpenAI (paid):** fill in your OpenAI key:
```
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL_NAME=gpt-4o-mini
```

---

### Step 5 — Run the app

```bash
python app.py
```

Then open your browser and go to:
**http://localhost:5000**

---

## 🗂️ Project Structure

```
crewai_dashboard/
├── app.py              ← Main app (Flask + CrewAI agents)
├── requirements.txt    ← Python dependencies
├── .env                ← Your API keys (never share this!)
├── README.md           ← This file
└── templates/
    └── index.html      ← Frontend dashboard UI
```

---

## 🤖 How the AI Agents Work

| Agent | Role | What it does |
|-------|------|-------------|
| Data Analyst | Reads CSV | Detects column types, calculates stats, finds nulls |
| Visualization Expert | Designs charts | Picks best chart type for each data relationship |
| Insights Writer | Writes findings | Generates 4-6 plain-English insights from the data |

---

## 📊 Supported Data Formats
- CSV files (`.csv`) — any size up to ~50,000 rows
- JSON files (`.json`) — array of objects format

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: crewai` | Run `pip install -r requirements.txt` again |
| `AuthenticationError` | Check your API key in `.env` is correct |
| `RateLimitError` | Wait 1 minute and try again (Groq free tier limit) |
| Port already in use | Change `port=5000` to `port=5001` in `app.py` |
| Charts not showing | Make sure your CSV has at least one numeric column |

---

## 💡 Tips for Best Results

- Your CSV should have **column headers** in the first row
- Include at least **one numeric column** and **one categorical column**
- The more specific your goal (the text box), the better the insights
- Use the agriculture dataset generated earlier as a test file

---

*Built with CrewAI, Flask, Chart.js, and Python*
