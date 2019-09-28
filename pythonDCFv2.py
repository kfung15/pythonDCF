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

	real_time_price_base = "https://financialmodelingprep.com/api/v3/stock/real-time-price/"
	real_time_price_url = real_time_price_base + str(ticker)
	real_time_price_results = requests.get(real_time_price_url)
	real_time_price_json = real_time_price_results.json()

	profile_base = "https://financialmodelingprep.com/api/v3/company/profile/"
	profile_url = profile_base + str(ticker)
	profile_results = requests.get(profile_url)
	profile_json = profile_results.json()


	#Next, grab the latest Current Asset figures for the company!


	latest_cash = float(balance_sheet_json.get("financials")[0].get("Cash and cash equivalents"))
	latest_STI = float(balance_sheet_json.get("financials")[0].get("Short-term investments"))
	latest_receivables = float(balance_sheet_json.get("financials")[0].get("Receivables"))
	latest_inventories = float(balance_sheet_json.get("financials")[0].get("Inventories"))
	latest_other_CA = float(balance_sheet_json.get("financials")[0].get("Total current assets")) - latest_cash - latest_STI - latest_receivables - latest_inventories

	#Next, grab the latest Current Liabilities figures for the company!

	latest_payables = float(balance_sheet_json.get("financials")[0].get("Payables"))
	latest_STD = float(balance_sheet_json.get("financials")[0].get("Short-term debt"))
	latest_other_CL = float(balance_sheet_json.get("financials")[0].get("Total current liabilities")) - latest_payables - latest_STD

	#Now divide all the CAs and CLs by the latest Total Revenue
	#Get all the forward percentages!!!

	latest_total_revenue = float(income_statement_json.get("financials")[0].get("Revenue"))
	cash_perc = latest_cash/latest_total_revenue
	STI_perc = latest_STI/latest_total_revenue
	receivables_perc = latest_receivables/latest_total_revenue
	inventories_perc = latest_inventories/latest_total_revenue
	other_CA_perc = latest_other_CA/latest_total_revenue

	payables_perc = latest_payables/latest_total_revenue
	STD_perc = latest_STD/latest_total_revenue
	other_CL_perc = latest_other_CL/latest_total_revenue



	#Now slam them dank predicts five years into the future
	cash_predict = []
	STI_predict = []
	receivables_predict = []
	inventories_predict = []
	other_CA_predict = []

	payables_predict = []
	STD_predict = []
	other_CL_predict = []

	#______________________________________________

	#Here is exactly where the problem starts.
	#Need to somehow get to Capital IQ and manually input the revenue and COGS predict figures.
	#DO NOT just extrapolate from previous percentage figures like you're doing right now!!!
	
	#MANUAL INPUT
	IQ_revenue_predict = []
	IQ_COGS_predict = []

	#Test total revenue and COGS list (temporary measure for testing purposes)
	trial_future_revenue = [265595000000, 265595000000, 265595000000, 265595000000, 265595000000]
	trial_future_COGS = [163756000000, 163756000000, 163756000000, 163756000000, 163756000000]


	cash_predict.append(latest_cash * cash_perc)
	STI_predict.append(latest_STI * STI_perc)
	receivables_predict.append(latest_receivables * receivables_perc)
	inventories_predict.append(latest_inventories * inventories_perc)
	other_CA_predict.append(latest_other_CA * other_CA_perc)

	payables_predict.append(latest_payables * payables_perc)
	STD_predict.append(latest_STD * STD_perc)
	other_CL_predict.append(latest_other_CL * other_CL_perc)



	for x in range(4):
		cash_predict.append(cash_predict[x] * cash_perc)
		STI_predict.append(STI_predict[x] * STI_perc)
		receivables_predict.append(receivables_predict[x] * receivables_perc)
		inventories_predict.append(inventories_predict[x] * inventories_perc)
		other_CA_predict.append(other_CA_predict[x] * other_CA_perc)
		
		payables_predict.append(payables_predict[x] * payables_perc)
		STD_predict.append(STD_predict[x] * STD_perc)
		other_CL_predict.append(other_CL_predict[x] * other_CL_perc)

	#Uncomment once you figure out the Capital IQ stuff
	# for x in range(len(trial_future_revenue)):
	# 	cash_predict.append(trial_future_revenue[x] * cash_perc)
	# 	STI_predict.append(trial_future_revenue[x] * STI_perc)
	# 	receivables_predict.append(trial_future_revenue[x] * receivables_perc)
	# 	inventories_predict.append(trial_future_revenue[x] * inventories_perc)
	# 	other_CA_predict.append(trial_future_revenue[x] * other_CA_perc)

	# 	payables_predict.append(trial_future_COGS[x] * other_CA_perc)
	# 	STD_predict.append(trial_future_COGS[x] * other_CA_perc)
	# 	other_CL_predict.append(trial_future_COGS[x] * other_CA_perc)

	#__________________________________________________________________

	# Now put all the predictions in to Net working capital list

	NWC_predict = []
	for x in range(len(cash_predict)):
		NWC_predict.append(cash_predict[x] + STI_predict[x] + receivables_predict[x] + inventories_predict[x] + other_CA_predict[x] - payables_predict[x] - STD_predict[x] - other_CL_predict[x])

	
	#Now get the delta of NWC figures
	latest_NWC = latest_cash + latest_STI + latest_receivables + latest_inventories + latest_other_CA - latest_payables - latest_STD - latest_other_CL
	
	delta_NWC = []

	delta_NWC.append(NWC_predict[0] - latest_NWC)

	for x in range(4):
		delta_NWC.append(NWC_predict[x + 1] - NWC_predict[x])



	

	#=======================================================================================
	#Next, calculate free cash flowz
	#But watch out tho, there is a huge buildup!
	

	
	#Get the list of operating margin predictions
	#Operating margin is operating expense/total revenue
	#Future operating margin is the average of the previous three
	previous_operating_margin = []
	for x in range(2 , 0, -1):
		previous_operating_margin.append(float(income_statement_json.get("financials")[x].get("Operating Expenses"))/float(income_statement_json.get("financials")[x].get("Revenue")))
	previous_operating_margin.append(float(income_statement_json.get("financials")[0].get("Operating Expenses"))/float(income_statement_json.get("financials")[0].get("Revenue")))


	operating_margin_predict = []
	operating_margin_predict.append(mean(previous_operating_margin))
	operating_margin_predict.append((operating_margin_predict[0] + previous_operating_margin[1] + previous_operating_margin[2])/3.0)
	operating_margin_predict.append((operating_margin_predict[0] + operating_margin_predict[1] + previous_operating_margin[2])/3.0)

	for x in range(2):
		operating_margin_predict.append((operating_margin_predict[x] + operating_margin_predict[x + 1] + operating_margin_predict[x + 2])/3.0)

	#Now put those ops margin predict figures into ops expense predict list
	operating_exp_predict = []
	for x in range(len(operating_margin_predict)):
		operating_exp_predict.append(operating_margin_predict[x] * trial_future_revenue[x])

	

	#Now get the EBIT predict figures
	#EBIT is total revenue - operating expenses
	EBIT_predict = []
	for x in range(len(operating_exp_predict)):
		EBIT_predict.append(trial_future_revenue[x] - operating_exp_predict[x])
	
	
	#Assume income taxes is 21% for now
	#Income taxes is EBIT * 0.21

	income_taxes_predict = []
	for x in range(len(EBIT_predict)):
		income_taxes_predict.append(EBIT_predict[x] * 0.21)

	

	#CAPEX predict is old Capex/old revenue * new revenue

	capex_predict = []
	capex_predict.append((float(cash_flow_json.get("financials")[0].get("Capital Expenditure"))/latest_total_revenue)*trial_future_revenue[0])

	for x in range(4):
		capex_predict.append((capex_predict[x]/trial_future_revenue[x])*trial_future_revenue[x + 1])

	#return(capex_predict)

	#D&A predict is old D&A/old revenue * new revenue

	DNA_predict = []
	DNA_predict.append((float(cash_flow_json.get("financials")[0].get("Depreciation & Amortization"))/latest_total_revenue)*trial_future_revenue[0])

	for x in range(4):
		DNA_predict.append((DNA_predict[x]/trial_future_revenue[x])*trial_future_revenue[x + 1])

	

	#EBITDA is EBIT + D&A

	EBITDA_predict = []
	for x in range(len(DNA_predict)):
		EBITDA_predict.append(DNA_predict[x] + EBIT_predict[x])

	#return(EBITDA_predict)

	#Finally, get the FCFs

	FCF_predict = []

	for x in range(len(EBITDA_predict)):
		FCF_predict.append(EBITDA_predict[x] - income_taxes_predict[x] + delta_NWC[x] - capex_predict[x])


	#==============================================================================================

	# Next, calculate WACC

	# For this, you need the Beta, Share Price, Diluted Shares Outstanding, Risk Free rate,
	# average spread on bonds for a certain credit rating

	beta = float(profile_json.get("profile").get("beta"))
	
	#MANUAL INPUT
	risk_free_rate = 0.01687
	expected_equity_mkt_return = 0.1815
	average_spread = 0.0110
	
	share_price = float(real_time_price_json.get("price"))
	diluted_shs_outstanding = float(income_statement_json.get("financials")[0].get("Weighted Average Shs Out (Dil)"))
	cost_of_debt = risk_free_rate + average_spread
	tax_rate = 0.21
	cod_after_debt = cost_of_debt * (1 - tax_rate)

	#for cost of equity, use the markowitz formula
	cost_of_equity = risk_free_rate + (beta * (expected_equity_mkt_return - risk_free_rate))

	#find the totals for debt and equity
	total_equity = share_price * diluted_shs_outstanding
	total_debt = float(balance_sheet_json.get("financials")[0].get("Net Debt"))
	total_capital = total_equity + total_debt

	debt_weight = total_debt/total_capital
	equity_weight = total_equity/total_capital

	print("After Tax Cost of Debt: " + str(cod_after_debt))
	print("Cost of equity: " + str(cost_of_equity))

	#print(debt_weight)
	#print(equity_weight)

	wacc = (debt_weight * cod_after_debt) + (equity_weight * cost_of_equity)
	print("WACC: " + str(wacc))

	#=========================================================================================
	#Now that you have the WACC, discount all those items in FCF_predict and take the sum

	discounted_FCF_predict = []

	#print(FCF_predict)

	for x in range(len(FCF_predict)):
		discounted_FCF_predict.append(FCF_predict[x]/((1 + wacc) ** (float(x) + 1)))


	#print(discounted_FCF_predict)
	total_disc_FCF = sum(discounted_FCF_predict)


	#========================================================================
	# now to find the terminal value
	long_term_growth_rate = 0.0286
	last_fcf = FCF_predict[-1]

	terminal_value = (last_fcf * (1 + long_term_growth_rate))/(wacc - long_term_growth_rate)
	print("Terminal Value: " + str(terminal_value))

	PV_TV = terminal_value/((1+wacc) ** 5)
	print("Present Value of TV: " + str(PV_TV))

	#==========================================================================
	#home stretch!
	#find the enterprise value and wrap up from there!

	enterprise_value = PV_TV + total_disc_FCF
	equity_value = enterprise_value - total_debt

	equity_value_per_share = equity_value/diluted_shs_outstanding

	return("Equity Value Per Share: " + str(equity_value_per_share))


def main():
	#Change this to the company that you want to look up!
	print("Company getting DCF'ed: AAPL")
	print(get_financial_data("AAPL"))

if __name__ == '__main__':
	main()

	



