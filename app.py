import streamlit as st
import pandas as pd
import plotly.express as px

# =============================
# App Configuration
# =============================
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# =============================
# Load Data
# =============================
@st.cache_data
def load_data():
    df = pd.read_csv("New_Sales1.csv")
    df['dateid'] = pd.to_datetime(df['dateid'])
    return df

df = load_data()

# =============================
# Sidebar Filters
# =============================
st.sidebar.header("🔍 Filters")


min_date = df['dateid'].min()
max_date = df['dateid'].max()

# Date filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),  # القيمة الافتراضية = كامل المدى
    min_value=min_date,
    max_value=max_date
)


# City filter
city_filter = st.sidebar.multiselect(
    "Select Cities",
    df['City_Lname'].unique(),
    default=df['City_Lname'].unique()
)

# Category filter
category_filter = st.sidebar.multiselect(
    "Select Categories",
    df['category'].unique(),
    default=df['category'].unique()
)

# Apply filters
filtered_df = df[
    (df['dateid'].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))) &
    (df['City_Lname'].isin(city_filter)) &
    (df['category'].isin(category_filter))
]

# =============================
# Page Navigation
# =============================
page = st.sidebar.radio(
    "📊 Select Page",
    ["1️⃣ Sales Overview", "2️⃣ Top Categories", "3️⃣ City Insights", "4️⃣ Transactions"]
)

# =============================
# PAGE 1: SALES OVERVIEW
# =============================
if page == "1️⃣ Sales Overview":
    st.title("📈 Sales Overview")

    total_sales = filtered_df["RowTotalVatexc"].sum()
    total_transactions = filtered_df["Transactionnumber"].nunique()
    total_stores = filtered_df["STOREID"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"{total_sales:,.0f}")
    col2.metric("🧾 Transactions", total_transactions)
    col3.metric("🏪 Stores", total_stores)

    sales_trend = filtered_df.groupby("dateid")["RowTotalVatexc"].sum().reset_index()
    fig = px.line(
        sales_trend,
        x="dateid",
        y="RowTotalVatexc",
        title="Daily Sales Trend",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================
# PAGE 2: TOP CATEGORIES
# =============================
elif page == "2️⃣ Top Categories":
    st.title("🏆 Top Categories")

    cat_sales = (
        filtered_df.groupby("category")["RowTotalVatexc"].sum().reset_index().sort_values(by="RowTotalVatexc", ascending=False)
    )

    fig = px.pie(
        cat_sales,
        names="category",
        values="RowTotalVatexc",
        title="Sales by Category",
        hole=0.4
    )

    # Highlight largest slice automatically
    max_index = cat_sales["RowTotalVatexc"].idxmax()
    pull = [0.05 if i == max_index else 0 for i in range(len(cat_sales))]
    fig.update_traces(pull=pull)

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(cat_sales, use_container_width=True)

# =============================
# PAGE 3: CITY INSIGHTS
# =============================
elif page == "3️⃣ City Insights":
    st.title("🌍 City Insights")

    city_sales = (
        filtered_df.groupby("City_Lname")["RowTotalVatexc"].sum().reset_index().sort_values(by="RowTotalVatexc", ascending=False)
    )

    fig = px.bar(
        city_sales,
        x="City_Lname",
        y="RowTotalVatexc",
        title="Total Sales by City",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(city_sales, use_container_width=True)

# =============================
# PAGE 4: TRANSACTION ANALYSIS
# =============================
elif page == "4️⃣ Transactions":
    st.title("📦 Transaction Analysis")

    trans_type = (
        filtered_df.groupby("trans_type1")["RowTotalVatexc"].sum().reset_index()
    )

    fig = px.bar(
        trans_type,
        x="trans_type1",
        y="RowTotalVatexc",
        title="Sales by Transaction Type",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Sample Data")
    st.dataframe(filtered_df.head(20), use_container_width=True)

# =============================
# END
# =============================
st.markdown("---")
st.caption("📊 Built with Streamlit | Kyrollos Dashboard")
