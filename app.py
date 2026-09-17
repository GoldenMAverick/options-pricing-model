"""
Options Pricing Model — Streamlit Dashboard
Black-Scholes pricer with Greeks, Implied Volatility, and interactive charts.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

from pricing.black_scholes import black_scholes, greeks, implied_vol, price_surface

# ──────────────────────────────────────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Options Pricing Model",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import premium font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Page background */
    .stApp {
        background: linear-gradient(135deg, #0D1B2A 0%, #0f2035 50%, #091624 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111f2e 0%, #0a1828 100%);
        border-right: 1px solid #1e3448;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a2a3a 0%, #162030 100%);
        border: 1px solid #1e3a50;
        border-radius: 12px;
        padding: 16px !important;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.15);
    }
    [data-testid="metric-container"] label {
        color: #7fb3cc !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #00D4FF !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }

    /* Divider */
    hr { border-color: #1e3448 !important; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #111f2e;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid #1e3448;
    }
    .stTabs [data-baseweb="tab"] {
        color: #7fb3cc;
        border-radius: 8px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00D4FF22, #0099bb22) !important;
        color: #00D4FF !important;
        border: 1px solid #00D4FF44 !important;
    }

    /* Slider accent */
    [data-testid="stSlider"] > div > div > div > div {
        background: linear-gradient(90deg, #00D4FF, #0099bb) !important;
    }

    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #00D4FF;
        letter-spacing: 0.03em;
        margin-bottom: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid #1e3448;
    }

    /* Greek badge */
    .greek-positive { color: #00e676; font-weight: 600; }
    .greek-negative { color: #ff5252; font-weight: 600; }

    /* Info box */
    .info-box {
        background: #111f2e;
        border-left: 3px solid #00D4FF;
        border-radius: 4px;
        padding: 10px 14px;
        margin: 8px 0;
        font-size: 0.85rem;
        color: #b0cfe0;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# Colour palette
# ──────────────────────────────────────────────────────────────────────────────
BG      = "#0D1B2A"
BG2     = "#1a2a3a"
CYAN    = "#00D4FF"
ACCENT  = "#FFB347"
GREEN   = "#00e676"
RED     = "#ff5252"
BORDER  = "#1e3448"
GRID    = "#1a2f40"
TEXT    = "#E8F4FD"
MUTED   = "#7fb3cc"

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=BG,
    font=dict(family="Inter, sans-serif", color=TEXT),
    xaxis=dict(gridcolor=GRID, linecolor=BORDER, tickfont=dict(color=MUTED)),
    yaxis=dict(gridcolor=GRID, linecolor=BORDER, tickfont=dict(color=MUTED)),
    margin=dict(l=50, r=30, t=50, b=50),
    legend=dict(bgcolor=BG2, bordercolor=BORDER, borderwidth=1, font=dict(color=TEXT)),
    hoverlabel=dict(bgcolor=BG2, bordercolor=CYAN, font=dict(color=TEXT)),
)
VOL_COLOURS = [CYAN, "#7B68EE", GREEN, ACCENT]


# ──────────────────────────────────────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0d1f30 0%, #162a40 100%);
    border: 1px solid #1e3a50;
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
">
    <h1 style="
        margin: 0 0 8px 0;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00D4FF, #7B68EE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    ">📈 Options Pricing Model</h1>
    <p style="margin: 0; color: #7fb3cc; font-size: 1rem;">
        Black-Scholes pricing engine · Option Greeks · Implied Volatility solver · Interactive stress tests
    </p>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# Sidebar — Parameters
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-header">⚙️ Model Parameters</div>', unsafe_allow_html=True)

    option_type = st.radio(
        "Option Type", ["Call", "Put"], horizontal=True,
        help="European call or put option"
    ).lower()

    st.markdown("---")
    st.markdown("**Market Inputs**")
    S     = st.slider("Underlying Price (S)", 50.0, 500.0, 100.0, 0.5,
                      help="Current price of the underlying asset")
    K     = st.slider("Strike Price (K)", 50.0, 500.0, 100.0, 0.5,
                      help="The agreed exercise price")
    T     = st.slider("Time to Expiry (T, years)", 0.01, 3.0, 1.0, 0.01,
                      help="Years until option expiry")
    r     = st.slider("Risk-Free Rate (r, %)", 0.0, 15.0, 5.0, 0.1,
                      help="Continuously compounded annualised rate") / 100
    sigma = st.slider("Volatility (σ, %)", 1.0, 100.0, 20.0, 0.5,
                      help="Annualised implied/historical volatility") / 100

    st.markdown("---")
    st.markdown("**Implied Volatility**")
    market_price_input = st.number_input(
        "Market Price (for IV)",
        min_value=0.01,
        value=round(black_scholes(S, K, T, r, sigma, option_type) * 1.1, 4),
        step=0.01,
        format="%.4f",
        help="Enter an observed market price to back-solve for implied volatility"
    )

    st.markdown("---")
    st.markdown('<div style="color: #7fb3cc; font-size: 0.78rem; text-align: center;">Black-Scholes Model · Continuous Dividend = 0</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# Compute results
# ──────────────────────────────────────────────────────────────────────────────
price   = black_scholes(S, K, T, r, sigma, option_type)
g       = greeks(S, K, T, r, sigma, option_type)
iv      = implied_vol(market_price_input, S, K, T, r, option_type)
moneyness = "ATM" if abs(S - K) < 0.5 else ("ITM" if (S > K and option_type == "call") or (S < K and option_type == "put") else "OTM")


# ──────────────────────────────────────────────────────────────────────────────
# Metric cards row
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="section-header">💰 Pricing & Greeks — {option_type.upper()} @ {moneyness}</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
with c1: st.metric("Option Price", f"${price:.4f}")
with c2: st.metric("Delta (Δ)", f"{g['delta']:+.4f}",
                   delta=f"{'≈ Δ hedge'}" if abs(g['delta']) > 0.4 else "")
with c3: st.metric("Gamma (Γ)", f"{g['gamma']:.5f}")
with c4: st.metric("Vega (ν)", f"{g['vega']:.4f}", help="Per 1% vol change")
with c5: st.metric("Theta (Θ)", f"{g['theta']:+.4f}", help="Per calendar day")
with c6: st.metric("Rho (ρ)", f"{g['rho']:+.4f}", help="Per 1% rate change")
with c7:
    if iv is not None:
        st.metric("Implied Vol", f"{iv:.2%}")
    else:
        st.metric("Implied Vol", "N/A")

st.markdown("---")

# ──────────────────────────────────────────────────────────────────────────────
# Tabs
# ──────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Price Sensitivity",
    "🔺 Greeks Curves",
    "🌡️ Heatmaps",
    "💹 P&L Payoff",
    "📋 IV & Data Table",
])


# ─── Tab 1: Price Sensitivity ────────────────────────────────────────────────
with tab1:
    st.markdown("#### Call/Put Price vs Underlying — Volatility Stress Test")
    col_l, col_r = st.columns(2)

    underliers = np.linspace(max(5, S * 0.4), S * 1.6, 300)
    vols = [0.10, 0.20, 0.30, 0.40]

    # Price sensitivity
    fig1 = go.Figure()
    for i, vol in enumerate(vols):
        prices = [black_scholes(s, K, T, r, vol, option_type) for s in underliers]
        fig1.add_trace(go.Scatter(
            x=underliers, y=prices,
            mode="lines",
            name=f"σ = {vol:.0%}",
            line=dict(color=VOL_COLOURS[i], width=2.5),
            hovertemplate="S: $%{x:.1f}<br>Price: $%{y:.4f}<extra>σ=%{fullData.name}</extra>",
        ))
    fig1.add_vline(x=K, line_dash="dash", line_color="white", opacity=0.4,
                   annotation_text=f"K={K}", annotation_font_color="white")
    fig1.add_vline(x=S, line_dash="dot", line_color=CYAN, opacity=0.6,
                   annotation_text=f"S={S}", annotation_font_color=CYAN)
    fig1.update_layout(**PLOT_LAYOUT,
        title=dict(text=f"{option_type.capitalize()} Price vs Underlying", font=dict(color=TEXT, size=15)),
        xaxis_title="Underlying Price ($)", yaxis_title="Option Price ($)",
        height=420,
    )
    col_l.plotly_chart(fig1, use_container_width=True)

    # Time decay
    fig2 = go.Figure()
    times = [1.5, 1.0, 0.5, 0.25, 0.083]
    time_colours = [ACCENT, CYAN, "#7B68EE", GREEN, RED]
    for i, t in enumerate(times):
        prices = [black_scholes(s, K, t, r, sigma, option_type) for s in underliers]
        fig2.add_trace(go.Scatter(
            x=underliers, y=prices,
            mode="lines",
            name=f"T={t:.3g}y",
            line=dict(color=time_colours[i], width=2),
            hovertemplate="S: $%{x:.1f}<br>Price: $%{y:.4f}<extra>%{fullData.name}</extra>",
        ))
    fig2.add_vline(x=K, line_dash="dash", line_color="white", opacity=0.4)
    fig2.add_vline(x=S, line_dash="dot", line_color=CYAN, opacity=0.6)
    fig2.update_layout(**PLOT_LAYOUT,
        title=dict(text="Time Decay (Theta) Effect", font=dict(color=TEXT, size=15)),
        xaxis_title="Underlying Price ($)", yaxis_title="Option Price ($)",
        height=420,
    )
    col_r.plotly_chart(fig2, use_container_width=True)


# ─── Tab 2: Greeks Curves ─────────────────────────────────────────────────────
with tab2:
    st.markdown("#### Greek Profiles vs Underlying Price")

    S_range = np.linspace(max(5, S * 0.4), S * 1.6, 300)
    greek_names = ["delta", "gamma", "vega", "theta", "rho"]
    greek_colours = [CYAN, ACCENT, GREEN, RED, "#7B68EE"]
    greek_labels = ["Delta (Δ)", "Gamma (Γ)", "Vega (ν)", "Theta (Θ)", "Rho (ρ)"]
    greek_hints  = ["Sensitivity to price", "Rate of delta change",
                    "Per 1% vol move", "Per calendar day", "Per 1% rate move"]

    fig_g = make_subplots(
        rows=2, cols=3,
        subplot_titles=greek_labels[:5] + [""],
        vertical_spacing=0.14, horizontal_spacing=0.08,
    )
    positions = [(1,1),(1,2),(1,3),(2,1),(2,2)]
    for idx, (gk, col, hint, pos) in enumerate(zip(greek_names, greek_colours, greek_hints, positions)):
        vals = [greeks(s, K, T, r, sigma, option_type)[gk] for s in S_range]
        fig_g.add_trace(go.Scatter(
            x=S_range, y=vals,
            mode="lines",
            name=greek_labels[idx],
            line=dict(color=col, width=2.5),
            showlegend=False,
            hovertemplate=f"S: $%{{x:.1f}}<br>{greek_labels[idx]}: %{{y:.5f}}<extra></extra>",
        ), row=pos[0], col=pos[1])
        fig_g.add_vline(x=K, line_dash="dash", line_color="white", opacity=0.3, row=pos[0], col=pos[1])
        fig_g.add_vline(x=S, line_dash="dot",  line_color=CYAN,  opacity=0.4, row=pos[0], col=pos[1])

    fig_g.update_layout(
        **PLOT_LAYOUT,
        height=580,
        title=dict(text=f"Option Greeks — {option_type.capitalize()}", font=dict(color=TEXT, size=16)),
    )
    # Update subplot axis colours
    for axis in fig_g.layout:
        if axis.startswith(("xaxis", "yaxis")):
            fig_g.layout[axis].update(gridcolor=GRID, linecolor=BORDER)

    st.plotly_chart(fig_g, use_container_width=True)

    # Greek summary table
    st.markdown("#### Greek Breakdown at Current Parameters")
    greek_df = pd.DataFrame({
        "Greek": greek_labels,
        "Symbol": ["Δ", "Γ", "ν", "Θ", "ρ"],
        "Value": [g[k] for k in greek_names],
        "Interpretation": greek_hints,
        "Unit": ["per $1 in S", "per $1 in Δ", "per 1% vol", "per day", "per 1% rate"],
    })
    st.dataframe(
        greek_df.style
            .format({"Value": "{:+.6f}"})
            .applymap(lambda v: f"color: {GREEN}" if isinstance(v, float) and v > 0
                      else (f"color: {RED}" if isinstance(v, float) and v < 0 else ""),
                      subset=["Value"])
            .set_properties(**{"background-color": BG2, "color": TEXT}),
        use_container_width=True, hide_index=True,
    )


# ─── Tab 3: Heatmaps ──────────────────────────────────────────────────────────
with tab3:
    st.markdown("#### Option Price Heatmap — Underlying vs Volatility")
    col_h1, col_h2 = st.columns(2)

    # Price heatmap: S vs sigma
    S_vals    = np.linspace(max(5, S * 0.5), S * 1.5, 40)
    sigma_vals = np.linspace(0.05, 0.60, 40)
    Z = np.array([[black_scholes(s, K, T, r, sig, option_type)
                   for sig in sigma_vals] for s in S_vals])

    fig_h1 = go.Figure(go.Heatmap(
        x=sigma_vals * 100, y=S_vals, z=Z,
        colorscale=[[0, "#0D1B2A"], [0.3, "#004466"], [0.7, "#0099BB"], [1, CYAN]],
        colorbar=dict(title="Price ($)", tickfont=dict(color=TEXT), titlefont=dict(color=TEXT)),
        hovertemplate="σ: %{x:.1f}%<br>S: $%{y:.1f}<br>Price: $%{z:.3f}<extra></extra>",
    ))
    fig_h1.add_hline(y=S, line_color=CYAN, line_dash="dash",
                     annotation_text="Current S", annotation_font_color=CYAN)
    fig_h1.update_layout(**PLOT_LAYOUT,
        title=dict(text=f"{option_type.capitalize()} Price: S vs σ", font=dict(color=TEXT, size=15)),
        xaxis_title="Volatility σ (%)", yaxis_title="Underlying Price ($)",
        height=420,
    )
    col_h1.plotly_chart(fig_h1, use_container_width=True)

    # Delta heatmap: S vs T
    T_vals = np.linspace(0.05, 2.0, 40)
    Z2 = np.array([[greeks(s, K, t, r, sigma, option_type)["delta"]
                    for t in T_vals] for s in S_vals])
    fig_h2 = go.Figure(go.Heatmap(
        x=T_vals, y=S_vals, z=Z2,
        colorscale=[[0, "#330033"], [0.5, "#004466"], [1, CYAN]],
        colorbar=dict(title="Delta", tickfont=dict(color=TEXT), titlefont=dict(color=TEXT)),
        hovertemplate="T: %{x:.2f}y<br>S: $%{y:.1f}<br>Δ: %{z:.4f}<extra></extra>",
    ))
    fig_h2.add_hline(y=S, line_color=CYAN, line_dash="dash",
                     annotation_text="Current S", annotation_font_color=CYAN)
    fig_h2.update_layout(**PLOT_LAYOUT,
        title=dict(text="Delta: S vs Time to Expiry", font=dict(color=TEXT, size=15)),
        xaxis_title="Time to Expiry (years)", yaxis_title="Underlying Price ($)",
        height=420,
    )
    col_h2.plotly_chart(fig_h2, use_container_width=True)


# ─── Tab 4: P&L Payoff ───────────────────────────────────────────────────────
with tab4:
    st.markdown("#### P&L Payoff Diagram")

    premium_paid = price
    S_payoff = np.linspace(max(1, K * 0.5), K * 1.5, 400)

    if option_type == "call":
        intrinsic = np.maximum(S_payoff - K, 0)
    else:
        intrinsic = np.maximum(K - S_payoff, 0)

    pnl_long  = intrinsic - premium_paid
    pnl_short = premium_paid - intrinsic

    fig_p = go.Figure()

    # Long position
    fig_p.add_trace(go.Scatter(
        x=S_payoff, y=pnl_long, mode="lines",
        name=f"Long {option_type.capitalize()}",
        line=dict(color=CYAN, width=3),
        fill="tozeroy",
        fillcolor="rgba(0,212,255,0.06)",
        hovertemplate="S: $%{x:.1f}<br>P&L: $%{y:.2f}<extra>Long</extra>",
    ))

    # Short position
    fig_p.add_trace(go.Scatter(
        x=S_payoff, y=pnl_short, mode="lines",
        name=f"Short {option_type.capitalize()}",
        line=dict(color=ACCENT, width=2, dash="dash"),
        hovertemplate="S: $%{x:.1f}<br>P&L: $%{y:.2f}<extra>Short</extra>",
    ))

    # Break-even
    if option_type == "call":
        breakeven = K + premium_paid
    else:
        breakeven = K - premium_paid

    fig_p.add_vline(x=K, line_color="white", line_dash="dash", opacity=0.4,
                    annotation_text=f"K={K}", annotation_font_color="white")
    fig_p.add_vline(x=S, line_color=CYAN, line_dash="dot", opacity=0.5,
                    annotation_text=f"S={S}", annotation_font_color=CYAN)
    fig_p.add_hline(y=0, line_color="white", opacity=0.3)
    fig_p.add_vline(x=breakeven, line_color=GREEN, line_dash="dot", opacity=0.7,
                    annotation_text=f"B/E={breakeven:.2f}", annotation_font_color=GREEN)

    fig_p.update_layout(**PLOT_LAYOUT,
        title=dict(text=f"P&L at Expiry — {option_type.capitalize()} (Premium: ${premium_paid:.4f})",
                   font=dict(color=TEXT, size=15)),
        xaxis_title="Underlying Price at Expiry ($)",
        yaxis_title="Profit / Loss ($)",
        height=480,
    )
    st.plotly_chart(fig_p, use_container_width=True)

    col_be1, col_be2, col_be3, col_be4 = st.columns(4)
    col_be1.metric("Premium Paid", f"${premium_paid:.4f}")
    col_be2.metric("Break-even", f"${breakeven:.2f}")
    max_profit = "Unlimited" if option_type == "call" else f"${K - premium_paid:.2f}"
    max_loss   = f"${premium_paid:.4f}"
    col_be3.metric("Max Profit", max_profit)
    col_be4.metric("Max Loss (Long)", max_loss)


# ─── Tab 5: IV & Data Table ───────────────────────────────────────────────────
with tab5:
    st.markdown("#### Implied Volatility Solver")
    col_iv1, col_iv2 = st.columns([2, 1])
    with col_iv1:
        st.markdown(f"""
        <div class="info-box">
            <b>Inputs:</b> Market Price = <code>${market_price_input:.4f}</code> &nbsp;|&nbsp;
            S = <code>{S}</code> &nbsp;|&nbsp; K = <code>{K}</code> &nbsp;|&nbsp;
            T = <code>{T:.2f}y</code> &nbsp;|&nbsp; r = <code>{r:.2%}</code><br><br>
            <b>Model Price at σ=20%:</b> <code>${black_scholes(S, K, T, r, 0.20, option_type):.4f}</code><br>
            <b>Solved Implied Vol:</b> <code>{"N/A" if iv is None else f"{iv:.4%}"}</code><br>
            <b>Algorithm:</b> Newton-Raphson (max 200 iterations, tol=1e-6)
        </div>
        """, unsafe_allow_html=True)

    with col_iv2:
        if iv is not None:
            st.metric("✅ Implied Volatility", f"{iv:.2%}")
        else:
            st.warning("IV solver did not converge. Check that market price is valid.")

    st.markdown("#### Stress Test — Price Table across Volatilities & Strikes")

    strike_range = np.linspace(K * 0.8, K * 1.2, 9)
    vol_range    = [0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
    table_data = {"Strike": [f"${k:.1f}" for k in strike_range]}
    for vol in vol_range:
        table_data[f"σ={vol:.0%}"] = [
            f"${black_scholes(S, k, T, r, vol, option_type):.4f}" for k in strike_range
        ]
    df = pd.DataFrame(table_data)
    st.dataframe(
        df.style.set_properties(**{"background-color": BG2, "color": TEXT}),
        use_container_width=True, hide_index=True,
    )

    st.markdown("#### Full Greeks at Current Parameters")
    summary_df = pd.DataFrame([{
        "Parameter": "S (Underlying)",   "Value": f"${S:.2f}"},
        {"Parameter": "K (Strike)",      "Value": f"${K:.2f}"},
        {"Parameter": "T (Expiry)",      "Value": f"{T:.3f} years"},
        {"Parameter": "r (Risk-free)",   "Value": f"{r:.2%}"},
        {"Parameter": "σ (Volatility)",  "Value": f"{sigma:.2%}"},
        {"Parameter": "Option Type",     "Value": option_type.capitalize()},
        {"Parameter": "Moneyness",       "Value": moneyness},
        {"Parameter": "Price",           "Value": f"${price:.6f}"},
        {"Parameter": "Delta",           "Value": f"{g['delta']:+.6f}"},
        {"Parameter": "Gamma",           "Value": f"{g['gamma']:.6f}"},
        {"Parameter": "Vega",            "Value": f"{g['vega']:.6f}"},
        {"Parameter": "Theta",           "Value": f"{g['theta']:+.6f}"},
        {"Parameter": "Rho",             "Value": f"{g['rho']:+.6f}"},
        {"Parameter": "Implied Vol",     "Value": f"{iv:.4%}" if iv else "N/A"},
    ])
    st.dataframe(
        summary_df.style.set_properties(**{"background-color": BG2, "color": TEXT}),
        use_container_width=True, hide_index=True,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #4a6a7a; font-size: 0.8rem; padding: 12px 0;">
    Built with ❤️ using <b>Streamlit</b> &amp; <b>Plotly</b> &nbsp;·&nbsp;
    Black-Scholes model assumes European options, no dividends, constant volatility &amp; risk-free rate<br>
    <span style="color: #ff9800;">⚠️ For educational purposes only — not financial advice</span>
</div>
""", unsafe_allow_html=True)
