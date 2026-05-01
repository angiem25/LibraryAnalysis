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

t1, t2, t3 = st.tabs(["Overview", "Data", "Conclusion"])
with t1:
    st.write("The overview of our library analysis")
    st.write("This i san overview of our library analysis. " \
    "We are going to see the data of multiple libraries over the US along with" \
    "their digital materials, program attendance, population, etc.")
    st.write("Here is our dataframe with our columns.")
    st.dataframe(df)
with t2:
    st.write("The data analysis:")
    st.dataframe(df)

    lib_df = state_df[state_df["LIBNAME"] == library]

    st.write(f"### Population vs Book Volume in {state}")
    st.write("Population vs Book Volume vs Library Branches in a City")
    fig = px.scatter(state_df, x="POPU_LSA",
    y="BKVOL", color="BRANLIB")
    st.plotly_chart(fig, use_container_width=True)

    materials = lib_df[["PRMATEXP", "ELMATEXP"]].sum().reset_index()
    materials.columns = ["Material Type", "Amount"]
    st.write(f"### Materials in {library}")
    st.write("Material types in library")
    fig = px.bar(
        materials,
        x="Material Type",
        y="Amount",
        title=f"Material Expenditures in {library}"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("Staff and Expenditures")
    fig = px.box(
        state_df,
        x="STABR",
        y="STAFFEXP",
        title=f"Staff Expenditures in {library} in {state}",
    )
    st.plotly_chart(fig, use_container_width=True)

    kids_attendance = lib_df[["K0_5ATTEN","K6_11ATTEN","YAATTEN"]].sum().reset_index()
    kids_attendance.columns = ["kids_group", "attendance"]
    st.write(f"### Kids Attendance in {library}")
    #st.write("Material types in library")
    fig = px.bar(
        kids_attendance,
        x="kids_group",
        y="attendance",
        title=f"Kids attendance {library}"
    )
    st.plotly_chart(fig, use_container_width=True)

with t3:
    st.write("Conclusion")