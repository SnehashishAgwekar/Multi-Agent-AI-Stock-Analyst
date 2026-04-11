import yfinance as yf
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from crew import stock_crew
import yfinance as yf
import plotly.graph_objects as go

load_dotenv()

st.set_page_config(
    page_title="AI Stock Analyst",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS ----------
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
.block-container { padding: 2rem 2.5rem; max-width: 1400px; }

/* ── Header ── */
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
    50% { opacity: 0.7; box-shadow: 0 0 0 6px rgba(0,255,140,0); }
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 24px;
}

/* ── Stat Cards ── */
.stat-row {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
    flex-wrap: wrap;
}
.stat-card {
    flex: 1;
    min-width: 110px;
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 16px;
}
.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #f0f4f0;
}
.stat-value.green { color: #00ff8c; }
.stat-value.red   { color: #ff4d6d; }
.stat-sub {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: rgba(255,255,255,0.3);
    margin-top: 2px;
}

/* ── Input ── */
.stTextInput label {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    color: rgba(255,255,255,0.4) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
.stTextInput > div > div > input {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid rgba(0, 255, 140, 0.2) !important;
    border-radius: 10px !important;
    color: #00ff8c !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    padding: 14px 18px !important;
    letter-spacing: 2px !important;
    caret-color: #00ff8c;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0, 255, 140, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(0,255,140,0.08) !important;
}

/* ── Button ── */
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
    margin-top: 12px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0, 255, 140, 0.25) !important;
}

/* ── Chips ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; }
.chip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 5px 10px;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: rgba(255,255,255,0.35);
}
.chip span { color: #00ff8c; margin-right: 4px; }

/* ── Output ── */
.output-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 260px;
    gap: 12px;
    color: rgba(255,255,255,0.15);
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    letter-spacing: 1px;
}
.output-icon { font-size: 40px; opacity: 0.3; }

.result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}
.result-ticker {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #00ff8c;
    letter-spacing: 1px;
}
.result-status {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #00ff8c;
    background: rgba(0,255,140,0.08);
    border: 1px solid rgba(0,255,140,0.2);
    border-radius: 5px;
    padding: 3px 10px;
    letter-spacing: 2px;
}
.result-box {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(0, 255, 140, 0.12);
    border-radius: 12px;
    padding: 24px;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    line-height: 1.8;
    color: #c8d8c8;
    white-space: pre-wrap;
    max-height: 400px;
    overflow-y: auto;
}
.result-box::-webkit-scrollbar { width: 4px; }
.result-box::-webkit-scrollbar-track { background: transparent; }
.result-box::-webkit-scrollbar-thumb { background: rgba(0,255,140,0.2); border-radius: 2px; }

