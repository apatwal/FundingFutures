import pandas as pd
import numpy as np
import streamlit as st


# bigdf = pd.read_csv("/Users/adityapatwal/Documents/hackathon/districtcosts/Data-Table 1.csv")
# california_df = bigdf[bigdf['state_name'] == 'California']
# df = california_df[california_df['year'] == 2020]
# new_df = df[['year', 'district', 'ppcstot', 'predcost', 'fundinggap', 'enroll']]
# negative_fundinggaps_df = new_df[new_df['fundinggap'] < 0]
# negative_fundinggaps_df = negative_fundinggaps_df.copy()
# negative_fundinggaps_df.loc[:, 'totalgap'] = negative_fundinggaps_df['fundinggap'] * negative_fundinggaps_df['enroll']
# lowest_totalgaps = negative_fundinggaps_df.nlargest(100, 'totalgap', keep='last').sort_values('totalgap')
# print(lowest_totalgaps)
#
#
# st.title("Underfunded school identifier")

#create dataframe of 100 schools with least funding
original_df = pd.read_csv("/Users/adityapatwal/Documents/hackathon/districtcosts/Data-Table 1.csv")
california_df = original_df[original_df['state_name'] == 'California']
temp_df = california_df[california_df['year'] == 2020]
new_df = temp_df[['year', 'district', 'ppcstot', 'predcost', 'fundinggap', 'enroll']]
negative_fundinggaps_df = new_df[new_df['fundinggap'] < 0]
negative_fundinggaps_df = negative_fundinggaps_df.copy()
negative_fundinggaps_df.loc[:, 'totalgap'] = negative_fundinggaps_df['fundinggap'] * negative_fundinggaps_df['enroll']
totalgap_sum = negative_fundinggaps_df['totalgap'].sum()
negative_fundinggaps_df.loc[:, 'weight'] = np.sqrt(negative_fundinggaps_df['totalgap']/totalgap_sum)
lowest_totalgaps = negative_fundinggaps_df.nlargest(100, 'weight', keep='last').sort_values('weight')

#calculate what percentage of funds should be allocated to each school
weight_sum = lowest_totalgaps['weight'].sum()
lowest_totalgaps['weight'] = (lowest_totalgaps['weight']/weight_sum)
#st.write("The sum is ", lowest_totalgaps['weight'].sum())

funds = int(st.text_input(label="Enter Funds...", value="0"))
st.write("The amount of funds is equal to ", funds)
lowest_totalgaps.loc[:, 'fundsalloc'] = lowest_totalgaps['weight'] * funds

lowest_totalgaps = lowest_totalgaps[['district', 'fundinggap', 'totalgap', 'fundsalloc']]
lowest_totalgaps.rename(columns={"district": "District", "fundinggap": "Per Student Funding Gap", "totalgap": "Total Funding Gap", "fundsalloc": "Total Allocated Funds"})
#['District', 'Per Student Funding Gap', 'Total Funding Gap', 'Total Allocated Funds']


#Display information
st.title("Underfunded School Identifier")
st.dataframe(lowest_totalgaps)





