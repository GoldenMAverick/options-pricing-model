#!/bin/bash
# ────────────────────────────────────────────────────────────
# setup_and_deploy.sh
# Run this script to install deps, push to GitHub, and get
# the Streamlit Community Cloud deployment link.
# ────────────────────────────────────────────────────────────
set -e

REPO_NAME="options-pricing-model"
GITHUB_USER="GoldenMAverick"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║       Options Pricing Model — Setup & Deploy         ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ── 1. Python venv + dependencies ─────────────────────────
echo "📦 Step 1: Creating virtual environment..."
cd "$PROJECT_DIR"
python3 -m venv .venv
source .venv/bin/activate
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed."
echo ""

# ── 2. Quick sanity check ─────────────────────────────────
echo "🧪 Step 2: Running sanity check..."
python3 - << 'EOF'
from pricing.black_scholes import black_scholes, greeks, implied_vol
price = black_scholes(100, 100, 1.0, 0.05, 0.20)
g     = greeks(100, 100, 1.0, 0.05, 0.20)
iv    = implied_vol(price * 1.1, 100, 100, 1.0, 0.05)
print(f"  Call Price : ${price:.4f}")
print(f"  Delta      : {g['delta']:.4f}")
print(f"  Gamma      : {g['gamma']:.5f}")
print(f"  Vega       : {g['vega']:.4f}")
print(f"  Theta      : {g['theta']:.4f}")
print(f"  Rho        : {g['rho']:.4f}")
print(f"  Implied Vol: {iv:.2%}")
EOF
echo "✅ Sanity check passed."
echo ""

# ── 3. Git init + commit ───────────────────────────────────
echo "🔧 Step 3: Initialising Git repository..."
git init
git add -A
git commit -m "feat: initial commit — Black-Scholes Options Pricing Model

- Black-Scholes pricing for European calls & puts
- All 5 Greeks (Delta, Gamma, Vega, Theta, Rho)
- Newton-Raphson Implied Volatility solver
- Streamlit dashboard with 5 interactive tabs
- Plotly dark-themed charts + heatmaps
- P&L payoff diagram with break-even line
- Stress-test price table across strikes & vols"

echo "✅ Git commit done."
echo ""

# ── 4. Push to GitHub ─────────────────────────────────────
echo "🐙 Step 4: Creating GitHub repository & pushing..."

# Try GitHub CLI first, fall back to git remote
if command -v gh &>/dev/null; then
    gh repo create "$GITHUB_USER/$REPO_NAME" \
        --public \
        --description "Interactive Black-Scholes Options Pricing Model — Greeks, IV solver, stress tests" \
        --source . \
        --remote origin \
        --push
    echo "✅ Pushed via GitHub CLI."
else
    echo ""
    echo "  ⚠️  GitHub CLI (gh) not found."
    echo "  Please run these commands manually:"
    echo ""
    echo "  1. Go to https://github.com/new"
    echo "  2. Create a repo named: $REPO_NAME (public)"
    echo "  3. Then run:"
    echo ""
    echo "     git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git"
    echo "     git branch -M main"
    echo "     git push -u origin main"
    echo ""
fi

# ── 5. Deployment instructions ────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║        🚀 Deploy to Streamlit Community Cloud        ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "  1. Go to: https://share.streamlit.io"
echo "  2. Sign in with GitHub"
echo "  3. Click 'New app'"
echo "  4. Fill in:"
echo "       Repository : $GITHUB_USER/$REPO_NAME"
echo "       Branch     : main"
echo "       Main file  : app.py"
echo "  5. Click 'Deploy!'"
echo ""
echo "  Your app will be live at:"
echo "  🌐 https://$REPO_NAME.streamlit.app"
echo ""
echo "  ────────────────────────────────────────────────────"
echo "  Or run locally:"
echo "  streamlit run app.py"
echo "  ────────────────────────────────────────────────────"
echo ""
echo "✅ All done! Happy trading 📈"
