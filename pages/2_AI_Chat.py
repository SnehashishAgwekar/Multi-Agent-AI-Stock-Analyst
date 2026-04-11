import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq
import yfinance as yf
import pandas as pd

load_dotenv()

st.set_page_config(
    page_title="AI Stock Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS (same theme) ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

* { box-sizing: border-box; }

.stApp {
    background-color: #080c10;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0, 200, 120, 0.08) 0%, transparent 60%),
        repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(255,255,255,0.015) 39px, rgba(255,255,255,0.015) 40px),
        repeating-linear-gradient(90deg, transparent, transparent 79px, rgba(255,255,255,0.015) 79px, rgba(255,255,255,0.015) 80px);
    font-family: 'Syne', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem; max-width: 1200px; }

.header-wrap {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(0, 255, 140, 0.15);
}
.header-badge {
    background: rgba(0, 255, 140, 0.1);
    border: 1px solid rgba(0, 255, 140, 0.3);
    border-radius: 6px;
    padding: 4px 10px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: #00ff8c;
    letter-spacing: 2px;
}
.header-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #f0f4f0;
    margin: 0;
    letter-spacing: -0.5px;
}
.header-sub {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: rgba(255,255,255,0.35);
    margin-top: 2px;
}
.dot-live {
    width: 8px; height: 8px;
    background: #00ff8c;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(0,255,140,0.4); }
    50%       { opacity: 0.7; box-shadow: 0 0 0 6px rgba(0,255,140,0); }
}

.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
}

