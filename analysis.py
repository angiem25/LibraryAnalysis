import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("Library Analysis")
df = pd.read_csv("PLS_FY23_AE_pud23i.csv",encoding="cp1252")



# Numeric columns used in dashboard
numeric_cols = [
    "F_EBOOK",
    "ELECCOLL",
    "TOTCIR",
    "ELMATCIR",
    "TOTPRO",
    "ADULTPRO",
    "TOTATTEN",
    "ADULTATTEN",
    "BKVOL",
    "VISITS",
    "POPU_LSA",
    "PRMATEXP",
    "ELMATEXP",
    "STAFFEXP",
    "K0_5ATTEN",
    "K6_11ATTEN",
    "YAATTEN"
]



# Convert columns to numeric safely
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows missing critical values
df = df.dropna(subset=[
    "POPU_LSA",
    "BKVOL",
    "LIBNAME",
    "STABR"
])



for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

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


    top5_metric = st.selectbox(
    "Top 5 Visualization",
    [
        "TOTCIR",
        "ELMATCIR",
        "TOTPRO",
        "ADULTPRO",
        "TOTATTEN",
        "ADULTATTEN",
        "F_EBOOK",
        "ELECCOLL",
        "BKVOL",
        "VISITS"
    ]
)

    top5_df = (
    df.sort_values(by=top5_metric, ascending=False)
    .head(5)
    .reset_index(drop=True)
    )

    top5_state = (
        state_df.sort_values(by=top5_metric, ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    circulation_df = top5_state[[ "LIBNAME", "TOTCIR", "ELMATCIR" ]].dropna()
    circulation_long = circulation_df.melt(
    id_vars="LIBNAME",
    value_vars=["TOTCIR", "ELMATCIR"],
    var_name="Type",
    value_name="Value"
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
    st.subheader(f"Top 5 Libraries by {top5_metric}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"🏆 Leaderboard — Top 5 by {top5_metric}")

    st.dataframe(
    top5_df[["LIBNAME", top5_metric]]
    .reset_index(drop=True)
    )

    st.dataframe(
    top5_state[["LIBNAME", top5_metric]]
    .reset_index(drop=True)
    )

    col1, col2 = st.columns(2)


    st.write("The data analysis:")
    st.dataframe(df)

    lib_df = state_df[state_df["LIBNAME"] == library]

    with col1:
        st.write(f"### Population vs Book Volume in {state}")
        st.write("Population vs Book Volume vs Library Branches in a City")
        fig = px.scatter(state_df, x="POPU_LSA",
        y="BKVOL", color="BRANLIB",height=400)
        st.plotly_chart(fig, use_container_width=True)

        materials = lib_df[["PRMATEXP", "ELMATEXP"]].sum().reset_index()
        materials.columns = ["Material Type", "Amount"]
        st.write(f"### Materials in {library}")
        st.write("Material types in library")
        fig = px.bar(
            materials,
            x="Material Type",
            y="Amount",
            title=f"Materials in {library}",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        
        kids_attendance = lib_df[["K0_5ATTEN","K6_11ATTEN","YAATTEN"]].sum().reset_index()
        kids_attendance.columns = ["kids_group", "attendance"]
        st.write(f"### Kids Attendance in {library}")
        fig = px.bar(
            kids_attendance,
            x="kids_group",
            y="attendance",
            title=f"Kids attendance {library}",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        circulation_long,
        x="LIBNAME",
        y="Value",
        color="Type",
        barmode="group",
        title="Circulation: Physical vs Electronic"
        )

    st.plotly_chart(fig, use_container_width=True)    

    program_df = top5_state[[ "LIBNAME", "TOTPRO", "ADULTPRO" ]].dropna()

program_long = program_df.melt(
    id_vars="LIBNAME",
    value_vars=["TOTPRO", "ADULTPRO"],
    var_name="Program Type",
    value_name="Count"
)

fig = px.bar(
    program_long,
    x="LIBNAME",
    y="Count",
    color="Program Type",
    barmode="stack",
    title="Library Programs Breakdown"
)

st.plotly_chart(fig, use_container_width=True)

attendance_df = top5_state[[ "LIBNAME", "TOTATTEN", "ADULTATTEN" ]].dropna()

attendance_long = attendance_df.melt(
    id_vars="LIBNAME",
    value_vars=["TOTATTEN", "ADULTATTEN"],
    var_name="Attendance Type",
    value_name="Value"
)

fig = px.bar(
    attendance_long,
    x="LIBNAME",
    y="Value",
    color="Attendance Type",
    barmode="group",
    title="Library Attendance Comparison"
)

st.plotly_chart(fig, use_container_width=True)


fig = px.bar(
    top5_state.sort_values(by=top5_metric),
    x=top5_metric,
    y="LIBNAME",
    orientation="h",
    title=f"Top 5 Libraries in {state}"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📍 Visits vs Program Attendance")

fig = px.scatter(
    top5_state,
    x="VISITS",
    y="TOTATTEN",
    size="TOTPRO",
    color="LIBNAME",
    hover_name="LIBNAME",
    title=f"Visits vs Attendance in {state}",
    trendline="ols"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📚 Circulation vs Electronic Materials")

fig = px.scatter(
    top5_state,
    x="TOTCIR",
    y="ELMATCIR",
    size="VISITS",
    color="LIBNAME",
    hover_name="LIBNAME",
    title=f"Circulation vs Electronic Materials in {state}",
)

st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    top5_state,
    x="TOTPRO",
    y="TOTATTEN",
    size="TOTCIR",
    color="ELMATCIR",
    hover_name="LIBNAME",
    title=f"Library Engagement Analysis in {state}",
    color_discrete_sequence=px.colors.qualitative.Bold
)


st.plotly_chart(fig, use_container_width=True)

state_df["VISITS_PER_PERSON"] = (
    state_df["VISITS"] / state_df["POPU_LSA"]
)

fig = px.bar(
    top5_state.sort_values(by="VISITS_PER_PERSON"),
    x="VISITS_PER_PERSON",
    y="LIBNAME",
    orientation="h",
    title="Library Visit Efficiency"
)


with t3:
    st.write("Conclusion")