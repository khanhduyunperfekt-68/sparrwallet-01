
# Sparrwallet (Python Fundamentals CLI) — Step 2

A tiny expense manager for monthly budgeting, written with only Python standard library.

## Features (Step 2)
- Input monthly income, fixed costs, and variable expenses (by day).
- Daily alert if a day's variable spend exceeds a threshold (default 15% of income).
- Safe-zone actions if remaining cash > 20% of income: invest (Stocks/ETF or Crypto BTC/ETH) or save for 3 months at 3.6%.
- Auto day increment for quick daily logging; shows today's date on start.
- Savings show maturity amount and maturity date (+3 months, clamped to month-end if needed).
- Summary saved to `data/summary.txt` after each run.

## How to run
```bash
python sparrwallet.py
```

## File structure
```
Sparrwallet_Project/
  sparrwallet.py
  README.md
  data/
    summary.txt   # generated after running
  docs/
```

## Notes
- Thresholds at the top of `sparrwallet.py`:
  - `DAILY_ALERT_RATIO = 0.15`
  - `SAFE_REMAINING_RATIO = 0.20`
  - `SAVINGS_RATE_3M = 0.036`

  ## Example Output

- Fundamentals-level CLI; no external dependencies.
=== SPARRWALLET SUMMARY ===
Income: 50000.00
Fixed costs: 10000.00
Variable costs: 0.00
Invested total: 0.00
Saved principal total: 0.00
Projected savings interest (3m): 0.00
Remaining: 40000.00


--- Evaluation ---
Overall spending acceptable.
