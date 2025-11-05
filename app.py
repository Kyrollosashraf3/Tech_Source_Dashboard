import streamlit as st
import pandas as pd
#import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.colors as pc


# wrangle 
def wrangle(path):
    df = pd.read_csv(path)

    # Date Type
    df['dateid'] = pd.to_datetime(df['dateid'], format='%Y%m%d')

    # phone type
    df['consumer_phone'] = df['consumer_phone'].astype(str).str.replace(r'\.0', '', regex=True)

    # Nulls
    df['consumer_phone']= df['consumer_phone'].fillna('Unknown')
    df['sub_category']  = df['sub_category'].fillna('Unknown')
    df['Supervisor']    = df['Supervisor'].fillna('Unknown')
    df['category']      = df['category'].fillna('Unknown')

    return df


# Read and wrangle data
df = wrangle("New_Sales1.csv")


# Store_Analysis

store_sales= df.groupby(['STOREID',"City_Lname"]).agg({
        'Transactionnumber': 'nunique',      
        'RowTotalVatexc': 'sum'              
        }).reset_index()
 
# Add new column 
store_sales["Avg_Sales_per_Transaction"] = round(store_sales['RowTotalVatexc'] / store_sales["Transactionnumber"]) 

store_sales =store_sales.rename(columns={
    'Transactionnumber': 'TRANSACTION_COUNT'
})


# 1- Top stores by sales
Top_Stores_Sales = store_sales[["STOREID","RowTotalVatexc","City_Lname"]
                                ].sort_values(by='RowTotalVatexc', ascending=False).head()



# 2- Top stores by number of orders
Top_Store_Orders_count= store_sales[["STOREID","City_Lname","TRANSACTION_COUNT"]
                                     ].sort_values(by='TRANSACTION_COUNT', ascending=False).head()


# 3- Top_Avg_Sales_per_Transaction
Top_Avg_Sales_per_Transaction= store_sales[["STOREID","Avg_Sales_per_Transaction"]
                                            ].sort_values(by='Avg_Sales_per_Transaction', ascending=False).head()




city_sales= df.groupby(["City_Lname"]).agg({
        "STOREID" : 'nunique',
        'Transactionnumber': 'nunique',      
        'RowTotalVatexc': 'sum'              
        }).reset_index()
 
# Add new column 
city_sales["Avg_Sales_per_Transaction"] = round(city_sales['RowTotalVatexc'] / city_sales["Transactionnumber"]) 

# Rename columns
city_sales = city_sales.rename(columns={
    'STOREID': 'STORE_NUMBER',
    'Transactionnumber': 'TRANSACTION_COUNT'
})




# 1- Top city by sales
Top_city_sales = city_sales.sort_values(by="RowTotalVatexc", ascending=False).head()

Top_city_sales["Store_performance"] = Top_city_sales["RowTotalVatexc"] / Top_city_sales["STORE_NUMBER"]
Top_city_sales["Store_performance"] = round(Top_city_sales["Store_performance"] / Top_city_sales["Store_performance"].sum(), 2) * 100



# 1.1- Top category sales
category_sales= df.groupby("category")["RowTotalVatexc"].sum().reset_index()

Top_category_sales= category_sales.sort_values(by='RowTotalVatexc', ascending=False).head()



# 2- top sub category sales
sub_category_sales = df.groupby(["sub_category"])['RowTotalVatexc'].sum().reset_index()

Top_sub_category_sales = sub_category_sales.sort_values(by='RowTotalVatexc', ascending=False).head(20)






# 1- Delivary or Not
Order_type = df_orders["IsDelivery"].value_counts() .reset_index()

Order_Maksab = df_orders["IsMaksab1"].value_counts().reset_index()

total_orders = df['Transactionnumber'].nunique()

Returns = df_orders[df_orders["trans_type1"].str.startswith ("Return") ]
Returns_number = Returns.shape[0]

