import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import json

st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.header('A first look at the data')
st.write("Let's start by taking a quick look at our dataset")
 
with st.echo():
    df = pd.read_csv("startups.csv")
    st.write(df.head(5))

st.write("""
         Before we do any analyses, we should **rename columns** for convenience. 
         
         We should also make sure that all the columns are in a **proper format**.
         
         Lastly, we could extract the data on **year** and **quarter** from the `Date Joined` column,
         and additionally create a `year_quarter` column to work with later.
         
         Here's how we can do it:
         """)
         
with st.echo():
    df = pd.read_csv('startups.csv')
          
    ## Renaming:
    df.columns = df.columns.str.lower().str.replace(' ', '_') ## lowercase ## "snake-case"
    df.columns = df.columns.str.strip() ## strip
    df.rename(columns = {'valuation_($b)':'valuation_dollar_billions'}, inplace = True)

    ## String -> numeric (excluding "$" sign at the beginning of each value)
    df['valuation_dollar_billions'] = [round(float(value[1:])) for 
                                       value in df['valuation_dollar_billions'].values]

    ## Date -> propper formatting
    df['date_joined'] = pd.to_datetime(df['date_joined'])

    ## Adding "year_quarter" column
    df['year'] = df['date_joined'].dt.year
    df['quarter'] = df['date_joined'].dt.quarter
    df['year_quarter'] = df['year'].astype(str) + '_' + df['quarter'].astype(str)

    ## Extended list for selectbox
    countries = list(df['country'].unique()) + ["All countries"]
    countries.sort()
    
st.write("Let's see the results:")
with st.echo():
    df.head()
st.write(df.head())

st.write("#### So, after all the previous steps, our dataset consists of:")

col1, col2, col3 = st.columns((3, 3, 3))
col1.metric("Count of rows:", df.shape[0])
col2.metric("Count of columns:", df.shape[1])
col3.metric("""Unique company
            names:""", df['company'].nunique())



st.write("""
         This means that there's usually one row per startup. 
         
         But there are some startups which seem to have more that one row.
         
         Let's find them.
         """)

with st.echo():
    duplicate_companies = df[df.duplicated(subset = ['company'])]['company']
    df[df['company'].isin(duplicate_companies)].sort_values(by = 'company')
st.write(df[df['company'].isin(duplicate_companies)].sort_values(by = 'company'))

st.write("""
         These seem to be different companies, with same names, however.
         Their locations and industries are completely different from each other.
         
         So, we do have one row per a unicorn startup after all. 
         
         Hooray!
         
         **Finally, let's do a quick analysis of missing and unique values across our dataset.**
         
         There's a nice little function we can use for this purpose:
         """)

with st.echo():
    def check_nunique_missing(df):

        check_list = []
        
        ## For each column in our df
        for col in df.columns:
            
            dtypes = df[col].dtypes ## Save it's data type
            nunique = df[col].nunique() ## Save the count of unique values
            not_na = df[col].notna().sum() ## Count of not-na values
            sum_na = df[col].isna().sum() ## Count of NAs
            
            ## I'm creating a list of lists - with one "sublist" per each column of the original df
            check_list.append([col, dtypes, nunique, not_na, sum_na]) 
            
        df_check = pd.DataFrame(check_list) ## list (of lists) -> pd.DataFrame
        
        ## Setting appropriate column names
        df_check.columns = ['column', 'dtypes', 'nunique', 'not_na', 'sum_na'] 
        
        return df_check 

    check_nunique_missing(df)

col1, col2 = st.columns((5, 3))

col1.write(check_nunique_missing(df))
with col2:
    st.write("""
             Looks like we have no missing values in any of the columns
             except for the `investors` column.
             
             We'll see how to address the missing values there, when the time comes :)
             """)
             
st.write("""
         One last step in this preliminary exploratory analysis would 
         be to check the time period our data covers.""")
col1, col2 = st.columns((3, 3))
col1.metric("Minimum year:", df['year'].min())
col2.metric("Maximum year:", df['year'].max())
    
st.write("""
         Now, we can move on to a more detailed analysis of our data.
         
         Let's start by exploring how unicorns are distributed across different countries.
         """)
    
with open('6261-unicorn.json', "r") as f:
    data = json.load(f)
st_lottie(data, height = 200)
