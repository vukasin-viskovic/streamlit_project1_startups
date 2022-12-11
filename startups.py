import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.title("Unicorn startups worldwide") ## Header
st.write("""
         We can use this Streamlit app to learn about unicorn startups across the world :)
         
         The app is still very much a work in progress!
         """) ## Text

st.subheader("Remains to be done:")
st.markdown("- Describe the df - it's source and basic structure")
st.markdown("- Clearly separate different levels of analysis -> world, countries, cities, industries...")
st.markdown("- Add filter by year option")
st.markdown("- Top investors, top industries")
st.markdown("- Include valuations into analysis - biggest companies per country, per example")


#############################################################################################

df = pd.read_csv("startups.csv")

## Renaming:
df.columns = df.columns.str.lower().str.replace(' ', '_') ## lowercase ## "snake-case"
df.columns = df.columns.str.strip() ## strip
df.rename(columns = {'valuation_($b)':'valuation_dollar_billions'}, inplace = True)

## String -> numeric
df['valuation_dollar_billions'] = [round(float(value[1:])) for value in df['valuation_dollar_billions'].values]

## Date -> propper formatting
df['date_joined'] = pd.to_datetime(df['date_joined'])

## Adding "year_quarter" column
df['year'] = df['date_joined'].dt.year
df['quarter'] = df['date_joined'].dt.quarter
df['year_quarter'] = df['year'].astype(str) + '_' + df['quarter'].astype(str)

## Extended list for selectbox
countries = list(df['country'].unique()) + ["All countries"]
countries.sort()

################################################################################################

st.header("Count of startups per country") ## Header ########################################### Bar chart countries - all

df_country_grouped = pd.DataFrame(df.groupby('country')['company']\
    .nunique()\
        .sort_values(ascending = False))

st.bar_chart(df_country_grouped)

selected_countries = st.selectbox('What country do you want to filter for?', countries) ## Selectbox Countries

if selected_countries == 'All countries':
    title_mini = "across all countries"
else:
    df = df[df['country'] == selected_countries]
    title_mini = f"in {selected_countries}"

st.header("A brief overview of the data") ## Header ############################################# Table 
st.write(df.head()) ## Table

st.subheader("Valuations across time") ########################################################## Line Chart - Country

df_dates = df[['date_joined', 'valuation_dollar_billions']].sort_values(by = 'date_joined').set_index('date_joined')

st.line_chart(df_dates)

st.header(f"Count of startups across cities {title_mini}") ###################################### Bar Chart Cities
how_many = st.number_input(label = 'Select how many cities you want to see on the bar chart',  ## Numerical input
                             min_value = 5, 
                             max_value = 30, 
                             value = 5)

## Grouping data for plotting

df_city_grouped = pd.DataFrame(df.groupby('city')['company']\
    .nunique()\
        .sort_values(ascending = False))

df_city_grouped.columns = ['count_companies']

if len(df_city_grouped) >= how_many:
    st.write(f"There are {len(df_city_grouped)} cities with unicorn startups {title_mini}.")
    st.write(f"The chart displays top {how_many} cities with most unicorns.")
    st.bar_chart(df_city_grouped.head(how_many))
elif len(df_city_grouped) >= 2 and len(df_city_grouped) < how_many:
    st.write(f"There are {len(df_city_grouped)} cities with unicorn startups {title_mini}")
    st.write(f"So, the bar chart can only display data for {len(df_city_grouped)} cities.")  
    st.bar_chart(df_city_grouped.head(len(df_city_grouped)))
else:
    st.write(f"There is only 1 city with unicorn startups {title_mini}: **{str(df_city_grouped.index[0])}** with **{df_city_grouped.values[0][0]} startup(s)**")
    st.write("So, it wouldn't make sense to produce a bar chart. Feel free to try another country :) ")