.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin: 20px 0 10px 0;
}
</style>
""", unsafe_allow_html=True)


# ---------- HELPER: Fetch price data ----------
def fetch_price_data(ticker: str):
    """Fetch current stats and 6-month OHLC history for a ticker."""
    try:
        t = yf.Ticker(ticker)

        # Fetch history FIRST before calling .info
        hist = t.history(period="6mo")
        hist.index = pd.to_datetime(hist.index).tz_localize(None)  # ✅ fixed  # strip timezone for Plotly

        if hist.empty:
            return {"ok": False, "error": f"No historical data found for {ticker}"}

        info = t.info

        price    = info.get("regularMarketPrice") or info.get("currentPrice") or float(hist["Close"].iloc[-1])
        change   = info.get("regularMarketChange", 0)
        pct      = info.get("regularMarketChangePercent", 0)
        volume   = info.get("regularMarketVolume") or int(hist["Volume"].iloc[-1])
        high52   = info.get("fiftyTwoWeekHigh") or float(hist["High"].max())
        low52    = info.get("fiftyTwoWeekLow") or float(hist["Low"].min())
        mktcap   = info.get("marketCap")
        currency = info.get("currency", "USD")
        name     = info.get("shortName", ticker.upper())

        if price is None:
            return {"ok": False, "error": f"Could not fetch price for {ticker}"}

        return {
            "ok": True,
            "name": name,
            "price": price,
            "change": change,
            "pct": pct,
            "volume": volume,
            "high52": high52,
            "low52": low52,
            "mktcap": mktcap,
            "currency": currency,
            "hist": hist,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def fmt_volume(v):
    if v is None: return "N/A"
    if v >= 1_000_000_000: return f"{v/1_000_000_000:.2f}B"
    if v >= 1_000_000:     return f"{v/1_000_000:.2f}M"
    if v >= 1_000:         return f"{v/1_000:.1f}K"
    return str(v)

def fmt_mktcap(v):
    if v is None: return "N/A"
    if v >= 1_000_000_000_000: return f"{v/1_000_000_000_000:.2f}T"
    if v >= 1_000_000_000:     return f"{v/1_000_000_000:.2f}B"
    if v >= 1_000_000:         return f"{v/1_000_000:.2f}M"
    return str(v)


def build_chart(hist, ticker, is_up):
    """Build a styled Plotly candlestick chart."""
    green = "#00ff8c"
    red   = "#ff4d6d"
    color = green if is_up else red

    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=hist.index,
        open=hist["Open"],
        high=hist["High"],
        low=hist["Low"],
        close=hist["Close"],
        increasing_line_color=green,
        decreasing_line_color=red,
        increasing_fillcolor=green,
        decreasing_fillcolor=red,
        name=ticker,
        whiskerwidth=0.3,
    ))

    # Volume bars at the bottom
    fig.add_trace(go.Bar(
        x=hist.index,
        y=hist["Volume"],
        name="Volume",
        marker_color=[green if c >= o else red
                      for c, o in zip(hist["Close"], hist["Open"])],
        opacity=0.25,
        yaxis="y2",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=8, b=0),
        height=340,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            color="rgba(255,255,255,0.25)",
            tickfont=dict(family="Space Mono", size=10, color="rgba(255,255,255,0.3)"),
            rangeslider=dict(visible=False),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.05)",
            zeroline=False,
            color="rgba(255,255,255,0.25)",
            tickfont=dict(family="Space Mono", size=10, color="rgba(255,255,255,0.3)"),
            side="right",
        ),
        yaxis2=dict(
            overlaying="y",
            side="left",
            showgrid=False,
            showticklabels=False,
            range=[0, hist["Volume"].max() * 5],
        ),
        legend=dict(
            font=dict(family="Space Mono", size=10, color="rgba(255,255,255,0.3)"),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            x=0, y=1.02,
        ),
        xaxis_rangeslider_visible=False,
    )
    return fig


# ---------- HEADER ----------
st.markdown("""
<div class="header-wrap">
    <div>
        <div class="header-badge"><span class="dot-live"></span>LIVE SYSTEM</div>
    </div>
    <div>
        <div class="header-title">AI Multi-Agent Stock Analyzer</div>
        <div class="header-sub">POWERED BY CREWAI &nbsp;·&nbsp; MULTI-AGENT PIPELINE &nbsp;·&nbsp; REAL-TIME ANALYSIS</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "result" not in st.session_state:
    st.session_state.result = None
    st.session_state.analyzed_stock = ""
    st.session_state.price_data = None

# ---------- LAYOUT ----------
col1, col2 = st.columns([1, 2], gap="large")

