import streamlit as st
import numpy as np
import pandas as pd

"""
# Rental Investigation
Edit assumptions on the left sidebar
"""

inital_value = st.sidebar.number_input("Inital Value In Thousands:", value=200, step=10) * 1000
years = st.sidebar.slider('Years Before Sale', min_value=1, max_value=30, value=30)
down_payment_p = st.sidebar.number_input("Down Payment % of Inital Value Assumption", value=4, step=1) /100
refinance_payment_p = st.sidebar.number_input("Refinance Payment % of Inital Value Assumption", value=3, step=1) /100
movement_cost = st.sidebar.number_input("Movement Cost", value=1000, step=100)

vacant_p = st.sidebar.number_input("Vacancy % Assumption", value=15, step=5) /100
appreciation = st.sidebar.number_input("Real House Appreciation Value % Assumption", value=2.0, step=.5) /100
man_time = st.sidebar.number_input("Yearly Man Hour Assumption", value=60, step=5) * years
man_rate = st.sidebar.number_input("Cost of Managemnt Time", value=40, step=5)
sale_cost_p = st.sidebar.number_input("Sale Cost % of Final Value Assumption", value=6, step=1) /100

mortage_init = st.sidebar.number_input("Mortage Cost", value=1250, step=10)
mortage_compound = st.sidebar.number_input("Mortage Yearly Increase % Assumption", value=.5, step=.1) /100
maint_init = st.sidebar.number_input("Monthly Maintance Inital Cost", value=150, step=10)
maint_compound = st.sidebar.number_input("Maintance Yearly Increase % Assumption", value=5, step=1) /100
rent_init = st.sidebar.number_input("Inital Rental Rate", value=1350, step=10)
rent_compound = st.sidebar.number_input("Rental Rate Yearly Increase % Assumption", value=2, step=1) /100



final_value = (inital_value * (1 + .025) ** (years))

final_value = final_value - (final_value*((30-years)/30))
sale_cost = final_value * sale_cost_p


management_cost = man_time * man_rate


# vectors
mortage_payment = mortage_init * 12 * np.full(years, 1+mortage_compound).cumprod()
maintenance = maint_init * 12 * np.full(years, 1+maint_compound).cumprod()
rent_rate = rent_init * 12 * np.full(years, 1+rent_compound).cumprod() * (1-vacant_p)
cash_flow = rent_rate - maintenance - mortage_payment




rent_df = pd.DataFrame({'Mortage': mortage_payment/12,
                        'Rent': rent_rate/12,
                        'Maintenance Cost': maintenance/12,
                        'Cash Flow': cash_flow/12},
                       index=list(range(years))
                      )


coi = (down_payment_p*inital_value) + (refinance_payment_p*inital_value) + movement_cost + management_cost

net_return = final_value + (rent_rate - maintenance - mortage_payment).sum() - coi - sale_cost 

rate_of_return = net_return/coi/years




"# Average Annual Rate Of Return:", round(rate_of_return, 4)
"$AverageAnnualRateOfReturn = NetReturn / COI / Years$"

"### Net Return:", round(net_return, 2)
"$NetReturn = Finalvalue + CashFlow - COI$"

# edit final value with a mortage calculator
"### Final Value:", round(final_value, 2)
"$Finalvalue = (Initialvalue * (1 + Appreciation) ^{(Years)}) - (Finalvalue * (30-Years)/30)$"

"### Cash Flow:", round(cash_flow.sum(),2)

"### Cost of Investment:", coi
"$COI = Downpayment + Refiancepayment + Movementcost + Managementcost$"
f"$COI = {down_payment_p*inital_value} + {refinance_payment_p*inital_value} + {movement_cost} + {management_cost}$"


"### Sale Cost:", round(sale_cost, 2), "| Vacant Rate:", vacant_p

"### Mangement Cost Per Year:", management_cost/years

"$Rent = RentRate * VacantPercent$"




"# Assumption Vectors:"
ax = rent_df.plot()
ax.set_ylabel('Monthly ($)')
ax.set_xlabel('Year')
st.pyplot()






