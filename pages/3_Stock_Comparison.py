import streamlit as st
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

load_dotenv()

st.set_page_config(
    page_title="Stock Comparison",
    page_icon="📊",
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

.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
}

.vs-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: rgba(255,255,255,0.15);
    padding-top: 32px;
}

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
    font-size: 20px !important;
    font-weight: 700 !important;
    padding: 14px 18px !important;
    letter-spacing: 3px !important;
    caret-color: #00ff8c;
    text-align: center !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0, 255, 140, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(0,255,140,0.08) !important;
}

.stButton > button {
    width: 100% !important;
    border-radius: 10px !important;
    padding: 14px 0 !important;
    background: linear-gradient(135deg, #00ff8c 0%, #00cc6a 100%) !important;
    color: #060a08 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 15px !important;
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

.stat-row { display: flex; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
.stat-card {
    flex: 1;
    min-width: 100px;
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 12px 14px;
}
.stat-label {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 17px;
    font-weight: 800;
    color: #f0f4f0;
}
.stat-value.green { color: #00ff8c; }
.stat-value.red   { color: #ff4d6d; }

.compare-header {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 16px;
}

.output-empty {
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
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ---------- HELPERS ----------
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

def fetch_stock(ticker: str) -> dict:
    try:
        t    = yf.Ticker(ticker)
        hist = t.history(period="6mo")
        hist.index = pd.to_datetime(hist.index).tz_localize(None)
        if hist.empty:
            return {"ok": False, "error": f"No data found for '{ticker}'. Use a valid ticker symbol like AAPL, TSLA."}
        info     = t.info
        price    = info.get("regularMarketPrice") or info.get("currentPrice") or float(hist["Close"].iloc[-1])
        change   = info.get("regularMarketChange", 0)
        pct      = info.get("regularMarketChangePercent", 0)
        volume   = info.get("regularMarketVolume") or int(hist["Volume"].iloc[-1])
        high52   = info.get("fiftyTwoWeekHigh") or float(hist["High"].max())
        low52    = info.get("fiftyTwoWeekLow") or float(hist["Low"].min())
        mktcap   = info.get("marketCap")
        currency = info.get("currency", "USD")
        name     = info.get("shortName", ticker.upper())
        pe       = info.get("trailingPE")
        beta     = info.get("beta")
        sector   = info.get("sector", "N/A")
        if price is None:
            return {"ok": False, "error": f"Price unavailable for {ticker}"}
        return {
            "ok": True, "name": name, "ticker": ticker,
            "price": price, "change": change, "pct": pct,
            "volume": volume, "high52": high52, "low52": low52,
            "mktcap": mktcap, "currency": currency,
            "pe": pe, "beta": beta, "sector": sector, "hist": hist,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def build_price_chart(d1, d2):
    h1 = d1["hist"]["Close"]
    h2 = d2["hist"]["Close"]
    common = h1.index.intersection(h2.index)
    h1 = h1.loc[common]
    h2 = h2.loc[common]
    n1 = (h1 / h1.iloc[0]) * 100
    n2 = (h2 / h2.iloc[0]) * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n1.index, y=n1.values, name=d1["ticker"], mode="lines",
                             line=dict(color="#00ff8c", width=2),
                             fill="tozeroy", fillcolor="rgba(0,255,140,0.04)"))
    fig.add_trace(go.Scatter(x=n2.index, y=n2.values, name=d2["ticker"], mode="lines",
                             line=dict(color="#4da6ff", width=2),
                             fill="tozeroy", fillcolor="rgba(77,166,255,0.04)"))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=8, b=0), height=300,
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(family="Space Mono", size=10, color="rgba(255,255,255,0.3)")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False,
                   tickfont=dict(family="Space Mono", size=10, color="rgba(255,255,255,0.3)"), side="right"),
        legend=dict(font=dict(family="Space Mono", size=10, color="rgba(255,255,255,0.4)"),
                    bgcolor="rgba(0,0,0,0)", orientation="h", x=0, y=1.1),
        hovermode="x unified",
    )
    return fig


def build_volume_chart(d1, d2):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d1["hist"].index, y=d1["hist"]["Volume"],
                         name=d1["ticker"], marker_color="rgba(0,255,140,0.5)"))
    fig.add_trace(go.Bar(x=d2["hist"].index, y=d2["hist"]["Volume"],
                         name=d2["ticker"], marker_color="rgba(77,166,255,0.5)"))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=8, b=0), height=220, barmode="group",
        xaxis=dict(showgrid=False, zeroline=False,
                   tickfont=dict(family="Space Mono", size=9, color="rgba(255,255,255,0.3)")),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                   tickfont=dict(family="Space Mono", size=9, color="rgba(255,255,255,0.3)"), side="right"),
        legend=dict(font=dict(family="Space Mono", size=10, color="rgba(255,255,255,0.4)"),
                    bgcolor="rgba(0,0,0,0)", orientation="h", x=0, y=1.1),
    )
    return fig


