import streamlit as st
import pandas as pd
#import plotly.express as px
#import altair as alt
from streamlit_lottie import st_lottie
import json

st.set_page_config(layout="wide")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("Unicorn startups worldwide") ## Header
st.write("""
         We can use this Streamlit app to learn about unicorn [startups](https://en.wikipedia.org/wiki/Startup_company) across the world :)
         
         ---
         
         **From Wiki**:
         
         *In business, a unicorn is a privately held startup company valued at over US$1 billion.*
         
         *The term was first published in 2013, coined by venture capitalist [Aileen Lee](https://en.wikipedia.org/wiki/Aileen_Lee),* 
         *choosing the mythical animal to represent the statistical rarity of such successful ventures.*
         
         ---
         
         We will use [this](https://www.kaggle.com/datasets/ramjasmaurya/unicorn-startups) lovely dataset, 
         available on Kaggle.com, to perform our explorations :)
         """)

with open('6261-unicorn.json', "r") as f:
    data = json.load(f)
st_lottie(data, height = 200)