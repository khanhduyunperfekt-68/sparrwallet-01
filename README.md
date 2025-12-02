# SparrWallet — Personal Expense Management Application

## 1. Executive Summary
SparrWallet is a lightweight personal expense management application developed to demonstrate core Python programming skills and basic financial logic. The project provides a simple, web-based dashboard for tracking monthly income, fixed expenses, daily variable spending, and for offering saving and investment suggestions when surplus funds are available. The application is implemented using Streamlit and is deployable on Streamlit Cloud.

## 2. Objectives
This project aims to:
- Reinforce fundamental Python concepts (variables, control flow, functions, and basic data structures).
- Apply simple financial calculations to model monthly budgets.
- Build a minimal, user-friendly web interface with Streamlit.
- Demonstrate deployment and version control practices using GitHub and Streamlit Cloud.

## 3. Key Features
- Monthly income and fixed-cost input.
- Recording daily variable expenses with per-day totals.
- Automatic computation of total spent and remaining balance.
- Color-coded financial status indicator (safe, moderate, danger) based on remaining balance.
- Automated suggestions when remaining balance exceeds a safety threshold:
  - Short-term saving (3-month term with a fixed interest rate).
  - Simple investment selection (stocks/ETF or crypto), recorded as allocations.
- Build and export a text summary report.

## 4. Technology Stack
- Language: Python 3.8+
- UI framework: Streamlit
- Standard libraries: datetime, os
- Deployment: Streamlit Cloud
- Version control: Git and GitHub

## 5. Repository Layout
```
Sparrwallet/
│
├── data/                 # Data output (summary.txt) and optional persistence
├── docs/                 # Documentation, screenshots, additional notes
├── Web_ui_Final/         # Local development copy of the UI (optional)
│
├── sparrwallet_app.py    # Streamlit application (main entry point)
└── README.md             # Project README (this file)
```

## 6. Running Locally
1. Install dependencies:
```
pip install streamlit
```
2. From the project root directory, run:
```
streamlit run sparrwallet_app.py
```
3. Open your browser to `http://localhost:8501` to view the dashboard.

## 7. Deployment on Streamlit Cloud
1. Push the repository to a public GitHub repository.
2. Create a new app on https://share.streamlit.io and connect it to the repository.
3. Configure deployment with:
   - Repository: your GitHub repository
   - Branch: main (or the branch you use)
   - Main file path: `sparrwallet_app.py`
4. Deploy. The service will build the environment and expose a public URL.

## 8. Configuration and Parameters
The application uses a few configurable constants at the top of the script:
- Daily alert threshold (fraction of monthly income, default 0.15).
- Monthly alert threshold (fraction of monthly income, default 0.90).
- Safety threshold for recommendations (fraction of monthly income, default 0.20).
- Saving interest for a 3-month term (default 0.036, i.e., 3.6% for the period).

Adjust these constants in the source code as required for demonstration or testing.

## 9. Sample Input and Expected Output
Sample inputs:
- Monthly income: 50,000,000
- Fixed costs: 12,000,000
- Daily variable expenses: 500,000 on day 1; 1,200,000 on day 2

Expected outputs:
- Calculated total spent and remaining balance.
- Visual indicator of financial status (safe/moderate/danger).
- If remaining balance exceeds safety threshold, actionable suggestions to save or invest and projected 3-month saving returns.

## 10. Deliverables for Submission
- Source code: `sparrwallet_app.py`
- README file (this document)
- Optional: screenshots of the running dashboard inside `docs/`
- (Optional) `data/summary.txt` produced by the application

## 11. Notes and Next Steps
Recommended enhancements (optional):
- Persist data to a lightweight local database or CSV for multi-session history.
- Add charts (time series) to visualize daily spending trends.
- Add CSV/Excel export for reports.
- Improve UI with custom branding and logo handling.

## 12. Author
Developer: Khánh Duy  
GitHub: https://github.com/khanhduyunperfekt-68

