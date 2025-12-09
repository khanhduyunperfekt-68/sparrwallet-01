import streamlit as st
from datetime import date, timedelta
import os
import pandas as pd

DAILY_ALERT = 0.15
MONTHLY_ALERT = 0.90
SAFE_ZONE = 0.20
SAVING_RATE_3M = 0.036

def add_months(d, m=3):
    y = d.year + (d.month - 1 + m) // 12
    mm = (d.month - 1 + m) % 12 + 1
    try:
        return date(y, mm, d.day)
    except ValueError:
        # adjust for invalid day (like Feb 30)
        if mm == 12:
            ny, nm = y + 1, 1
        else:
            ny, nm = y, mm + 1
        return date(ny, nm, 1) - timedelta(days=1)

# Color logic

def color_bar(pct):
    if pct < 0.25:
        return "#d32f2f", "Danger"
    elif pct < 0.5:
        return "#fbc02d", "Moderate"
    else:
        return "#4CAF50", "Safe"

# Init session state

ss = st.session_state
if "income" not in ss:
    ss.income = 0.0
    ss.fixed = 0.0
    ss.day_totals = {}
    ss.variable_total = 0.0
    ss.investments = []
    ss.savings = []
    ss.log = []

# Layout

st.set_page_config(page_title="SparrWallet", layout="wide")
st.title("SparrWallet – Finance Dashboard (Fundamental)")
st.caption(f"Today: {date.today():%d/%m/%Y}")

# SIDEBAR: Budget setup

st.sidebar.header("Budget Setup")
st.sidebar.caption(
    "Enter your monthly income and fixed monthly costs. "
    "This initializes your monthly budget."
)

income = st.sidebar.number_input(
    "Monthly income (€)",
    min_value=0.0,
    help="Total monthly income before any expenses."
)

fixed = st.sidebar.number_input(
    "Fixed monthly costs (€)",
    min_value=0.0,
    help="Recurring expenses such as rent, utilities, insurance, etc."
)

if st.sidebar.button("Initialize / Reset"):
    ss.income = income
    ss.fixed = fixed
    ss.day_totals = {}
    ss.variable_total = 0.0
    ss.investments = []
    ss.savings = []
    ss.log = ["Initialized"]
    st.sidebar.success("Budget initialized.")

# Core Calculations

inv_total = sum(x["amount"] for x in ss.investments)
sav_principal = sum(x["amount"] for x in ss.savings)
sav_interest = sum(x["interest"] for x in ss.savings)
spent_now = ss.fixed + ss.variable_total + inv_total + sav_principal
remaining = ss.income - spent_now
ratio = 0 if ss.income <= 0 else max(min(remaining / ss.income, 1), 0)

# Dashboard: Remaining / Ratio / Add expense

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Remaining (€)", f"{remaining:,.2f}")
    st.metric("Spent so far (€)", f"{spent_now:,.2f}")

with c2:
    st.write("**Remaining Ratio**")
    color, status = color_bar(ratio)
    bar = f"""
    <div style='height:22px;width:100%;background:#eee;border-radius:10px;overflow:hidden;'>
      <div style='height:100%;width:{ratio*100:.1f}%;background:{color};'></div>
    </div>
    <p style='margin-top:4px;color:{color};font-weight:bold;'>{status} ({ratio*100:.1f}%)</p>
    """
    st.markdown(bar, unsafe_allow_html=True)

with c3:
    st.subheader("Add Daily Spending")
    st.caption("Record your daily variable expenses here.")

    v_day = st.number_input(
        "Day of month",
        min_value=1,
        max_value=31,
        help="Select the day when the spending occurred."
    )

    v_amt = st.number_input(
        "Amount (€)",
        min_value=0.0,
        step=1.0,
        help="Enter the spending amount."
    )

    category = st.text_input("Category (optional)", help="Example: food, transport, entertainment.")

    if st.button("Add expense"):
        ss.day_totals[v_day] = ss.day_totals.get(v_day, 0.0) + float(v_amt)
        ss.variable_total += float(v_amt)
        ss.log.append(f"+{v_amt:.2f} on day {v_day}")

        if ss.day_totals[v_day] > ss.income * DAILY_ALERT:
            st.warning(f"Daily alert: Day {v_day} exceeded {int(DAILY_ALERT*100)}% of income.")

        st.success("Expense added.")


