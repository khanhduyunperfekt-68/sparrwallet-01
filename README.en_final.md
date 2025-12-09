# SparrWallet -- Personal Budgeting Application (Python + Streamlit)

**Author:** Nguyễn Khánh Duy\
**Course:** Python Fundamentals\
**University:** SRH University

SparrWallet is a lightweight financial planning tool developed for the
Python Fundamentals course. The application allows users to track daily
expenses, calculate remaining monthly budget, visualize spending
patterns, and receive recommendations for saving or investing. This
project demonstrates basic Python programming, data handling, and the
development of a simple interactive interface using Streamlit.

------------------------------------------------------------------------

## 📑 Table of Contents

1.  Author\
2.  Project Overview\
3.  Features\
4.  Technologies Used\
5.  Installation\
6.  How to Run the Application\
7.  Usage Manual\
8.  Data Structure\
9.  Project Directory Structure\
10. Limitations\
11. License

------------------------------------------------------------------------

## 1. Author

-   **Name:** Nguyễn Khánh Duy\
-   **Course:** Python Fundamentals\
-   **Institution:** SRH University

------------------------------------------------------------------------

## 2. Project Overview

SparrWallet helps users understand their monthly finances by tracking
fixed and variable expenses. The application calculates how much of the
monthly income remains, evaluates the financial safety level, and
provides recommendations such as saving for 3 months at a fixed interest
rate or making small investments.

It also includes a spending chart to help interpret financial behaviour,
addressing feedback that the user interface should include additional
guidance and visualization.

------------------------------------------------------------------------

## 3. Features

### **Core Functionality**

-   Input monthly income and fixed monthly expenses.\
-   Add daily variable expenses with optional categories.\
-   Automatic calculation of remaining balance and percentage of income
    left.\
-   Safety evaluation (Safe / Moderate / Danger zones).\
-   Ability to invest in Stocks/ETFs or Crypto.\
-   Ability to save money for 3 months at 3.6% fixed interest.\
-   Auto-calculation of maturity date for savings.

### **User Interface**

-   Clear tooltips and guidance for all financial inputs.\
-   Daily spending chart (line chart).\
-   Clean layout using Streamlit columns.\
-   Real-time updates without page reload.

### **Data Output**

-   Export summary file to `/data/summary.txt`.\
-   Includes sample dataset (`sample_summary.txt`) for demonstration
    purposes.

------------------------------------------------------------------------

## 4. Technologies Used

-   Python 3.10+\
-   **Streamlit** -- interactive web interface\
-   **Pandas** -- tabular data & charts\
-   **datetime** -- date handling for savings maturity

------------------------------------------------------------------------

## 5. Installation

### **Prerequisites**

Ensure you have Python installed.

Install required libraries:

``` bash
pip install streamlit pandas
```

------------------------------------------------------------------------

## 6. How to Run the Application

Open a terminal:

``` bash
cd Sparr_Wallet_Project
streamlit run sparrwallet_app.py
```

A browser window will open automatically.\
If not, Streamlit will display a local URL such as:

    http://localhost:8501

------------------------------------------------------------------------

## 7. Usage Manual

### **Step 1: Initialize Budget**

In the sidebar, enter: - Monthly income (€)\
- Fixed monthly costs (€)

Click **"Initialize / Reset"**.

### **Step 2: Add Daily Spending**

Provide: - Day of month\
- Spending amount (€)\
- (Optional) Category

A warning appears if daily spending exceeds **15% of income**.

### **Step 3: Review Dashboard**

Display includes: - Total spent\
- Remaining balance\
- Safety status (Danger / Moderate / Safe)\
- Daily spending chart

### **Step 4: Investment or Savings Recommendation**

If remaining balance \> 20% of income: - Choose between **Stocks/ETF**,
**Crypto**, or **3-month savings** - Enter amount\
- System calculates interest + maturity date

### **Step 5: Export Summary**

Click **"Build & Save summary.txt"**\
File saved to `/data/`.

------------------------------------------------------------------------

## 8. Data Structure

### **Input Data**

-   User-generated: income, fixed costs, daily expenses\
-   Stored in Streamlit session state

### **Output Data**

`summary.txt` containing: - Income\
- Fixed + variable costs\
- Investments\
- Savings & interest\
- Remaining balance

### **Sample Data**

`/data/sample_summary.txt` --- sample dataset in EUR.

------------------------------------------------------------------------

## 9. Project Directory Structure

    Sparr_Wallet_Project/
    │
    ├── data/
    │    └── sample_summary.txt
    │
    ├── docs/
    │    └── summary.txt
    │
    ├── Web_UI_Final/
    │    └── sparr_logo.png
    │
    ├── sparrwallet_app.py
    └── README.md

------------------------------------------------------------------------

## 10. Limitations

-   Not a production-level finance tool.\
-   No persistent database (session resets clear data).\
-   Simple implementation prioritizing clarity over optimization.

------------------------------------------------------------------------

## 11. License

This project is created for educational purposes in the Python
Fundamentals course at SRH University.\
Free to use and modify for learning.
