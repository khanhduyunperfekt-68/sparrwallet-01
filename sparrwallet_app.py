# sparrwallet_app.py
# SparrWallet - Finance Dashboard (Streamlit, 1-file, fundamentals)
# Features:
# - Income + fixed costs
# - Daily variable expenses (per day, alerts 15%/day & 90%/month)
# - Safe zone suggestion (>20% remaining) → Actions: Stocks/ETF, Crypto, Save 3m@3.6%
# - Progress bar, metrics, daily table, logs, build summary, save summary.txt

import streamlit as st
from datetime import date, timedelta
import os

# ---------------- CONFIG ----------------
DAILY_ALERT_RATIO    = 0.15      # daily spend > 15% income
MONTHLY_ALERT_RATIO  = 0.90      # total spent > 90% income
SAFE_REMAINING_RATIO = 0.20      # suggest actions when remaining > 20% income
SAVINGS_RATE_3M      = 0.036     # flat interest for the 3-month term

# ------------- SMALL HELPERS -----------
def add_months_safe(d: date, months: int) -> date:
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    try:
        return date(y, m, d.day)
    except ValueError:
        # clamp to last day of month
        if m == 12:
            ny, nm = y + 1, 1
        else:
            ny, nm = y, m + 1
        first_next = date(ny, nm, 1)
        return first_next - timedelta(days=1)

def fmt(d: date) -> str:
    return f"{d.day:02d}/{d.month:02d}/{d.year}"

def get_state():
    ss = st.session_state
    # initialize once
    ss.setdefault("income", 0.0)
    ss.setdefault("fixed", 0.0)
    ss.setdefault("variable_total", 0.0)
    ss.setdefault("day_totals", {})      # {day:int -> amount:float}
    ss.setdefault("investments", [])     # [{day, kind, amount}]
    ss.setdefault("savings", [])         # [{day, amount, interest, maturity, mat_date}]
    ss.setdefault("log", [])
    return ss

def remaining_amount(ss) -> float:
    inv = sum(x["amount"] for x in ss.investments)
    sav = sum(x["amount"] for x in ss.savings)
    spent = ss.fixed + ss.variable_total + inv + sav
    return ss.income - spent

# ----------------- UI -------------------
st.set_page_config(page_title="SparrWallet Dashboard", page_icon="💎", layout="wide")

