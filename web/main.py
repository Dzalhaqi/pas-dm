import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.title("Analisis Fuzzy Time Series Terhadap Ketersediaan Air Bersih dan Sanitasi di Seluruh Dunia")

st.markdown("## Data")

# load dataset
df = pd.read_csv('data.csv')