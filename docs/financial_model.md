# Financial model

The forecast covers exactly the next 14 days. Each day's closing balance equals the previous balance plus expected outstanding invoice collections minus scheduled expenses. Monetary operations use Python Decimal rounded to cents. The interface displays CNY. No model output supplies ledger values.

The expected scenario uses documented expected collection dates. The conservative scenario assumes no additional collections during the horizon. This is a scenario comparison, not a statistical confidence interval. The minimum balance and first negative day are calculated from daily balances. Forecast assumptions can fail if customers pay late or obligations change.

Sending a reminder records simulated delivery with zero cash received. Rescheduling moves the date of an eligible expense and keeps the liability. A separately recorded sandbox receipt changes actual cash and the invoice balance. Outcome verification checks available recorded cash against scheduled obligations; an improvement relying on expected collections remains projected recovery.

Financing options are hypothetical, read-only bullet repayment examples. Interest uses principal × annual rate × days / 365, rounded to cents. Total borrowing cost is interest plus disclosed fees; total repayment includes principal. Terms and rates are illustrative, not offers. Repayment may fall outside the 14-day forecast, so apparent immediate cash relief does not establish affordability.

Forecast evaluation samples realized receipt days independently of the forecast's expected dates. Daily balance MAE and terminal absolute error are synthetic sensitivity measures. They are not validation on real SME outcomes.