Quality_Level = (total_orders - Returns_number) / total_orders




#----------------------------------------------------------


def bar(df, x, y, title , n=10 ,text= None , hover=None, hover2=None ):
   
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        text=text ,
        hover_data={hover: True , hover2: True}
                     )   
        
  
    colors = pc.sample_colorscale(
        "Blues",  [i/(n) for i in range((n))]  )[::-1]

    fig.update_traces(
        marker=dict(color=colors),
        #textposition="outside",  
        textfont=dict(size=15, color="black")  ,
        
    )
    
    fig.update_layout(template="plotly_white")
    
    return fig






def pie(df, names, values, title ,  n=10 , hover=None, hover2=None  ):

    fig = px.pie(
    df,
    names= names,
    values= values,
    title= title,  
    hover_data={hover: True , hover2: True} )
    

    colors = pc.sample_colorscale(
        "Blues",  [i/(n) for i in range((n))]  )[::-1]
    
    max_val = df[values].max()

    fig.update_traces(
        marker=dict(colors=colors),
        textinfo="label+percent",  
        textposition="inside"    ,

            
        pull = [0.08 if v == max_val else 0 for v in df[values]]

           
    )
 
    return fig


# -------------------------------------------------------------------

fig1 = bar(Top_city_sales ,"City_Lname" , "RowTotalVatexc" , "Top City by Sales", 12,
             "RowTotalVatexc" , hover= "STORE_NUMBER",hover2= "TRANSACTION_COUNT")




fig2 = bar(Top_city_sales ,
            "City_Lname" ,"Store_performance" , "City Sales performance By store nubmer", 
            12, "Store_performance" ,"STORE_NUMBER", "RowTotalVatexc")

fig2.update_traces(text=Top_city_sales["Store_performance"].map("{:.0f}%".format))





fig3 = bar(Top_Stores_Sales ,
            "STOREID" ,
            "RowTotalVatexc" , 
            "Top Stores By Sales", 
            10,
            "RowTotalVatexc" , 
            "City_Lname" ,
            )

fig3.update_traces(
    text=Top_Stores_Sales["RowTotalVatexc"].apply(lambda x: f"{x:,.0f}")
)



# Top Stores By Orders Count
fig4 = bar(Top_Store_Orders_count ,
            "STOREID" ,
            "TRANSACTION_COUNT" , 
            "Top Stores By Orders Count", 
            8,
            "TRANSACTION_COUNT" , 
            "City_Lname"        )

fig4.update_traces(
    text=Top_Store_Orders_count["TRANSACTION_COUNT"].apply(lambda x: f"{x:,.0f}")
)

     



# Sales Share by Category

fig5 = pie(
    Top_category_sales,
    names="category",
    values="RowTotalVatexc",
    title="Sales Share by Category",
    n=8,
    hover="RowTotalVatexc",
    hover2=None
)


# Maksab Or Not
fig6 = pie (
    df=Order_Maksab,
    names="IsMaksab1",
    values="count",
    title="Orders: Maksab vs Non-Maksab",
    n=4
)





fig7 = px.bar(
    Top_sub_category_sales.head(15),
    x="RowTotalVatexc",
    y="sub_category",
    orientation="h",
    title="Top 10 Sub Categories by Sales",
    text="RowTotalVatexc"
)

n =25
colors = pc.sample_colorscale(
        "Blues",  [i/(n) for i in range((n))]  )[::-1]

fig7.update_traces(
        marker=dict(color=colors),
        textfont=dict(size=15, color="black")  ,
        
    )
fig7.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
fig7.update_layout(template="plotly_white", yaxis={'categoryorder':'total ascending'})



fig8 = pie (
    df=Order_type,
    names="IsDelivery",
    values="count",
    title="Orders: Delivery vs Non-Delivery",
    n=4
)

# -----------------------------------------------------

Total_Sales = df["RowTotalVatexc"].sum()
formatted_sales = f"{Total_Sales:,.0f}"  

