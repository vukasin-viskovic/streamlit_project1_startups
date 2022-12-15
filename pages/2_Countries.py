import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
import json

st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

##################################################################################################
    
st.header('Exploration across countries')

st.write("\n")
st.write("""
         
         Let's start by examining which countries are home to most unicorn startups :)
         """)

############################# DATA - importing and transforming ##################################

df = pd.read_csv("startups.csv")

## Renaming:
df.columns = df.columns.str.lower().str.replace(' ', '_') ## lowercase ## "snake-case"
df.columns = df.columns.str.strip() ## strip
df.rename(columns = {'valuation_($b)':'valuation_dollar_billions'}, inplace = True)

## String -> numeric (excluding "$" sign at the beginning of each value)
df['valuation_dollar_billions'] = [round(float(value[1:])) for value in df['valuation_dollar_billions'].values]

## Date -> propper formatting
df['date_joined'] = pd.to_datetime(df['date_joined'])

## Adding "year_quarter" column
df['year'] = df['date_joined'].dt.year
df['quarter'] = df['date_joined'].dt.quarter
df['year_quarter'] = df['year'].astype(str) + '_' + df['quarter'].astype(str)

## Extended list for selectbox
countries = list(df['country'].unique())
countries.sort()

########################################### SIDEBAR ############################################

st.sidebar.subheader('Bar chart parameters')

num_countries = st.sidebar.slider('Specify how many countries to plot', 5, df['country'].nunique(), 10)

ascending = st.sidebar.selectbox('Should the plotted values be sorted in ascending or descending order?',
                                ['descending', 'ascending'])
if ascending == 'descending':
    ascending = False
else:
    ascending = True
count_or_perc = st.sidebar.selectbox('Should the plot display values as counts or percentages?',
                                ['counts', 'percentages'])

plot_height = st.sidebar.slider('Specify plot height', 200, 500, 400)

graph_color = st.sidebar.color_picker('Graph Colors', '#8074F5')

st.sidebar.write('---')

############################################ PLOT ##############################################

df_country_grouped = pd.DataFrame(df.groupby('country')['company']\
    .nunique()\
        .sort_values(ascending = ascending)\
            .reset_index().head(num_countries))

df_country_grouped.rename(columns = {'company' : 'Count of companies'}, inplace = True)

df_country_grouped['Percentage of all companies'] = round(df_country_grouped['Count of companies'] / 
                                                          df['company'].nunique() * 100, 2)

if count_or_perc == 'percentages':
    y_column = 'Percentage of all companies'
    bar_title = "Percentage of startups per country"
else:
    y_column = 'Count of companies'
    bar_title = "Count of startups per country"
fig = px.bar(df_country_grouped, 
             x = 'country', 
             y = y_column, 
             title = bar_title,
             labels={'country' : 'Country'},
             height = plot_height,
             color_discrete_sequence = [graph_color],
             hover_data = ['country', 'Count of companies', 'Percentage of all companies'])
fig.update_xaxes(tickangle= -90)
#fig.update_traces(mode="markers+lines", hovertemplate=None)
#fig.update_layout(hovermode="country")
st.plotly_chart(fig, use_container_width = True)

####################################################################################################

st.write("""
         As we can see, most startups are based in USA (634 unicorn startups, 
         amountning to 53.59\% of the unicorns worldwide).
         
         USA is followed by China and India.
         
         """)

st.write("---")

###################################################################################################

st.sidebar.subheader('Metrics parameter')
selected_countries = st.sidebar.multiselect("""What countries do you want to filter for?
                                            Defaults to all countries""", 
                                            countries,
                                            None)

if len(selected_countries) == 0:
    selected_countries = countries  
    title_mini = "across all countries"
else:
    title_mini = f"in {', and '.join(selected_countries)}"

df_selected = df[df['country'].isin(selected_countries)]

###################################################################################################
   
st.markdown('### Specific country - metrics')
st.write("We can choose which countries to focus on in the sidebar dropdown list :)")
st.write(f"Let's examine startup valuations **{title_mini}**.")
st.write('\n')

col1, col2, col3 = st.columns((3, 3, 3))
col1.metric("Count of unicorns:", df_selected['company'].nunique())
col1.metric("Percentage of all unicorns:", round(df_selected['company'].nunique() / df['company'].nunique() * 100, 2))
col2.metric("AVG valuation ($ billion):", round(df_selected['valuation_dollar_billions'].mean(), 2))
col2.metric("Median valuation ($ billion):", df_selected['valuation_dollar_billions'].median())
col3.metric("Highest valuation ($ billion):", df_selected['valuation_dollar_billions'].max())
col3.metric("Lowest valuation ($ billion):", df_selected['valuation_dollar_billions'].min())

with open('6261-unicorn.json', "r") as f:
    data = json.load(f)
st_lottie(data, height = 200)