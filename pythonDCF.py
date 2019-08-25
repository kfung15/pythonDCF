"""
Proj: pythonDCF.py

Auth: Ken Fung

Desc: One afternoon I decided to port a DCF model sample from WSP into python.
It's still wonky though. Sometimes it throws out negative values for equity value per share.
I suspect that it has got to do with the unlevered FCF calculations. I'm not quite sure exactly what to put in those.
Ahh well, I'll ask around, change things up, and things should get better!

"""


import requests
import json
from statistics import mean


def get_financial_data(ticker):
    
	#First, grab the data from all three of the available financial statements
	#Remember, things go in descending order, in terms of time!
	balance_sheet_base = "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/"
	balance_sheet_url = balance_sheet_base + str(ticker)
	balance_sheet_results = requests.get(balance_sheet_url)
	balance_sheet_json = balance_sheet_results.json()

	cash_flow_base = "https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/"
	cash_flow_url = cash_flow_base + str(ticker)
	cash_flow_results = requests.get(cash_flow_url)
	cash_flow_json = cash_flow_results.json()

	income_statement_base = "https://financialmodelingprep.com/api/v3/financials/income-statement/"
	income_statement_url = income_statement_base + str(ticker)
	income_statement_results = requests.get(income_statement_url)
	income_statement_json = income_statement_results.json()


	#Balance sheet data isolation time!

	#Bucket of current assets
	cash_list = []
	inventories_list = []
	short_term_investments_list = []
	accounts_receivables_list = []

	#Bucket of current liabilities
	accounts_payables_list = []
	short_term_debt_list = []

	long_term_debt_list = []

	# Grab this from the cash flow statement
	capex_list = []

	#Income statement data isolation time!
	revenue_list = []
	revenue_growth_rate_list = []
	EBITDA_list = []
	EBITDA_margin_list = []
	EBIT_list = []
	EBIT_margin_list = []
	DA_list = []
	DA_revenue_percent_list = []


	for x in range(len(balance_sheet_json.get("financials"))):
		if float(balance_sheet_json.get("financials")[x].get("Short-term investments")) != 0.0:
			short_term_investments_list.append(float(balance_sheet_json.get("financials")[x].get("Short-term investments")))
		cash_list.append(float(balance_sheet_json.get("financials")[x].get("Cash and cash equivalents")))
		inventories_list.append(float(balance_sheet_json.get("financials")[x].get("Inventories")))
		accounts_receivables_list.append(float(balance_sheet_json.get("financials")[x].get("Receivables")))

		accounts_payables_list.append(float(balance_sheet_json.get("financials")[x].get("Payables")))
		
		if float(balance_sheet_json.get("financials")[x].get("Short-term debt")) != 0.0:
			short_term_debt_list.append(float(balance_sheet_json.get("financials")[x].get("Short-term debt")))

		long_term_debt_list.append(float(balance_sheet_json.get("financials")[x].get("Long-term debt")))

		capex_list.append(float(cash_flow_json.get("financials")[x].get("Capital Expenditure")))

		revenue_list.append(float(income_statement_json.get("financials")[x].get("Revenue")))
		revenue_growth_rate_list.append(float(income_statement_json.get("financials")[x].get("Revenue Growth")))
		EBITDA_list.append(float(income_statement_json.get("financials")[x].get("EBITDA")))
		EBIT_list.append(float(income_statement_json.get("financials")[x].get("EBIT")))
		

	for x in range(len(EBITDA_list)):
		DA_list.append(float(EBITDA_list[x]) - float(EBIT_list[x]))
		EBITDA_margin_list.append(float(EBITDA_list[x])/float(revenue_list[x]))
		EBIT_margin_list.append(float(EBIT_list[x])/float(revenue_list[x]))
		DA_revenue_percent_list.append(float(DA_list[x])/float(revenue_list[x]))

	#Now for the prediction portion!

	avg_revenue_growth_rate = mean(revenue_growth_rate_list)
	avg_EBIT_margin = mean(EBIT_margin_list)
	avg_EBITDA_margin = mean(EBITDA_margin_list)
	avg_DA_revenue_percent = mean(DA_revenue_percent_list)

	accounts_receivables_growth_rate_list = []
	inventories_growth_rate_list = []
	short_term_investments_growth_rate_list = []

	accounts_payables_growth_rate_list = []
	short_term_debt_growth_rate_list = []

	capex_growth_rate_list = []

	for x in range(-1, -int(len(accounts_receivables_list)), -1):
		accounts_receivables_growth_rate_list.append((accounts_receivables_list[x - 1] - accounts_receivables_list[x])/accounts_receivables_list[x])
		inventories_growth_rate_list.append((inventories_list[x - 1] - inventories_list[x])/inventories_list[x])
		accounts_payables_growth_rate_list.append((accounts_payables_list[x - 1] - accounts_payables_list[x])/accounts_payables_list[x])
		capex_growth_rate_list.append((capex_list[x - 1] - capex_list[x])/capex_list[x])

	for x in range(-1, -int(len(short_term_debt_list)), -1):
		short_term_debt_growth_rate_list.append((short_term_debt_list[x - 1] - short_term_debt_list[x])/short_term_debt_list[x])

	for x in range(-1, -int(len(short_term_investments_list)), -1):
		short_term_investments_growth_rate_list.append((short_term_investments_list[x - 1] - short_term_investments_list[x])/short_term_investments_list[x])

	avg_accounts_receivables_growth_rate = mean(accounts_receivables_growth_rate_list)
	avg_inventories_growth_rate = mean(inventories_growth_rate_list)
	avg_short_term_investments_growth_rate = mean(short_term_investments_growth_rate_list)

	avg_accounts_payables_growth_rate = mean(accounts_payables_growth_rate_list)
	avg_short_term_debt_growth_rate = mean(short_term_debt_growth_rate_list)
	avg_capex_growth_rate = mean(capex_growth_rate_list)

	#Now that I got all the relevant averages, time to stretch out the last available relevant figures!
	#Do for five years in the future!

	future_revenue_list = []
	future_EBITDA_list = []
	future_EBIT_list = []
	future_DA_list = []

	future_revenue_list.append(revenue_list[0] * (1.0 + avg_revenue_growth_rate))
	future_EBITDA_list.append(EBITDA_list[0] * (1.0 + avg_EBITDA_margin))
	future_EBIT_list.append(EBIT_list[0] * (1.0 + avg_EBIT_margin))
	future_DA_list.append(DA_list[0] * (1.0 + avg_DA_revenue_percent))


	for x in range(4):
		future_revenue_list.append(future_revenue_list[x] * (1.0 + avg_revenue_growth_rate))
		future_EBITDA_list.append(future_EBITDA_list[x] * (1.0 + avg_EBITDA_margin))
		future_EBIT_list.append(future_EBIT_list[x] * (1.0 + avg_EBIT_margin))
		future_DA_list.append(future_DA_list[x] * (1.0 + avg_DA_revenue_percent))


	future_cash_list = []
	future_inventories_list = []
	future_short_term_investments_list = []
	future_accounts_receivables_list = []

	for x in range(5):
		future_cash_list.append(cash_list[0])

	future_inventories_list.append(inventories_list[0] * (1.0 + avg_inventories_growth_rate))
	future_short_term_investments_list.append(short_term_investments_list[0] * (1.0 + avg_short_term_investments_growth_rate))
	future_accounts_receivables_list.append(accounts_receivables_list[0] * (1.0 + avg_accounts_receivables_growth_rate))

	for x in range(4):
		future_inventories_list.append(future_inventories_list[x] * (1.0 + avg_inventories_growth_rate))
		future_short_term_investments_list.append(future_short_term_investments_list[x] * (1.0 + avg_short_term_investments_growth_rate))
		future_accounts_receivables_list.append(future_accounts_receivables_list[x] * (1.0 + avg_accounts_receivables_growth_rate))

	future_accounts_payables_list = []
	future_short_term_debt_list = []
	future_long_term_debt_list = []
	future_capex_list = []

	for x in range(5):
		future_long_term_debt_list.append(long_term_debt_list[0])

	future_accounts_payables_list.append(accounts_payables_list[0] * (1.0 + avg_accounts_payables_growth_rate))
	future_short_term_debt_list.append(short_term_debt_list[0] * (1.0 + avg_short_term_debt_growth_rate))
	future_capex_list.append(capex_list[0] * (1.0 + avg_capex_growth_rate))

	for x in range(4):
		future_accounts_payables_list.append(future_accounts_payables_list[x] * (1.0 + avg_accounts_payables_growth_rate))
		future_short_term_debt_list.append(future_short_term_debt_list[x] * (1.0 + avg_short_term_debt_growth_rate))
		future_capex_list.append(future_capex_list[x] * (1.0 + avg_capex_growth_rate))


	#Now we move onto the Free Cash Flow Buildup section

	tax_rate = 0.4
	future_EBIAT_list = []

	for x in range(len(future_EBIT_list)):
		future_EBIAT_list.append(future_EBIT_list[x] * (1.0 - tax_rate))

	unlevered_FCF_list = []

	for x in range(len(future_DA_list)):
		#unlevered_FCF_list.append(future_EBIAT_list[x] + future_DA_list[x] - future_inventories_list[x] - future_short_term_investments_list[x] - future_accounts_receivables_list[x] + future_accounts_payables_list[x] + future_short_term_debt_list[x] - future_capex_list[x])
		unlevered_FCF_list.append(future_EBIAT_list[x] + future_DA_list[x] - future_inventories_list[x] - future_accounts_receivables_list[x] + future_accounts_payables_list[x] - future_capex_list[x])


	#Now we find the WACC (Weighted Average Cost of Capital)

	profile_base = "https://financialmodelingprep.com/api/v3/company/profile/"
	profile_url = profile_base + str(ticker)
	profile_results = requests.get(profile_url)
	profile_json = profile_results.json()

	share_price = float(profile_json.get("profile").get("price"))
	diluted_shares_outstanding = float(income_statement_json.get("financials")[0].get("Weighted Average Shs Out"))
	after_tax_cost_of_debt = 0.031
	cost_of_equity = 0.15

	total_debt = float(balance_sheet_json.get("financials")[0].get("Total debt"))
	total_equity = share_price * diluted_shares_outstanding
	total_capital = total_debt + total_equity

	debt_weighting = total_debt/total_capital
	equity_weighting = total_equity/total_capital

	WACC = ((debt_weighting * after_tax_cost_of_debt) + (equity_weighting * cost_of_equity))

	#Now that we found the WACC, we can go back up to the FCF section

	FCF_present_values_list = []
	for x in range(5):
		FCF_present_values_list.append(unlevered_FCF_list[x]/((1 + WACC) ** (x+1)))

	PV_sum = sum(FCF_present_values_list)

	#Now we can move on to the Terminal Value section
	#Here, we will be using the Growth in Perpetuity method

	long_term_growth_rate = 0.04
	FCF_t_plus_one = unlevered_FCF_list[-1] * (1.0 + long_term_growth_rate)
	terminal_value = FCF_t_plus_one / (WACC - long_term_growth_rate)
	PV_of_terminal_value = terminal_value/((1.0 + WACC) ** (int(len(unlevered_FCF_list))))

	#Lastly, we move onto the Enterprise Value to Equity Value section

	enterprise_value = PV_sum + PV_of_terminal_value
	net_debt = total_debt - cash_list[0]
	equity_value = enterprise_value - net_debt
	equity_value_per_share = equity_value/diluted_shares_outstanding


	return(equity_value_per_share)

def main():
    #Change this to the company that you want to look up!
	print(get_financial_data("AAPL"))

if __name__ == '__main__':
    main()

