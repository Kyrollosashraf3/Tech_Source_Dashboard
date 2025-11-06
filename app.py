import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.colors as pc

# -----------------------------
# Wrangle
# -----------------------------
def wrangle(path):
    df = pd.read_csv(path)

    # Date Type
    df['dateid'] = pd.to_datetime(df['dateid'], format='%Y%m%d')

    # Phone type
    df['consumer_phone'] = df['consumer_phone'].astype(str).str.replace(r'\.0', '', regex=True)

    # Fill Nulls
    df['consumer_phone'] = df['consumer_phone'].fillna('Unknown')
    df['sub_category'] = df['sub_category'].fillna('Unknown')
    df['category'] = df['category'].fillna('Unknown')

    return df

# -----------------------------
# Read and wrangle data
# -----------------------------
df = wrangle("New_Sales1.csv")

# -----------------------------
# Store Analysis
# -----------------------------
store_sales = df.groupby(['STOREID', "City_Lname"]).agg({
    'Transactionnumber': 'nunique',
    'RowTotalVatexc': 'sum'
}).reset_index()

store_sales["Avg_Sales_per_Transaction"] = round(store_sales['RowTotalVatexc'] / store_sales["Transactionnumber"])
store_sales = store_sales.rename(columns={'Transactionnumber': 'TRANSACTION_COUNT'})

Top_Stores_Sales = store_sales[["STOREID","RowTotalVatexc","City_Lname"]].sort_values(by='RowTotalVatexc', ascending=False).head()
Top_Store_Orders_count = store_sales[["STOREID","City_Lname","TRANSACTION_COUNT"]].sort_values(by='TRANSACTION_COUNT', ascending=False).head()
Top_Avg_Sales_per_Transaction = store_sales[["STOREID","Avg_Sales_per_Transaction"]].sort_values(by='Avg_Sales_per_Transaction', ascending=False).head()

city_sales = df.groupby(["City_Lname"]).agg({
    "STOREID": 'nunique',
    'Transactionnumber': 'nunique',
    'RowTotalVatexc': 'sum'
}).reset_index()

city_sales["Avg_Sales_per_Transaction"] = round(city_sales['RowTotalVatexc'] / city_sales["Transactionnumber"])
city_sales = city_sales.rename(columns={'STOREID': 'STORE_NUMBER', 'Transactionnumber': 'TRANSACTION_COUNT'})

Top_city_sales = city_sales.sort_values(by="RowTotalVatexc", ascending=False).head()
Top_city_sales["Store_performance"] = Top_city_sales["RowTotalVatexc"] / Top_city_sales["STORE_NUMBER"]
Top_city_sales["Store_performance"] = round(Top_city_sales["Store_performance"] / Top_city_sales["Store_performance"].sum(), 2) * 100

category_sales = df.groupby("category")["RowTotalVatexc"].sum().reset_index()
Top_category_sales = category_sales.sort_values(by='RowTotalVatexc', ascending=False).head()

sub_category_sales = df.groupby(["sub_category"])['RowTotalVatexc'].sum().reset_index()
Top_sub_category_sales = sub_category_sales.sort_values(by='RowTotalVatexc', ascending=False).head(20)

df_orders = df.groupby(["Transactionnumber", "trans_type1", "IsDelivery", "IsMaksab1"])["RowTotalVatexc"].sum().reset_index()
Order_type = df_orders["IsDelivery"].value_counts().reset_index()
Order_Maksab = df_orders["IsMaksab1"].value_counts().reset_index()



# CARDS
Total_Sales = df["RowTotalVatexc"].sum()
Total_Sales = f"{Total_Sales:,.0f}"  

total_orders = df['Transactionnumber'].nunique()
total_orders= f"{total_orders:,.0f}"

Customesr_number = df["consumer_phone"].nunique()
Customesr_number = f"{Customesr_number:,.0f}"




# -----------------------------
# Helper functions
# -----------------------------
def bar(df, x, y, title, n=10, text=None, hover=None, hover2=None):
    fig = px.bar(df, x=x, y=y, title=title, text=text, hover_data={hover: True, hover2: True})
    colors = pc.sample_colorscale("Blues", [i/(n) for i in range((n))])[::-1]
    fig.update_traces(marker=dict(color=colors), textfont=dict(size=15, color="black"))
    fig.update_layout(template="plotly_white")
    return fig

def pie(df, names, values, title, n=10, hover=None, hover2=None):
    fig = px.pie(df, names=names, values=values, title=title, hover_data={hover: True, hover2: True})
    colors = pc.sample_colorscale("Blues", [i/(n) for i in range((n))])[::-1]
    max_val = df[values].max()
    fig.update_traces(marker=dict(colors=colors), textinfo="label+percent", textposition="inside",
                      pull=[0.08 if v == max_val else 0 for v in df[values]])
    return fig




