import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="HR Attrition Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================
# CUSTOM CSS
# ==================================

st.markdown("""
<style>

/* Main Page */
.stApp{
    background-color:#F8F5FF;
}

/* Top White Header */
[data-testid="stHeader"]{
    background-color:#F8F5FF;
}

[data-testid="stToolbar"]{
    background-color:#F8F5FF;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background-color:#EEE6FF;
}

/* Filter Labels */
[data-testid="stSidebar"] label{
    color:#4C1D95 !important;
    font-weight:600;
}

/* Selected Filter Chips */
span[data-baseweb="tag"]{
    background-color:#px.colors.sequential.Blues_r;
    color:px.colors.sequential.Blues_r;
    border:1px solid #C084FC !important;
    border-radius:10px !important;
}

/* Filter Remove Icon */
span[data-baseweb="tag"] svg{
    color:#4C1D95 !important;
}

/* Dashboard Title */
.dashboard-title{
    text-align:center;
    color:#2E1065;
    font-size:48px;
    font-weight:800;
    padding-bottom:15px;
}

/* KPI Cards */
.kpi-card{
    background:#FFFFFF;
    border-radius:18px;
    padding:22px;
    text-align:center;
    box-shadow:0px 6px 18px rgba(124,58,237,0.12);
    border-left:8px solid #8B5CF6;
}

.kpi-title{
    color:#6B7280;
    font-size:16px;
    font-weight:600;
}

.kpi-value{
    color:px.colors.sequential.Blues_r;
    font-size:30px;
    font-weight:bold;
}

/* Chart Containers */
[data-testid="stPlotlyChart"]{
    background:white;
    border-radius:18px;
    padding:12px;
    box-shadow:0px 4px 14px rgba(124,58,237,0.08);
}

hr{
    border:1px solid #D8B4FE;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# LOAD DATA
# ==================================

DATA_PATH = Path(__file__).parent / "Data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
df = pd.read_csv(DATA_PATH)

# ==================================
# SIDEBAR FILTERS
# ==================================

st.sidebar.title("🔍 Dashboard Filters")

department = st.sidebar.multiselect(
    "Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

job_role = st.sidebar.multiselect(
    "Job Role",
    df["JobRole"].unique(),
    default=df["JobRole"].unique()
)

marital = st.sidebar.multiselect(
    "Marital Status",
    df["MaritalStatus"].unique(),
    default=df["MaritalStatus"].unique()
)

overtime = st.sidebar.multiselect(
    "OverTime",
    df["OverTime"].unique(),
    default=df["OverTime"].unique()
)

# ==================================
# FILTER DATA
# ==================================

filtered_df = df[
    (df["Department"].isin(department)) &
    (df["Gender"].isin(gender)) &
    (df["JobRole"].isin(job_role)) &
    (df["MaritalStatus"].isin(marital)) &
    (df["OverTime"].isin(overtime))
]

# ==================================
# HEADER
# ==================================

st.markdown("""
<div class='dashboard-title'>
📊 HR Attrition Analysis Dashboard
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==================================
# KPI SECTION
# ==================================

total_emp = len(filtered_df)

employees_left = len(
    filtered_df[filtered_df["Attrition"]=="Yes"]
)

attrition_rate = round((employees_left / total_emp) * 100, 2) if total_emp else 0
avg_income = round(filtered_df["MonthlyIncome"].mean(), 0) if total_emp else 0
avg_tenure = round(filtered_df["YearsAtCompany"].mean(), 1) if total_emp else 0

c1,c2,c3,c4,c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class='kpi-card'>
    <div class='kpi-title'>Total Employees</div>
    <div class='kpi-value'>{total_emp}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-card'>
    <div class='kpi-title'>Employees Left</div>
    <div class='kpi-value'>{employees_left}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-card'>
    <div class='kpi-title'>Attrition Rate</div>
    <div class='kpi-value'>{attrition_rate}%</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='kpi-card'>
    <div class='kpi-title'>Avg Income</div>
    <div class='kpi-value'>${avg_income:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class='kpi-card'>
    <div class='kpi-title'>Avg Tenure</div>
    <div class='kpi-value'>{avg_tenure}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("##")

# ==================================
# ROW 1
# ==================================

col1,col2 = st.columns(2)

with col1:

    dept_attrition = (
        filtered_df[filtered_df["Attrition"]=="Yes"]
        .groupby("Department")
        .size()
        .reset_index(name="Employees Left")
    )

    fig1 = px.bar(
        dept_attrition,
        x="Department",
        y="Employees Left",
        title="Attrition by Department",
        color="Employees Left",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:

    fig2 = px.pie(
        filtered_df,
        names="Attrition",
        title="Attrition Distribution",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    st.plotly_chart(fig2, use_container_width=True)

# ==================================
# ROW 2
# ==================================

col3,col4 = st.columns(2)

with col3:

    fig3 = px.histogram(
        filtered_df,
        x="OverTime",
        color="Attrition",
        title="Overtime vs Attrition",
        barmode="group",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    st.plotly_chart(fig3, use_container_width=True)

with col4:

    fig4 = px.histogram(
        filtered_df,
        x="JobSatisfaction",
        color="Attrition",
        title="Job Satisfaction vs Attrition",
        barmode="group",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    st.plotly_chart(fig4, use_container_width=True)

# ==================================
# ROW 3
# ==================================

col5,col6 = st.columns(2)

with col5:

    fig5 = px.box(
        filtered_df,
        x="Attrition",
        y="MonthlyIncome",
        color="Attrition",
        title="Salary vs Attrition",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    st.plotly_chart(fig5, use_container_width=True)

with col6:

    fig6 = px.histogram(
        filtered_df,
        x="WorkLifeBalance",
        color="Attrition",
        title="Work-Life Balance vs Attrition",
        barmode="group",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    st.plotly_chart(fig6, use_container_width=True)

# ==================================
# AGE DISTRIBUTION
# ==================================

fig7 = px.histogram(
    filtered_df,
    x="Age",
    color="Attrition",
    title="Age Distribution",
    color_discrete_sequence=px.colors.sequential.Blues_r
)

st.plotly_chart(fig7, use_container_width=True)

