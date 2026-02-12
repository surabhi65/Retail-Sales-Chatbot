import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv(r"C:\Users\ASUS\Downloads\train (1).csv")


total_sales = data["Sales"].sum()
total_transactions = data["Order ID"].nunique()
total_customers = data["Customer ID"].nunique()
total_state = data["State"].nunique()
total_country = data["Country"].nunique()
total_city = data["City"].nunique()
total_category = data["Category"].nunique()
total_product=data["Product Name"].nunique()
total_segment=data["Segment"].nunique()
total_subcategory=data["Sub-Category"].nunique()


st.title("🤖 Retail Sales Chatbot")
st.write("Hey 👋")
st.write("Ask me about sales,products,category,region, etc.")
st.write("Suggestions: summarize,Total sales,Sales by region,Top 5 customers")


user_input = st.text_input("Type your question here:")

if user_input:
    query = user_input.lower()

    if "total sales" in query:
        st.write(f"📊Total Sales = {round(total_sales,2)}")
    elif "total transactions" in query:
        st.write(f"💳Total Transactions = {total_transactions}")
    elif "total customers" in query:
        st.write(f"👥Total Customers = {total_customers}")
    elif "total state" in query:
        st.write(f"Total States = {total_state}")
    elif "total country" in query:
        st.write(f"Total Countries = {total_country}")
    elif "total city" in query:
        st.write(f"Total Cities = {total_city}")
    elif "total category" in query:
        st.write(f"Total Categories = {total_category}")
    elif "total product" in query:
        st.write(f"Total product={total_product}")
    elif "total segments" in query:
        st.write(f"Total segment={total_segment}")
    elif "total sub categories" in query:
        st.write(f"Total sub categories={total_subcategory}")


   
    elif "top product by sales" in query:
        top_product = data.groupby("Product Name")["Sales"].sum().idxmax()
        st.write(f"Top Selling Product = {top_product}")
    elif "top category by sales" in query:
        top_category = data.groupby("Category")["Sales"].sum().idxmax()
        st.write(f"Top Performing Category = {top_category}")
    elif "top 5 customers" in query:
        top_customer = data.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(5)
        st.write("Top 5 Customers:")
        st.write(top_customer)
    elif "top 5 city" in query:
        top_city_sales = data.groupby("City")["Sales"].sum().sort_values(ascending=False).head(5)
        st.write("Top 5 Cities:")
        st.write(top_city_sales)
    elif "top 5 state" in query:
        top_state_sales = data.groupby("State")["Sales"].sum().sort_values(ascending=False).head(5)
        st.write("Top 5 States:")
        st.write(top_state_sales)
    
    elif "summarize" in query or "key insights" in query:
       st.subheader("Summarize")
       
       st.markdown("""

A small group of customers contribute a disproportionately high share of total revenue.

🔎 Business Insight:
Revenue concentration indicates high-value enterprise clients
Strong potential for long-term contracts
However, dependency risk exists if 1–2 major customers leave

🎯 Strategic Action:
Strengthen retention strategies for top clients
Introduce loyalty or premium partnership programs
Diversify revenue base to reduce dependency risk

🛒 Top Sold Items
A limited number of items dominate total sales volume and revenue.

🔎 Business Insight:
Clear high-demand product segments
Business likely follows the 80/20 Pareto Principle
These items drive major revenue performance

🎯 Strategic Action:
Maintain strong inventory for top-performing products
Focus marketing efforts on best-selling categories
Analyze margin contribution of top items

🏷️ Category Performance
Certain product categories generate significantly higher revenue compared to others.

🔎 Business Insight:
Revenue concentration across few categories
Possible underperformance in long-tail categories
Indicates product portfolio imbalance

🎯 Strategic Action:
Optimize or discontinue low-performing categories
Bundle slow-moving products with high-demand items
Invest more in high-margin categories

🌍 Geographic & Country-Level Performance
Revenue varies significantly across countries.

🔎 Business Insight:
Some regions dominate sales contribution
Indicates stronger brand presence in specific markets
Possible untapped potential in underperforming regions

🎯 Strategic Action:
Expand marketing in mid-performing regions
Study best-performing country strategies
Evaluate logistics efficiency across geographies

🏢 Branch-Level Performance
Revenue distribution across branches is uneven.

🔎 Business Insight:
One or two branches likely contribute major revenue share
Operational efficiency may differ regionally
Possible management or demand variations

🎯 Strategic Action:
Benchmark top branch performance
Improve processes in low-performing branches
Consider resource reallocation""")


    
    elif "sales by region" in query:
        region_sales = data.groupby("Region")["Sales"].sum()
        st.write("Sales by Region:")
        st.write(region_sales)
    elif "sales by state" in query:
        state_sales = data.groupby("State")["Sales"].sum().sort_values(ascending=False).head(10)
        st.write("Sales by State(Graph):")
        st.bar_chart(state_sales)
    elif "sales by customers" in query:
        cust_sales = data.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False)
        st.write("Top 5 Customers:")
        st.write(cust_sales)
    elif "sales by city" in query:
        city_sales = data.groupby("City")["Sales"].sum().sort_values(ascending=False).head(5)
        st.write("Top 5 Cities (Graph):")
        st.bar_chart(city_sales)
    elif "sales by customer" in query:
        cust_sales = data.groupby("Customer Name")["Sales"].sum().sort_values(ascending=False).head(5)
        st.write("Top 5 Customers (Graph):")
        st.bar_chart(cust_sales)
    elif "customer by segment" in query:
        cust_seg=data.groupby("Segment")["Customer Name"].nunique()
        st.write("Customers by segment(Graph):")
        st.bar_chart(cust_seg)
    elif "customer by region"in query:
        cust_reg=data.groupby("Region")["Customer Name"].nunique()
        st.write("Customers by region(Graph):")
        st.bar_chart(cust_reg)
    elif "sales by segment" in query:
        sal_seg=data.groupby("Segment")["Sales"].sum().sort_values(ascending=False).head()
        st.write("Sales by segment(Graph):")
        st.bar_chart(sal_seg)
    elif "ship mode by customer" in query:
        ship_cust=data.groupby("Ship Mode")["Customer ID"].nunique()
        st.write("Shipping Mode by customer(Graph):")
        st.bar_chart(ship_cust) 
    elif "customer by city" in query:
        cust_ct=data.groupby("City")["Customer ID"].nunique()
        st.write("Customer by city(Graph):")
        st.bar_chart(cust_ct)  
    elif "customer by state" in query:
        cust_st=data.groupby("State")["Customer ID"].nunique()
        st.write("Customer by state(Graph):")
        st.bar_chart(cust_st)  
    elif "shipping modes" in query.lower():
        ship_modes=data["Ship Mode"].drop_duplicates()
        st.subheader("Available Shipping Modes")
        st.write(ship_modes.values)
    elif "customers" in query.lower():
        cust_name=data["Customer Name"].drop_duplicates()
        st.subheader("Customers:")
        st.write(cust_name.values)
    elif "city" in query:
        city_names=data["City"].drop_duplicates()
        st.subheader("Cities:")
        st.write(city_names.values)
    elif "state" in query:
        state_names=data["State"].drop_duplicates()
        st.subheader("States:")
        st.write(state_names.values)
    elif "category" in query:
        cat_name=data["Category"].drop_duplicates()
        st.subheader("Categories:")
        st.write(cat_name.values)
    elif "product" in query:
        prod_name=data["Product Name"].drop_duplicates()
        st.subheader("Products:")
        st.write(prod_name.values)
    elif "sub category" in query:
        sub_cat=data["Sub-Category"].drop_duplicates()
        st.subheader("Sub categories:")
        st.write(sub_cat.values)
    elif "region" in query:
        reg_name=data["Region"].drop_duplicates()
        st.subheader("Regions:")
        st.write(reg_name.values)
    elif "postal codes" in query:
        post_cd=data["Postal Code"].drop_duplicates()
        st.subheader("Postal Code:")
        st.write(post_cd.values)
    elif "country" in query:
        country_name=data["Country"].drop_duplicates()
        st.subheader("Country:")
        st.write(country_name.values)
    else:
        st.write("Sorry, I don't understand that yet. Try asking about total sales, top product, top category, sales by region/state/city/customer, or top 5 customers/cities/states.")




        