# ---------- LEFT PANEL ----------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    stock = st.text_input(
        "Stock Ticker / Name",
        value="TSLA",
        placeholder="e.g. AAPL, NVDA, RELIANCE"
    )

    run = st.button("🚀 Run Analysis")

    st.markdown("""
    <div class="chip-row">
        <div class="chip"><span>⚡</span>Multi-Agent</div>
        <div class="chip"><span>🔍</span>News Scan</div>
        <div class="chip"><span>📊</span>Fundamentals</div>
        <div class="chip"><span>🧠</span>AI Synthesis</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Price Stats Card (shows after run) ──
    if st.session_state.price_data and st.session_state.price_data["ok"]:
        d = st.session_state.price_data
        is_up = d["change"] >= 0
        sign  = "+" if is_up else ""
        clr   = "green" if is_up else "red"

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(255,255,255,0.3);
                    letter-spacing:3px;text-transform:uppercase;margin-bottom:14px;">
            {d['name']}
        </div>
        <div class="stat-row">
            <div class="stat-card">
                <div class="stat-label">Price</div>
                <div class="stat-value">{d['currency']} {d['price']:,.2f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Change</div>
                <div class="stat-value {clr}">{sign}{d['change']:.2f}</div>
                <div class="stat-sub">{sign}{d['pct']:.2f}%</div>
            </div>
        </div>
        <div class="stat-row">
            <div class="stat-card">
                <div class="stat-label">Volume</div>
                <div class="stat-value" style="font-size:16px">{fmt_volume(d['volume'])}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Mkt Cap</div>
                <div class="stat-value" style="font-size:16px">{fmt_mktcap(d['mktcap'])}</div>
            </div>
        </div>
        <div class="stat-row">
            <div class="stat-card">
                <div class="stat-label">52W High</div>
                <div class="stat-value green" style="font-size:15px">{d['high52']:,.2f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">52W Low</div>
                <div class="stat-value red" style="font-size:15px">{d['low52']:,.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------- RIGHT PANEL ----------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    # ── Run the crew + fetch price data ──
    if run and stock.strip():
        ticker = stock.strip().upper()

        # Fetch price data first (fast)
        with st.spinner(f"Fetching live data for {ticker}..."):
            st.session_state.price_data = fetch_price_data(ticker)
            st.session_state.analyzed_stock = ticker

        # ✅ DEBUG - paste here
        st.write("price_data ok:", st.session_state.price_data.get("ok"))
        st.write("error:", st.session_state.price_data.get("error"))
        if st.session_state.price_data.get("hist") is not None:
            st.write("hist shape:", st.session_state.price_data["hist"].shape)
            st.write(st.session_state.price_data["hist"].head())

        # Run AI agents
        with st.spinner(f"🤖 Agents analyzing {ticker} — this may take a minute..."):
            result = stock_crew.kickoff(inputs={"stock": ticker})
            st.session_state.result = str(result)

    # ── Chart section ──
    if st.session_state.price_data and st.session_state.price_data["ok"]:
        d      = st.session_state.price_data
        is_up  = d["change"] >= 0
        sign   = "+" if is_up else ""

        st.markdown(f"""
        <div class="result-header">
            <div class="result-ticker">{st.session_state.analyzed_stock}</div>
            <div class="result-status">{"▲" if is_up else "▼"} {sign}{d['pct']:.2f}%</div>
        </div>
        <div class="section-label">6-Month Price History</div>
        """, unsafe_allow_html=True)

        fig = build_chart(d["hist"], st.session_state.analyzed_stock, is_up)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    elif st.session_state.price_data and not st.session_state.price_data["ok"]:
        st.markdown(f"""
        <div class="output-empty">
            <div class="output-icon">⚠️</div>
            <div>Could not fetch data for this ticker</div>
            <div style="font-size:10px;opacity:0.5;">Check the symbol and try again</div>
        </div>
        """, unsafe_allow_html=True)

    # ── AI Analysis section ──
    if st.session_state.result:
        st.markdown('<div class="section-label">AI Agent Analysis</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="result-header" style="margin-top:0">
            <div style="font-family:'Space Mono',monospace;font-size:11px;color:rgba(255,255,255,0.3);">
                CrewAI · 2 Agents · Groq llama-3.3-70b
            </div>
            <div class="result-status">✓ COMPLETE</div>
        </div>
        <div class="result-box">{st.session_state.result}</div>
        """, unsafe_allow_html=True)

    elif not st.session_state.price_data:
        st.markdown("""
        <div class="output-empty">
            <div class="output-icon">📡</div>
            <div>AWAITING INPUT</div>
            <div style="font-size:10px; opacity:0.6;">Enter a ticker and hit Run Analysis</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)