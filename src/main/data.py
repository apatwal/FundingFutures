import streamlit as st
import pandas as pd
import numpy as np
import locale
import re

locale.setlocale(locale.LC_ALL, '')
#Title
st.markdown("<h1 style='text-align: center; color: White;'>Funding Futures</h1>", unsafe_allow_html=True)


# Create dropdown selectbox
state_names = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

state = st.sidebar.selectbox('Select a state:', state_names, placeholder='Select State', index=4)


# Display the selected state
#st.write('Selected state:', state)
st.markdown(f"<h2 style='text-align: center; color: white;'>{state} School Districts Information</h2>", unsafe_allow_html=True)


#create dataframe of 100 schools with least funding
df = pd.read_csv("/Users/adityapatwal/Documents/hackathon/districtcosts/Data-Table 1.csv")


#filter to data from selected state 2020
df = df[df['state_name'] == state]
df = df[df['year'] == 2020]


# only consider negative funding gaps per pupil
df = df[['district', 'ppcstot', 'predcost', 'fundinggap', 'enroll']]
df = df[df['fundinggap'] < 0]


#calculate totalGaps for each school
#calculate totalGaps for each school
df.loc[:, 'Total Gap'] = df['fundinggap'] * df['enroll']
totalgap_sum = df['Total Gap'].sum()
def convertToCurrency(value):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Set the locale to use the correct formatting
    s = locale.currency(value, grouping=True, symbol=True)  # Specify symbol=True to include the currency symbol
    s = re.sub(r'[()]', '', s)  # Remove parentheses
    return s
s = convertToCurrency(abs(totalgap_sum))
st.sidebar.write(f"The total funds needed in order to properly fund each district is " + s)


#rename columns
df = df.rename(columns = {'district':'District',
                          'ppcstot': 'Spending per Pupil',
                          'predcost' : 'Required Spending',
                          'fundinggap' : 'Funding Gap',
                          'enroll' : 'Enrollment Size',
                          })


#calculate total enrollment size
totalEnrollment = df['Enrollment Size'].sum()


#Dropdown menu that determines algorithm for weight of districts
opt1 = 'Helping those in need proportionately'
opt2 = 'Impacting a greater audience'
option = st.sidebar.selectbox('What is most important to you?',
                              (opt1, opt2), placeholder="Select One")


#Number input that takes in the amount of funds to be allocated
funds = st.sidebar.number_input(label='Enter Funds', value=10000000)
#st.write("The amount of funds is equal to ", funds)


#Implement previously chosen option
if option == opt1:
    # find weight by taking sqrt of a schools total gap / states's funding gap
    df.loc[:, 'weight'] = np.sqrt(df['Total Gap']/totalgap_sum)
elif option == opt2:
    df.loc[:, 'weight'] = df['Total Gap']/totalgap_sum


# calculate what percentage of funds should be allocated to each school
df = df.nlargest(100, 'weight', keep='last').sort_values('weight')
weight_sum = df['weight'].sum()
df['weight'] = (df['weight']/weight_sum)
df.loc[:, 'Total Allocated Funds'] = df['weight'] * funds
df.loc[:, 'Post Allocation Gap'] = df['Funding Gap'] + (df['Total Allocated Funds']/df['Enrollment Size'])
df = df[['District', 'Funding Gap', 'Total Gap', 'Total Allocated Funds', 'Post Allocation Gap']]
df = df.rename(columns={"Funding Gap": "Per Student Funding Gap", "Total Gap": "Total Funding Gap"})
df.reset_index(inplace=True)

#Display information
if option == opt2 or option == opt1:
    st.dataframe(df)

bar_data = df[['District', 'Post Allocation Gap']]
bar_data.loc[:, 'Difference'] = df['Per Student Funding Gap'] - df['Post Allocation Gap']
st.bar_chart(bar_data, x="District",  y=["Post Allocation Gap", "Difference"], color=["#FF0000", "#0000FF"], height=800)