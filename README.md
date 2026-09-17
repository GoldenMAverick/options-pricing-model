# 📈 Options Pricing Model

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://options-pricing-model.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> An interactive **Black-Scholes options pricing dashboard** built with Streamlit and Plotly.  
> Price European options, compute all 5 Greeks, solve for implied volatility, and run stress tests — all in your browser.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧮 **Black-Scholes Pricing** | Closed-form price for European calls & puts |
| 🔺 **Option Greeks** | Delta, Gamma, Vega, Theta, Rho — from first principles |
| 🔍 **Implied Volatility** | Newton-Raphson IV solver from market price |
| 📊 **Price Sensitivity** | Interactive vol stress-test & time-decay charts |
| 🌡️ **Heatmaps** | 2D price & delta surfaces across S × σ and S × T |
| 💹 **P&L Payoff** | Long/short payoff diagram with break-even line |
| 📋 **Stress Table** | Price matrix across strikes × volatilities |

---

## 🚀 Live Demo

**[🌐 Open the app →](https://options-pricing-model.streamlit.app)**

---

## 🛠️ Local Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/GoldenMAverick/options-pricing-model.git
cd options-pricing-model

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 📁 Project Structure

```
options-pricing-model/
├── app.py                    # Main Streamlit dashboard (5 tabs)
├── pricing/
│   ├── __init__.py
│   └── black_scholes.py      # BS formula, Greeks, IV solver, price_surface
├── .streamlit/
│   └── config.toml           # Dark theme config (#0D1B2A palette)
├── requirements.txt
└── README.md
```

---

## 📐 Model Details

### Black-Scholes Formula

For a European **call** option:

$$C = S \cdot N(d_1) - K e^{-rT} N(d_2)$$

For a European **put** option:

$$P = K e^{-rT} N(-d_2) - S \cdot N(-d_1)$$

Where:

$$d_1 = \frac{\ln(S/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$$

### Greeks

| Greek | Formula | Meaning |
|---|---|---|
| **Delta (Δ)** | $N(d_1)$ | Price sensitivity to underlying |
| **Gamma (Γ)** | $\frac{N'(d_1)}{S\sigma\sqrt{T}}$ | Rate of delta change |
| **Vega (ν)** | $S N'(d_1) \sqrt{T}$ | Sensitivity to volatility |
| **Theta (Θ)** | $-\frac{S N'(d_1)\sigma}{2\sqrt{T}} - rKe^{-rT}N(d_2)$ | Time decay per day |
| **Rho (ρ)** | $KTe^{-rT}N(d_2)$ | Sensitivity to interest rate |

### Implied Volatility

Newton-Raphson iteration:

$$\sigma_{n+1} = \sigma_n - \frac{C_{BS}(\sigma_n) - C_{mkt}}{\mathcal{V}(\sigma_n)}$$

---

## ⚠️ Disclaimer

This tool is **for educational purposes only**. It does not constitute financial advice.  
The Black-Scholes model assumes:
- European-style options (no early exercise)
- No dividends
- Constant volatility and risk-free rate
- Continuous trading with no transaction costs

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

*Built with [Streamlit](https://streamlit.io) · [Plotly](https://plotly.com) · [SciPy](https://scipy.org)*