/* Chat bubbles */
.chat-user {
    display: flex;
    justify-content: flex-end;
    margin: 10px 0;
}
.chat-ai {
    display: flex;
    justify-content: flex-start;
    margin: 10px 0;
}
.bubble-user {
    background: rgba(0, 255, 140, 0.12);
    border: 1px solid rgba(0, 255, 140, 0.25);
    border-radius: 16px 16px 4px 16px;
    padding: 12px 18px;
    max-width: 75%;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    color: #e0f0e0;
    line-height: 1.6;
}
.bubble-ai {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px 16px 16px 4px;
    padding: 12px 18px;
    max-width: 75%;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    color: #c8d8c8;
    line-height: 1.8;
    white-space: pre-wrap;
}
.bubble-label {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: rgba(255,255,255,0.2);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.bubble-label-right {
    text-align: right;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: rgba(0,255,140,0.4);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

/* Chat input area */
.stTextInput > div > div > input {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid rgba(0, 255, 140, 0.2) !important;
    border-radius: 10px !important;
    color: #e0f0e0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 14px !important;
    padding: 14px 18px !important;
    caret-color: #00ff8c;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0, 255, 140, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(0,255,140,0.08) !important;
}
.stTextInput label {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    color: rgba(255,255,255,0.4) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

.stButton > button {
    width: 100% !important;
    border-radius: 10px !important;
    padding: 14px 0 !important;
    background: linear-gradient(135deg, #00ff8c 0%, #00cc6a 100%) !important;
    color: #060a08 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    letter-spacing: 1px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    margin-top: 8px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0, 255, 140, 0.25) !important;
}

.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 16px 0 10px 0;
}

.suggestion-chip {
    display: inline-block;
    background: rgba(0,255,140,0.06);
    border: 1px solid rgba(0,255,140,0.15);
    border-radius: 6px;
    padding: 5px 12px;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: rgba(0,255,140,0.6);
    margin: 4px 4px 4px 0;
    cursor: pointer;
}

.ticker-badge {
    display: inline-block;
    background: rgba(0,255,140,0.1);
    border: 1px solid rgba(0,255,140,0.3);
    border-radius: 5px;
    padding: 2px 8px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: #00ff8c;
    font-weight: 700;
    margin-left: 8px;
}

.chat-container {
    max-height: 520px;
    overflow-y: auto;
    padding-right: 4px;
    margin-bottom: 16px;
}
.chat-container::-webkit-scrollbar { width: 4px; }
.chat-container::-webkit-scrollbar-track { background: transparent; }
.chat-container::-webkit-scrollbar-thumb { background: rgba(0,255,140,0.2); border-radius: 2px; }

.empty-chat {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;
    gap: 12px;
    color: rgba(255,255,255,0.15);
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    letter-spacing: 1px;
}
.empty-icon { font-size: 48px; opacity: 0.25; }
</style>
""", unsafe_allow_html=True)


# ---------- GROQ CLIENT ----------
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found in .env file!")
        st.stop()
    return Groq(api_key=api_key)


# ---------- FETCH QUICK STOCK CONTEXT ----------
def get_stock_context(ticker: str) -> str:
    """Fetch brief stock data to inject into the AI system prompt."""
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="5d")
        hist.index = pd.to_datetime(hist.index).tz_localize(None)
        info = t.info

        price    = info.get("regularMarketPrice") or info.get("currentPrice") or float(hist["Close"].iloc[-1])
        change   = info.get("regularMarketChange", 0)
        pct      = info.get("regularMarketChangePercent", 0)
        high52   = info.get("fiftyTwoWeekHigh", "N/A")
        low52    = info.get("fiftyTwoWeekLow", "N/A")
        mktcap   = info.get("marketCap", "N/A")
        name     = info.get("shortName", ticker)
        sector   = info.get("sector", "N/A")
        pe       = info.get("trailingPE", "N/A")
        currency = info.get("currency", "USD")

        return (
            f"Stock: {name} ({ticker})\n"
            f"Current Price: {currency} {price:,.2f}\n"
            f"Daily Change: {change:+.2f} ({pct:+.2f}%)\n"
            f"52W High: {high52} | 52W Low: {low52}\n"
            f"Market Cap: {mktcap}\n"
            f"Sector: {sector}\n"
            f"P/E Ratio: {pe}\n"
        )
    except Exception:
        return f"Ticker: {ticker} (live data unavailable)"


# ---------- CHAT WITH GROQ ----------
def chat_with_groq(messages: list, stock_context: str) -> str:
    client = get_groq_client()

    system_prompt = f"""You are an expert AI stock market analyst and financial advisor assistant.
You have access to the following live market data for the stock the user is asking about:

{stock_context}

Use this data to give accurate, specific, and insightful answers.
Be concise but thorough. Use bullet points where helpful.
Always ground your analysis in the data provided.
If asked about price predictions, give a balanced view with both bull and bear cases.
Format numbers clearly (e.g., $250.40, +2.3%).
Do NOT make definitive buy/sell recommendations — instead provide analysis and let the user decide."""

    groq_messages = [{"role": "system", "content": system_prompt}]
    groq_messages += [{"role": m["role"], "content": m["content"]} for m in messages]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=groq_messages,
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content


# ---------- HEADER ----------
st.markdown("""
<div class="header-wrap">
    <div>
        <div class="header-badge"><span class="dot-live"></span>AI CHAT</div>
    </div>
    <div>
        <div class="header-title">AI Stock Chat</div>
        <div class="header-sub">POWERED BY GROQ &nbsp;·&nbsp; LLAMA 3.3 70B &nbsp;·&nbsp; REAL-TIME CONTEXT</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_ticker" not in st.session_state:
    st.session_state.chat_ticker = "TSLA"
if "stock_context" not in st.session_state:
    st.session_state.stock_context = ""

# ---------- LAYOUT ----------
col1, col2 = st.columns([1, 2.5], gap="large")

# ---------- LEFT PANEL ----------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    ticker_input = st.text_input(
        "Stock Ticker",
        value=st.session_state.chat_ticker,
        placeholder="e.g. AAPL, NVDA, TSLA"
    )

    load_btn = st.button("📡 Load Stock Context")

    if load_btn and ticker_input.strip():
        t = ticker_input.strip().upper()
        with st.spinner(f"Fetching context for {t}..."):
            ctx = get_stock_context(t)
        st.session_state.chat_ticker   = t
        st.session_state.stock_context = ctx
        st.session_state.chat_messages = []  # reset chat on new ticker

    st.markdown("</div>", unsafe_allow_html=True)

    # Stock context preview card
    if st.session_state.stock_context:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="section-label">Live Context Loaded</div>
        <div style="font-family:'Space Mono',monospace;font-size:11px;color:rgba(200,220,200,0.7);
                    line-height:1.9;white-space:pre-wrap;">{st.session_state.stock_context}</div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Clear chat button
    if st.session_state.chat_messages:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_messages = []
            st.rerun()

    # Suggested questions
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Suggested Questions</div>", unsafe_allow_html=True)
    suggestions = [
        "What is the current trend?",
        "Is it a good time to buy?",
        "What are the key risks?",
        "Explain the 52W range",
        "What does the P/E ratio mean?",
        "Give me a bull vs bear case",
    ]
    for s in suggestions:
        st.markdown(f"<div class='suggestion-chip'>💬 {s}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------- RIGHT PANEL ----------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    # Header row
    ticker_label = f"<span class='ticker-badge'>{st.session_state.chat_ticker}</span>" if st.session_state.stock_context else ""
    st.markdown(f"""
    <div style="display:flex;align-items:center;margin-bottom:16px;">
        <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:#f0f4f0;">
            Chat with AI Analyst
        </div>
        {ticker_label}
    </div>
    """, unsafe_allow_html=True)

    # Chat messages area
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    if not st.session_state.chat_messages:
        st.markdown("""
        <div class="empty-chat">
            <div class="empty-icon">🤖</div>
            <div>Load a stock and start asking questions</div>
            <div style="font-size:10px;opacity:0.5;">e.g. "Is TSLA a good buy right now?"</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-user">
                    <div>
                        <div class="bubble-label-right">YOU</div>
                        <div class="bubble-user">{msg['content']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-ai">
                    <div>
                        <div class="bubble-label">AI ANALYST · GROQ</div>
                        <div class="bubble-ai">{msg['content']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Input area
    st.markdown("<div class='section-label'>Your Question</div>", unsafe_allow_html=True)
    user_input = st.text_input(
        "Ask anything about the stock",
        placeholder="e.g. What are the key risks for this stock?",
        label_visibility="collapsed"
    )
    send_btn = st.button("💬 Send Message")

    if send_btn and user_input.strip():
        if not st.session_state.stock_context:
            st.warning("⚠️ Please load a stock context first using the left panel!")
        else:
            st.session_state.chat_messages.append({"role": "user", "content": user_input.strip()})
            with st.spinner("🤖 AI Analyst is thinking..."):
                reply = chat_with_groq(st.session_state.chat_messages, st.session_state.stock_context)
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)