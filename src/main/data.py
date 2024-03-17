import pandas as pd
import numpy as np
import streamlit as st
import requests

# api_key = '68ca08d738dd1219a5f92c9d16b60c65'
# app_id = '5110e220'
# url = 'https://api.schooldigger.com/v2.0/districts'
#
# params = {
#     'q': 'Liberty',
#     'st': 'CA',
#     'appID': app_id,
#     'appKey': api_key,
# }
# response = requests.get(url, params=params)
#
# if response.status_code == 200:
#     # Parse the JSON response into a Python dictionary
#     data = response.json()
#     for school in data['districtList']:
#         print(school['districtName'])
#     print(data)
st.title("Underfunded District Identifier")
st.subheader("2020 California School Districts Information")

opt0 = 'Drop Down Menu'
opt1 = 'Impacting a greater audience'
opt2 = 'Helping those in need equally'
option = st.selectbox('What is most important to you?',
     (opt0, opt1, opt2))


#create dataframe of 100 schools with least funding
original_df = pd.read_csv("/Users/adityapatwal/Documents/hackathon/districtcosts/Data-Table 1.csv")

#filter to data from California 2020
california_df = original_df[original_df['state_name'] == 'California']
temp_df = california_df[california_df['year'] == 2020]

# only consider negative funding gaps per pupil
new_df = temp_df[['district', 'ppcstot', 'predcost', 'fundinggap', 'enroll']]
negative_fundinggaps_df = new_df[new_df['fundinggap'] < 0]

#calculate totalGaps for each school
negative_fundinggaps_df = negative_fundinggaps_df.copy()
negative_fundinggaps_df.loc[:, 'Total Gap'] = negative_fundinggaps_df['fundinggap'] * negative_fundinggaps_df['enroll']
totalgap_sum = negative_fundinggaps_df['Total Gap'].sum()

negative_fundinggaps_df = negative_fundinggaps_df.rename(columns = {'district':'District',
                                                                    'ppcstot': 'Spending per Pupil',
                                                                    'predcost' : 'Required Spending',
                                                                    'fundinggap' : 'Funding Gap',
                                                                    'enroll' : 'Enrollment Size',
                                                                    })
totalEnrollment = negative_fundinggaps_df['Enrollment Size'].sum()

st.dataframe(negative_fundinggaps_df)


# WEIGHT

funds = int(st.text_input(label="Enter Funds...", value="0"))
st.write("The amount of funds is equal to ", funds)


if option == opt1:
    # find weight by taking sqrt of a schools total gap / California's funding gap
    negative_fundinggaps_df.loc[:, 'weight'] = np.sqrt(negative_fundinggaps_df['Total Gap']/totalgap_sum)
    lowest_totalgaps = negative_fundinggaps_df.nlargest(100, 'weight', keep='last').sort_values('weight')

    # calculate what percentage of funds should be allocated to each school
    weight_sum = lowest_totalgaps['weight'].sum()
    lowest_totalgaps['weight'] = (lowest_totalgaps['weight']/weight_sum)


    lowest_totalgaps.loc[:, 'Total Allocated Funds'] = lowest_totalgaps['weight'] * funds

    lowest_totalgaps = lowest_totalgaps[['District', 'Funding Gap', 'Total Gap', 'Total Allocated Funds']]
    lowest_totalgaps = lowest_totalgaps.rename(columns={"Funding Gap": "Per Student Funding Gap", "Total Gap": "Total Funding Gap"})

elif option == opt2:
     negative_fundinggaps_df.loc[:, 'weight'] = np.sqrt(negative_fundinggaps_df['Enrollment Size']/totalEnrollment)
     lowest_totalgaps = negative_fundinggaps_df.nlargest(100, 'weight', keep='last').sort_values('weight')
     # calculate what percentage of funds should be allocated to each school
     weight_sum = lowest_totalgaps['weight'].sum()
     lowest_totalgaps['weight'] = (lowest_totalgaps['weight']/weight_sum)
     lowest_totalgaps.loc[:, 'Total Allocated Funds'] = lowest_totalgaps['weight'] * funds

     lowest_totalgaps = lowest_totalgaps[['District', 'Funding Gap', 'Total Gap', 'Total Allocated Funds']]
     lowest_totalgaps = lowest_totalgaps.rename(columns={"Funding Gap": "Per Student Funding Gap", "Total Gap": "Total Funding Gap"})






#Display information
if option == opt2 or option == opt1:
    st.dataframe(lowest_totalgaps)