# ---------- HEADER ----------
st.markdown("""
<div class="header-wrap">
    <div><div class="header-badge">📊 COMPARE</div></div>
    <div>
        <div class="header-title">Stock Comparison</div>
        <div class="header-sub">SIDE-BY-SIDE ANALYSIS &nbsp;·&nbsp; 6-MONTH PERFORMANCE &nbsp;·&nbsp; KEY METRICS</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "cmp_data" not in st.session_state:
    st.session_state.cmp_data = None

# ---------- INPUT SECTION ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-label'>Enter Two Stock Tickers to Compare</div>", unsafe_allow_html=True)

col_t1, col_vs, col_t2, col_btn = st.columns([2, 0.4, 2, 1.2], gap="small")

with col_t1:
    t1 = st.text_input("Stock 1", value="TSLA", placeholder="e.g. TSLA")

with col_vs:
    st.markdown("<div class='vs-divider'>VS</div>", unsafe_allow_html=True)

with col_t2:
    t2 = st.text_input("Stock 2", value="AAPL", placeholder="e.g. AAPL")

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    compare_btn = st.button("⚡ Compare Now")

st.markdown("</div>", unsafe_allow_html=True)

# ---------- RUN ----------
if compare_btn and t1.strip() and t2.strip():
    tk1 = t1.strip().upper()
    tk2 = t2.strip().upper()
    with st.spinner(f"Fetching live data for {tk1} and {tk2}..."):
        d1 = fetch_stock(tk1)
        d2 = fetch_stock(tk2)
    if not d1["ok"]:
        st.error(f"❌ {d1['error']}")
    elif not d2["ok"]:
        st.error(f"❌ {d2['error']}")
    else:
        st.session_state.cmp_data = (d1, d2)

# ---------- RESULTS ----------
if st.session_state.cmp_data:
    d1, d2 = st.session_state.cmp_data
    is_up1 = d1["change"] >= 0
    is_up2 = d2["change"] >= 0
    sign1  = "+" if is_up1 else ""
    sign2  = "+" if is_up2 else ""
    clr1   = "green" if is_up1 else "red"
    clr2   = "green" if is_up2 else "red"

    # ── Price Chart ──
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='section-label'>
        6-Month Normalized Price Performance &nbsp;
        <span style='color:#00ff8c;'>{d1['ticker']}</span>
        <span style='color:rgba(255,255,255,0.2);margin:0 6px;'>vs</span>
        <span style='color:#4da6ff;'>{d2['ticker']}</span>
        <span style='color:rgba(255,255,255,0.2);margin-left:12px;font-size:9px;'>(Base = 100)</span>
    </div>
    """, unsafe_allow_html=True)
    st.plotly_chart(build_price_chart(d1, d2), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Side by Side Cards ──
    left, right = st.columns(2, gap="large")

    def render_card(d, clr, sign, hex_color):
        st.markdown(f"""
        <div class='card'>
            <div class='compare-header' style='color:{hex_color};'>
                {d['ticker']}
                <span style='font-family:Space Mono,monospace;font-size:12px;
                             color:rgba(255,255,255,0.3);font-weight:400;margin-left:10px;'>
                    {d['name']}
                </span>
            </div>
            <div class="stat-row">
                <div class="stat-card">
                    <div class="stat-label">Price</div>
                    <div class="stat-value">{d['currency']} {d['price']:,.2f}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Daily Change</div>
                    <div class="stat-value {clr}">{sign}{d['change']:.2f}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">% Change</div>
                    <div class="stat-value {clr}">{sign}{d['pct']:.2f}%</div>
                </div>
            </div>
            <div class="stat-row">
                <div class="stat-card">
                    <div class="stat-label">Market Cap</div>
                    <div class="stat-value" style="font-size:14px">{fmt_mktcap(d['mktcap'])}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Volume</div>
                    <div class="stat-value" style="font-size:14px">{fmt_volume(d['volume'])}</div>
                </div>
            </div>
            <div class="stat-row">
                <div class="stat-card">
                    <div class="stat-label">52W High</div>
                    <div class="stat-value green" style="font-size:14px">{d['high52']:,.2f}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">52W Low</div>
                    <div class="stat-value red" style="font-size:14px">{d['low52']:,.2f}</div>
                </div>
            </div>
            <div class="stat-row">
                <div class="stat-card">
                    <div class="stat-label">P/E Ratio</div>
                    <div class="stat-value" style="font-size:14px">{f"{d['pe']:.1f}" if d['pe'] else 'N/A'}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Beta</div>
                    <div class="stat-value" style="font-size:14px">{f"{d['beta']:.2f}" if d['beta'] else 'N/A'}</div>
                </div>
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(255,255,255,0.25);margin-top:6px;">
                🏢 Sector: {d['sector']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with left:
        render_card(d1, clr1, sign1, "#00ff8c")
    with right:
        render_card(d2, clr2, sign2, "#4da6ff")

    # ── Head to Head Table ──
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Head to Head Summary</div>", unsafe_allow_html=True)

    def winner(v1, v2, higher_is_better=True):
        if v1 is None or v2 is None: return "—", "—"
        return ("✅", "—") if (v1 > v2) == higher_is_better else ("—", "✅")

    rows = [
        ("Daily % Change", f"{sign1}{d1['pct']:.2f}%", f"{sign2}{d2['pct']:.2f}%", winner(d1["pct"], d2["pct"])),
        ("Market Cap",     fmt_mktcap(d1['mktcap']),   fmt_mktcap(d2['mktcap']),   winner(d1["mktcap"], d2["mktcap"])),
        ("Volume",         fmt_volume(d1['volume']),   fmt_volume(d2['volume']),   winner(d1["volume"], d2["volume"])),
        ("P/E Ratio",      f"{d1['pe']:.1f}" if d1['pe'] else "N/A", f"{d2['pe']:.1f}" if d2['pe'] else "N/A", winner(d1["pe"], d2["pe"], higher_is_better=False)),
        ("Beta (Risk)",    f"{d1['beta']:.2f}" if d1['beta'] else "N/A", f"{d2['beta']:.2f}" if d2['beta'] else "N/A", winner(d1["beta"], d2["beta"], higher_is_better=False)),
    ]

    table = f"""
    <table style="width:100%;border-collapse:collapse;font-family:'Space Mono',monospace;font-size:12px;">
        <thead>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.08);">
                <th style="text-align:left;padding:10px 8px;color:rgba(255,255,255,0.25);
                           font-size:9px;letter-spacing:2px;font-weight:400;">METRIC</th>
                <th style="text-align:center;padding:10px 8px;color:#00ff8c;font-size:12px;">{d1['ticker']}</th>
                <th style="text-align:center;padding:10px 8px;color:#4da6ff;font-size:12px;">{d2['ticker']}</th>
            </tr>
        </thead><tbody>
    """
    for label, v1, v2, (w1, w2) in rows:
        table += f"""
            <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                <td style="padding:10px 8px;color:rgba(255,255,255,0.4);">{label}</td>
                <td style="text-align:center;padding:10px 8px;color:#e0f0e0;">{v1} {w1}</td>
                <td style="text-align:center;padding:10px 8px;color:#e0f0e0;">{v2} {w2}</td>
            </tr>"""
    table += "</tbody></table>"
    st.markdown(table, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Volume Chart ──
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Volume Comparison (6 Months)</div>", unsafe_allow_html=True)
    st.plotly_chart(build_volume_chart(d1, d2), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="output-empty">
        <div style="font-size:56px;opacity:0.2;">📊</div>
        <div style="font-size:14px;">Enter two stock tickers above and click
            <b style='color:rgba(0,255,140,0.5)'>Compare Now</b>
        </div>
        <div style="font-size:10px;opacity:0.4;margin-top:4px;">
            e.g. TSLA vs AAPL &nbsp;·&nbsp; NVDA vs AMD &nbsp;·&nbsp; MSFT vs GOOGL
        </div>
    </div>
    """, unsafe_allow_html=True)