# number of orders
total_orders = df['Transactionnumber'].nunique()
formatted_total_orders= f"{total_orders:,.0f}"

itemid_counts = df['itemid'].nunique()
formatted_item =        f"{itemid_counts: ,.0f}"

STORE_COUNTS = df['STOREID'].nunique()
STORE_COUNTS =        f"{STORE_COUNTS: ,.0f}"




# Sales Overview (Region → City → Store → Supervisor → Staff)
fig10 = px.treemap(
    df,
    path=["reg_Lname",'City_Lname','STOREID', "Supervisor", "Staff_Name"], 
    values='RowTotalVatexc',
    title='Sales by City and Store',
    hover_data={'RowTotalVatexc':':,.2f'}
)

fig10.update_traces(
    hovertemplate='<b>%{label}</b><br>Total Sales: %{value}<extra></extra>'
)



# Sales by Category → Sub-category
fig11 = px.treemap(
    df,
    path=['category','sub_category'],
    values='RowTotalVatexc',
    title="Sales by Category → Sub-category",
    hover_data={'RowTotalVatexc':':,.2f'}
 )

fig11.update_traces(
    hovertemplate='<b>%{label}</b><br>Total Sales: %{value}<extra></extra>'
)



# Plot sales trend over time with days
fig12 = px.line(
    sales_trend,
    x='dateid',
    y='RowTotalVatexc',
    markers=True,
    text='day_name',  
    title='Sales Trend Over Time',
    labels={'dateid': 'Date', 'RowTotalVatexc': 'Sales Amount'}
)

fig12.update_traces(textposition='top center')  
fig12.update_layout(xaxis_tickangle=45 , yaxis_tickformat=".3~s" )







fig13 = px.line(
    sales_by_cat[sales_by_cat['category'].isin(Top_category_sales['category'])],
    x='dateid',
    y='RowTotalVatexc',
    color='category',
    markers=True,
    title='Daily Sales Comparison by Category',
    labels={
        'dateid': 'Date',
        'RowTotalVatexc': 'Total Sales',
        'category': 'Category'
    }
)

fig13.update_traces(mode='lines+markers')
fig13.update_layout(
    xaxis_tickangle=45,
    yaxis_tickformat=".2s",  
    plot_bgcolor='white',
    legend_title_text='Category'
)


sales_by_sub_cat = df.groupby(['dateid', "sub_category","category"])['RowTotalVatexc'].sum().reset_index()


fig14 = px.line(
    sales_by_sub_cat,
    x='dateid',
    y='RowTotalVatexc',
    color='sub_category',
    markers=True,
    title='Daily Sales Comparison by Category',
    labels={
        'dateid': 'Date',
        'RowTotalVatexc': 'Total Sales',
        'sub_category': 'Sub-Category'
    },
    hover_data={'category': True}  # ← نضيف العمود اللي عايز نظهره

)

fig14.update_traces(mode='lines+markers')
fig14.update_layout(
    xaxis_tickangle=45,
    yaxis_tickformat=".2s",  # (K, M)
    plot_bgcolor='white',
    legend_title_text='sub_category'
)







# Add day name column
sales_trend= df.groupby('dateid')['RowTotalVatexc'].sum().reset_index()
sales_trend['day_name'] = sales_trend['dateid'].dt.day_name()










st.title("   ")
#st.subheader("     ")


# plotly_chart
st.set_page_config(layout="wide", page_title="Dashboard")

figures = [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8 , fig10, fig11 , fig12 , fig13 , fig14 ]
 
 
for i in range(0, len(figures), 2):  
    # عمودين لكل صف
    if i + 1 < len(figures):
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(figures[i], use_container_width=True)
        with col2:
            st.plotly_chart(figures[i+1], use_container_width=True)
    else:  # لو الشارت الأخير لوحده
        st.plotly_chart(figures[i], use_container_width=True)


