import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#st.title("Library Analysis")
df = pd.read_csv("PLS_FY23_AE_pud23i.csv",encoding="cp1252")
#st.dataframe(df)
#Libraries = st.selectbox(
#"Libraries", df["BRANLIB"].unique())
#st.bar_chart
#st.write(df) # DataFrame
#st.write(fig) # Plotly / Altair fig
#st.write({"a":1}) # JSON
#st.write(model)

st.write("Population vs Book Volume vs Library Branches in a City")
fig = px.scatter(df, x="POPU_LSA",
y="BKVOL", color="BRANLIB")
st.write(df.columns)
st.plotly_chart(fig, use_container_width=True)