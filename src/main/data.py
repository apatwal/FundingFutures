import pandas as pd
import numpy as np
import streamlit as st



st.markdown("<h1 style='text-align: center; color: White;'>Funding Futures</h1>", unsafe_allow_html=True)
state_names = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

# Create dropdown selectbox
state = st.selectbox('Select a state:', state_names)

# Display the selected state
st.write('Selected state:', state)

st.markdown(f"<h2 style='text-align: center; color: white;'>2020 {state} School Districts Information</h2>", unsafe_allow_html=True)

opt0 = 'Drop Down Menu'
opt1 = 'Impacting a greater audience'
opt2 = 'Helping those in need equally'
option = st.selectbox('What is most important to you?',
     (opt0, opt1, opt2))


#create dataframe of 100 schools with least funding
original_df = pd.read_csv("/Users/adityapatwal/Documents/hackathon/districtcosts/Data-Table 1.csv")

#filter to data from California 2020
state_df = original_df[original_df['state_name'] == state]
temp_df = state_df[state_df['year'] == 2020]

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

st.dataframe(negative_fundinggaps_df, width = 800)


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
    st.dataframe(lowest_totalgaps, width=800)