# -----------------------------
# Figures
# -----------------------------
fig1 = bar(Top_city_sales, "City_Lname", "RowTotalVatexc", "Top City by Sales", 12, "RowTotalVatexc", "STORE_NUMBER", "TRANSACTION_COUNT")
fig2 = bar(Top_city_sales, "City_Lname", "Store_performance", "City Sales performance By store number", 12, "Store_performance", "STORE_NUMBER", "RowTotalVatexc")
fig2.update_traces(text=Top_city_sales["Store_performance"].map("{:.0f}%".format))

fig3 = bar(Top_Stores_Sales, "STOREID", "RowTotalVatexc", "Top Stores By Sales", 10, "RowTotalVatexc", "City_Lname")
fig3.update_traces(text=Top_Stores_Sales["RowTotalVatexc"].apply(lambda x: f"{x:,.0f}"))

fig4 = bar(Top_Store_Orders_count, "STOREID", "TRANSACTION_COUNT", "Top Stores By Orders Count", 8, "TRANSACTION_COUNT", "City_Lname")
fig4.update_traces(text=Top_Store_Orders_count["TRANSACTION_COUNT"].apply(lambda x: f"{x:,.0f}"))

fig5 = pie(Top_category_sales, names="category", values="RowTotalVatexc", title="Sales Share by Category", n=8, hover="RowTotalVatexc")
fig6 = pie(Order_Maksab, names="IsMaksab1", values="count", title="Orders: Maksab vs Non-Maksab", n=4)

fig7 = px.bar(Top_sub_category_sales.head(15), x="RowTotalVatexc", y="sub_category", orientation="h", title="Top 10 Sub Categories by Sales", text="RowTotalVatexc")
colors = pc.sample_colorscale("Blues", [i/(25) for i in range(25)])[::-1]
fig7.update_traces(marker=dict(color=colors), textfont=dict(size=15, color="black"))
fig7.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
fig7.update_layout(template="plotly_white", yaxis={'categoryorder':'total ascending'})

fig8 = pie(Order_type, names="IsDelivery", values="count", title="Orders: Delivery vs Non-Delivery", n=4)

fig10 = px.treemap(df, path=['City_Lname','STOREID'], values='RowTotalVatexc', title='Sales by City and Store', hover_data={'RowTotalVatexc':':,.2f'})
fig10.update_traces(hovertemplate='<b>%{label}</b><br>Total Sales: %{value}<extra></extra>')

fig11 = px.treemap(df, path=['category','sub_category'], values='RowTotalVatexc', title="Sales by Category → Sub-category", hover_data={'RowTotalVatexc':':,.2f'})
fig11.update_traces(hovertemplate='<b>%{label}</b><br>Total Sales: %{value}<extra></extra>')

sales_trend = df.groupby('dateid')['RowTotalVatexc'].sum().reset_index()
sales_trend['day_name'] = sales_trend['dateid'].dt.day_name()
fig12 = px.line(sales_trend, x='dateid', y='RowTotalVatexc', markers=True, text='day_name', title='Sales Trend Over Time', labels={'dateid': 'Date', 'RowTotalVatexc': 'Sales Amount'})
fig12.update_traces(textposition='top center')
fig12.update_layout(xaxis_tickangle=45 , yaxis_tickformat=".3~s")

sales_by_cat = df.groupby(['dateid', 'category'])['RowTotalVatexc'].sum().reset_index()
fig13 = px.line(sales_by_cat[sales_by_cat['category'].isin(Top_category_sales['category'])], x='dateid', y='RowTotalVatexc', color='category', markers=True, title='Daily Sales Comparison by Category', labels={'dateid':'Date','RowTotalVatexc':'Total Sales','category':'Category'})
fig13.update_traces(mode='lines+markers')
fig13.update_layout(xaxis_tickangle=45, yaxis_tickformat=".2s", plot_bgcolor='white', legend_title_text='Category')

sales_by_sub_cat = df.groupby(['dateid', "sub_category","category"])['RowTotalVatexc'].sum().reset_index()
fig14 = px.line(sales_by_sub_cat, x='dateid', y='RowTotalVatexc', color='sub_category', markers=True, title='Daily Sales Comparison by Category', labels={'dateid':'Date','RowTotalVatexc':'Total Sales','sub_category':'Sub-Category'}, hover_data={'category': True})
fig14.update_traces(mode='lines+markers')
fig14.update_layout(xaxis_tickangle=45, yaxis_tickformat=".2s", plot_bgcolor='white', legend_title_text='sub_category')

# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(layout="wide", page_title="Dashboard")
st.title("Sales Dashboard")

# Define pages
pages = {
    "Page 1": [fig1, fig2, fig3, fig4],
    "Page 2": [fig5, fig6, fig7, fig8],
    "Page 3": [fig10, fig11],
    "Page 4": [fig12, fig13, fig14]
}

# Sidebar page selector
page_choice = st.sidebar.radio("Select Page", list(pages.keys()))
figures_to_show = pages[page_choice]

# Display figures
for i in range(0, len(figures_to_show), 2):
    if i + 1 < len(figures_to_show):
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(figures_to_show[i], use_container_width=True)
        with col2:
            st.plotly_chart(figures_to_show[i+1], use_container_width=True)
    else:
        st.plotly_chart(figures_to_show[i], use_container_width=True)
