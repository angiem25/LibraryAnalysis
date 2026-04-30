import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("Library Analysis")
df = pd.read_csv("PLS_FY23_AE_pud23i.csv",encoding="cp1252")

df.columns = df.columns.str.strip()
df = df.dropna(subset=["POPU_LSA", "BKVOL"])

with st.sidebar:
    state = st.selectbox(
        "Select State",
        sorted(df["STABR"].dropna().unique())
    )

    state_df = df[df["STABR"] == state]

    library = st.selectbox(
    
        "LIBNAME",
        sorted(state_df["LIBNAME"].dropna().unique())
    )

# ✅ Filter data

lib_df = state_df[state_df["LIBNAME"] == library]

st.write(f"### Population vs Book Volume in {state}")
st.write("Population vs Book Volume vs Library Branches in a City")
fig = px.scatter(state_df, x="POPU_LSA",
y="BKVOL", color="BRANLIB")
st.plotly_chart(fig, use_container_width=True)

materials = lib_df[["PRMATEXP", "ELMATEXP"]].sum().reset_index()
materials.columns = ["Material Type", "Expenditure"]
st.write(f"### Materials in {library}")
st.write("Material types in library")
fig = px.bar(
    materials,
    x="Material Type",
    y="Expenditure",
    title=f"Material Expenditures in {library}"
)
st.plotly_chart(fig, use_container_width=True)