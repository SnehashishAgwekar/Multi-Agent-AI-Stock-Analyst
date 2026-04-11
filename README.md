# 📊 Multi-Agent AI Stock Analyst

An AI-powered multi-agent system that analyzes stocks, compares performance, and generates trading insights using autonomous agents.

---

## 🚀 Overview

This project implements a **multi-agent architecture** where different AI agents collaborate to simulate real-world financial roles like analysts and traders.

The system processes stock-related queries, performs analysis, and generates intelligent insights automatically.

Multi-agent systems are widely used in financial AI to break down complex tasks into specialized roles for better decision-making and scalability. ([GitHub][1])

---

## ✨ Features

* 📈 AI-based stock analysis
* 🔍 Stock comparison between companies
* 🤖 Multi-agent system (Analyst + Trader)
* 💬 AI chatbot for interaction
* ⚡ Modular and extensible architecture
* 🧠 Task-based workflow execution

---

## 🏗️ Architecture

The system is built using a **crew-based agent workflow**:

* **Analyst Agent**

  * Performs stock research and analysis
  * Extracts insights from data

* **Trader Agent**

  * Makes trading decisions
  * Provides recommendations

* **Tasks**

  * `analyze_task.py` → analysis logic
  * `trade_task.py` → trading logic

* **Crew (`crew.py`)**

  * Orchestrates agents
  * Manages workflow execution

---

## 📂 Project Structure

```bash
.
├── app.py                  # App entry point
├── main.py                 # Core execution
├── crew.py                 # Agent orchestration
├── analyst_agent.py        # Analyst agent
├── trader_agent.py         # Trader agent
├── analyze_task.py         # Analysis logic
├── trade_task.py           # Trading logic
├── stock_research_tool.py  # Data fetching
├── 2_AI_Chat.py            # Chatbot interface
├── 3_Stock_Comparison.py   # Stock comparison module
├── requirements.txt        # Dependencies
├── runtime.txt             # Runtime config
├── .env.example            # Environment variables template
```

---

## 🛠️ Tech Stack

* Python
* Crew-based AI agents
* LLM APIs (e.g., Groq / OpenAI)
* Stock data APIs

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/SnehashishAgwekar/Multi-Agent-AI-Stock-Analyst.git
cd Multi-Agent-AI-Stock-Analyst
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup environment variables

Create a `.env` file:

```bash
API_KEY=your_api_key_here
```

---

## ▶️ Run the Project

```bash
python main.py
```

or

```bash
python app.py
```

---

## 🧠 How It Works

1. User inputs a stock query
2. Analyst agent processes and analyzes data
3. Trader agent evaluates decisions
4. Crew coordinates execution
5. System outputs insights and recommendations

---

## 📊 Example Use Cases

* Compare stocks (e.g., Apple vs Tesla)
* Get AI-driven trading suggestions
* Analyze stock trends automatically

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.
It does not provide financial advice.

---

## 🚀 Future Improvements

* 🌐 Frontend dashboard (React)
* 📡 Real-time stock data integration
* 📊 Portfolio tracking
* ☁️ Deployment (AWS / Render / Vercel)

---

## 👨‍💻 Author

**Snehashish Agwekar**

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!

[1]: https://github.com/tauricresearch/tradingagents?utm_source=chatgpt.com "TradingAgents: Multi-Agents LLM Financial Trading ..."
