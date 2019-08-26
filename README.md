# pythonDCF
My attempt on putting a DCF model into a program

Steps:
1. Retrieve revenue, EBITDA, EBIT and D&A. Forecast five years into the future by averaging out the change in numbers from year to year and extrapolating.
2. Look at the balance sheet and retrieve data on cash (& cash equivalents), receivables, inventories, short-term investments, payables, short-term debt, and long-term debt. Look at the income statement for capital expenditure.
3. For five years in the future, assume that cash (& cash equivalents) and long-term debt remain constant from the latest report. For all the other factors, average out the change in numbers from year to year and extrapolate.
4. Assume an earnings tax rate of 40%, for now. From EBIT, calculate EBIAT using that 40% tax rate.
5. Calculate unlevered free cash flow for five years into the future. From EBIAT, add D&A, add liabilities from step 3, subtract assets from step 3, and subtract capex from step 3.
6. Calculate weighted average cost of capital (WACC). Get the share price, and diluted shares outstanding. If diluted shares outstanding is not available, just get the shares outstanding for now. Assume tax rate of debt is 40%. Assume cost of debt is 3.2% and cost of equity is 15%.
7. Use the WACC figure to calculate the present value of free cash flows from the unlevered free cash flow figures in step 5.
8. Sum the present value of all five future years of free cash flows.
9. Calculate the present value of terminal value. Assume long-term growth rate of 4%, for now.
10. Take the present value of terminal value from step 9 and the sum of present values of free cash flows from step 8, add them together to get the enterprise value.
11. Subtract net debt from enterprise value to get equity value.
12. Divide equity value by diluted shares outstanding to get equity value per share.

Things to work on:
I'm still trying to figure out how DCF modelling works, and as I get more information, I'll update this program.

1. What exactly goes into the unlevered free cash flow formula?
2. How is cost of debt calculated?
3. How is cost of equity calculated?
4. How exactly do analysts figure out the growth percentage of a firm (asset, liabilities, revenue, etc.) for five years into the future?