# Header with optional logo
col_logo, col_title = st.columns([1, 5])
with col_logo:
    logo_path = os.path.join(os.path.dirname(__file__), "sparr_logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=72)
    else:
        st.markdown("### 💎")
with col_title:
    st.markdown("## **SparrWallet – Finance Dashboard**")
    st.caption(f"Today: {fmt(date.today())}")

ss = get_state()

# Sidebar: Budget setup
st.sidebar.header("Budget")
ss.income = st.sidebar.number_input("Monthly income", min_value=0.0, step=100.0, value=float(ss.income))
ss.fixed  = st.sidebar.number_input("Fixed costs",    min_value=0.0, step=50.0,  value=float(ss.fixed))

if st.sidebar.button("Initialize / Reset"):
    ss.variable_total = 0.0
    ss.day_totals = {}
    ss.investments = []
    ss.savings = []
    ss.log = ["Initialized budget."]
    st.sidebar.success("Budget initialized.")

st.sidebar.divider()

# Main 3 columns: metrics, gauge, add expense
c1, c2, c3 = st.columns([1,1,1])

with c1:
    rem = remaining_amount(ss)
    total_spent_now = ss.income - rem
    st.metric("Remaining", f"{rem:,.2f}")
    st.metric("Total spent so far", f"{total_spent_now:,.2f}")

with c2:
    pct = 0 if ss.income <= 0 else max(min(rem / ss.income, 1), 0)
    st.write("**Remaining ratio**")
    st.progress(pct)  # Streamlit progress bar (0..1)
    if total_spent_now > ss.income * MONTHLY_ALERT_RATIO:
        st.error("Warning: You used more than 90% of monthly income.")
    else:
        st.info("Tracking normally.")

with c3:
    st.write("**Add variable expense**")
    amt = st.number_input("Amount", min_value=0.0, step=10.0, key="var_amt")
    day = st.number_input("Day (1-31, blank=auto today)", min_value=1, max_value=31, value=date.today().day, step=1, key="var_day")
    if st.button("Add expense"):
        ss.day_totals[day] = ss.day_totals.get(day, 0.0) + float(amt)
        ss.variable_total += float(amt)
        ss.log.append(f"+ {amt:.2f} on day {day} | variable_total={ss.variable_total:.2f}")
        # alerts
        if ss.day_totals[day] > ss.income * DAILY_ALERT_RATIO:
            st.warning(f"Daily alert: day {day} > {int(DAILY_ALERT_RATIO*100)}% of income.")
        st.success("Expense added.")

st.divider()

# Safe zone suggestion + Actions
safe = (ss.income > 0 and remaining_amount(ss) > ss.income * SAFE_REMAINING_RATIO)
if safe:
    st.success("💡 You have a healthy remaining amount → consider investing or saving.")
    ac1, ac2, ac3 = st.columns([2,2,1])
    with ac1:
        action = st.radio("Action", ["Invest: Stocks/ETF", "Invest: Crypto (BTC/ETH)", "Save 3 months @ 3.6%"], horizontal=False)
    with ac2:
        action_amt = st.number_input("Action amount", min_value=0.0, step=10.0, key="act_amt")
    with ac3:
        if st.button("Perform action"):
            amt_ok = action_amt > 0 and action_amt <= remaining_amount(ss)
            if not amt_ok:
                st.error(f"Amount must be > 0 and ≤ remaining ({remaining_amount(ss):.2f}).")
            else:
                d = date.today().day
                if action.startswith("Invest"):
                    kind = "STOCKS/ETF" if "Stocks" in action else "CRYPTO (BTC/ETH)"
                    ss.investments.append({"day": d, "kind": kind, "amount": float(action_amt)})
                    ss.log.append(f"Invested {kind} {action_amt:.2f} on day {d}")
                    st.success("Invested successfully.")
                else:
                    interest = float(action_amt) * SAVINGS_RATE_3M
                    maturity = float(action_amt) + interest
                    mat_date = add_months_safe(date.today(), 3)
                    ss.savings.append({
                        "day": d, "amount": float(action_amt),
                        "interest": interest, "maturity": maturity, "mat_date": mat_date
                    })
                    ss.log.append(f"Saved {action_amt:.2f}; maturity {maturity:.2f} on {fmt(mat_date)}")
                    st.info(f"Saved. 3m interest: {interest:.2f}; maturity {maturity:.2f} on {fmt(mat_date)}")
else:
    st.warning("Not in safe zone yet (need > 20% of income remaining).")

st.divider()

# Two columns: daily table & summary/log
left, right = st.columns([2,2])

with left:
    st.subheader("Daily expenses")
    if ss.day_totals:
        st.table({"Day": list(sorted(ss.day_totals.keys())),
                  "Amount": [ss.day_totals[d] for d in sorted(ss.day_totals.keys())]})
    else:
        st.caption("No variable expenses yet.")

with right:
    st.subheader("Summary")
    inv_total = sum(x["amount"] for x in ss.investments)
    sav_total_principal = sum(x["amount"] for x in ss.savings)
    sav_total_interest  = sum(x["interest"] for x in ss.savings)
    rem = remaining_amount(ss)

    st.markdown(f"""
- **Income:** {ss.income:,.2f}  
- **Fixed costs:** {ss.fixed:,.2f}  
- **Variable costs:** {ss.variable_total:,.2f}  
- **Invested (total):** {inv_total:,.2f}  
- **Saved principal (total):** {sav_total_principal:,.2f}  
- **Projected savings interest (3m):** {sav_total_interest:,.2f}  
- **Remaining:** {rem:,.2f}
""")

    if ss.investments:
        st.markdown("**Investments**")
        st.table({ "Day": [x["day"] for x in ss.investments],
                   "Kind": [x["kind"] for x in ss.investments],
                   "Amount": [x["amount"] for x in ss.investments] })

    if ss.savings:
        st.markdown("**Savings**")
        st.table({ "Day": [x["day"] for x in ss.savings],
                   "Amount": [x["amount"] for x in ss.savings],
                   "Interest": [x["interest"] for x in ss.savings],
                   "Maturity": [x["maturity"] for x in ss.savings],
                   "Maturity date": [fmt(x["mat_date"]) for x in ss.savings] })

st.divider()

# Build + Save summary.txt
colA, colB = st.columns([1,3])
with colA:
    if st.button("Build & Save summary.txt"):
        # compose text
        rem = remaining_amount(ss)
        lines = [
            "=== SPARRWALLET SUMMARY ===",
            f"Income: {ss.income:.2f}",
            f"Fixed costs: {ss.fixed:.2f}",
            f"Variable costs: {ss.variable_total:.2f}",
            f"Invested (total): {inv_total:.2f}",
            f"Saved (principal total): {sav_total_principal:.2f}",
            f"Projected savings interest (3m): {sav_total_interest:.2f}",
            f"Remaining: {rem:.2f}",
            ""
        ]
        if ss.investments:
            lines.append("Investments:")
            for i, iv in enumerate(ss.investments, 1):
                lines.append(f"  {i}) Day {iv['day']}: {iv['kind']} — {iv['amount']:.2f}")
        if ss.savings:
            lines.append("\nSavings:")
            for i, s in enumerate(ss.savings, 1):
                lines.append(f"  {i}) Day {s['day']}: Saved {s['amount']:.2f} → "
                             f"Interest {s['interest']:.2f} → Maturity {s['maturity']:.2f} "
                             f"(Date: {fmt(s['mat_date'])})")

        # evaluation
        total_spent_overall = ss.income - rem
        if total_spent_overall > ss.income * MONTHLY_ALERT_RATIO:
            lines.append("\nEvaluation: Your spending is NOT healthy.")
        elif rem < 0:
            lines.append("\nEvaluation: You overspent.")
        else:
            lines.append("\nEvaluation: Overall spending is acceptable.")
        lines.append("\nHave a nice day!")

        # write file
        out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.abspath(os.path.join(out_dir, "summary.txt"))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        st.success(f"Saved to {out_path}")

with colB:
    st.subheader("Session log")
    if ss.log:
        st.code("\n".join(ss.log))
    else:
        st.caption("No logs yet.")