st.divider()

# Safe zone suggestions

if ss.income > 0 and remaining > ss.income * SAFE_ZONE:
    st.success("Safe zone: You may invest or save now.")
    a1, a2, a3 = st.columns([2, 2, 1])

    with a1:
        action = st.radio("Choose action", ["Invest: Stocks/ETF", "Invest: Crypto", "Save 3 months @ 3.6%"])

    with a2:
        a_amt = st.number_input("Amount (€)", min_value=0.0, step=10.0)

    with a3:
        if st.button("Perform"):
            if a_amt <= 0 or a_amt > remaining:
                st.error(f"Amount must be >0 and ≤ remaining ({remaining:.2f}).")
            else:
                d = date.today().day
                if action.startswith("Invest"):
                    kind = "STOCKS/ETF" if "Stocks" in action else "CRYPTO"
                    ss.investments.append({"day": d, "kind": kind, "amount": float(a_amt)})
                    ss.log.append(f"Invested {kind} {a_amt:.2f}")
                    st.success("Investment recorded.")
                else:
                    interest = float(a_amt) * SAVING_RATE_3M
                    maturity = float(a_amt) + interest
                    mat_date = add_months(date.today(), 3)
                    ss.savings.append({
                        "day": d,
                        "amount": float(a_amt),
                        "interest": interest,
                        "maturity": maturity,
                        "mat_date": mat_date
                    })
                    ss.log.append(f"Saved {a_amt:.2f}; maturity {maturity:.2f} on {mat_date:%d/%m/%Y}")
                    st.info(f"Saved. Interest: {interest:.2f}; maturity on {mat_date:%d/%m/%Y}")
else:
    st.warning("Not in safe zone yet. Remaining must exceed 20% of income.")


st.divider()

# Daily expenses + Chart

left, right = st.columns(2)

with left:
    st.subheader("Daily Expenses")

    if ss.day_totals:
        df = pd.DataFrame({
            "Day": list(ss.day_totals.keys()),
            "Amount": list(ss.day_totals.values())
        }).sort_values("Day")

        st.subheader("Spending Chart (Daily)")
        st.caption("This chart summarizes your daily spending.")
        st.line_chart(df.set_index("Day"))

        st.table(df)
    else:
        st.caption("No variable expenses yet.")

# Summary

with right:
    st.subheader("Summary")
    st.markdown(f"""
- **Income:** {ss.income:,.2f}  
- **Fixed costs:** {ss.fixed:,.2f}  
- **Variable costs:** {ss.variable_total:,.2f}  
- **Invested (total):** {inv_total:,.2f}  
- **Saved principal:** {sav_principal:,.2f}  
- **Projected interest (3m):** {sav_interest:,.2f}  
- **Remaining:** {remaining:,.2f}
    """)

    if ss.investments:
        st.markdown("**Investments**")
        st.table(pd.DataFrame(ss.investments))

    if ss.savings:
        st.markdown("**Savings**")
        st.table(pd.DataFrame([{
            "Day": x["day"],
            "Amount": x["amount"],
            "Interest": x["interest"],
            "Maturity": x["maturity"],
            "Maturity date": x["mat_date"].strftime("%d/%m/%Y")
        } for x in ss.savings]))


st.divider()

# Export summary
if st.button("Build & Save summary.txt"):
    lines = [
        "=== SPARRWALLET SUMMARY ===",
        f"Income: {ss.income:.2f}",
        f"Fixed costs: {ss.fixed:.2f}",
        f"Variable costs: {ss.variable_total:.2f}",
        f"Invested (total): {inv_total:.2f}",
        f"Saved (principal total): {sav_principal:.2f}",
        f"Projected interest (3m): {sav_interest:.2f}",
        f"Remaining: {remaining:.2f}",
        ""
    ]
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.abspath(os.path.join(out_dir, "summary.txt"))
    with open(out_path, "w") as f:
        f.write("\n".join(lines))
    st.success(f"Saved to {out_path}")
    ss.log.append("summary.txt saved")

# Session log
st.subheader("Session Log")
if ss.log:
    st.code("\n".join(ss.log))
else:
    st.caption("No logs yet.")

