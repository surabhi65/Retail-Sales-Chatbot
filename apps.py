import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title="Retail Analytics Pro Dashboard", layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
.main { background-color: #0E1117; }
section[data-testid="stSidebar"] { background-color: #111827; }
.metric-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 20px; border-radius: 15px; text-align: center;
    color: white; box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}
.metric-value { font-size: 28px; font-weight: bold; }
.metric-label { font-size: 14px; opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

REPURCHASE_ORDERS_THRESHOLD = 5
REPURCHASE_SALES_THRESHOLD = 2000


@st.cache_data
def load_data(uploaded_file):
    """Load and preprocess CSV data."""
    data = pd.read_csv(uploaded_file)
    data["Order Date"] = pd.to_datetime(data["Order Date"], dayfirst=True)
    data["year"] = data["Order Date"].dt.year
    data["month_num"] = data["Order Date"].dt.month
    data["month_name"] = data["Order Date"].dt.strftime("%B")
    return data

def apply_filters(data):
    """Apply all sidebar filters."""
    st.sidebar.markdown("## 🔎 Filters")
    st.sidebar.divider()
    
    filtered_data = data.copy()
    
    
    years = ["All"] + sorted(data["year"].unique())
    selected_year = st.sidebar.selectbox("Select Year", years)
    if selected_year != "All":
        filtered_data = filtered_data[filtered_data["year"] == selected_year]
    
    
    categories = ["All"] + sorted(filtered_data["Category"].unique())
    selected_category = st.sidebar.selectbox("Select Category", categories)
    if selected_category != "All":
        filtered_data = filtered_data[filtered_data["Category"] == selected_category]
    
    regions = ["All"] + sorted(filtered_data["Region"].unique())
    selected_region = st.sidebar.selectbox("Select Region", regions)
    if selected_region != "All":
        filtered_data = filtered_data[filtered_data["Region"] == selected_region]
    
  
    customers = ["All"] + sorted(filtered_data["Customer Name"].unique())
    selected_customer = st.sidebar.selectbox("Select Customer", customers)
    if selected_customer != "All":
        filtered_data = filtered_data[filtered_data["Customer Name"] == selected_customer]
    
    return filtered_data

@st.cache_data
def compute_metrics(filtered_data):
    """Compute key metrics from filtered data."""
    total_sales = filtered_data["Sales"].sum()
    total_orders = filtered_data["Order ID"].nunique()
    total_customers = filtered_data["Customer ID"].nunique()
    total_products = filtered_data["Product Name"].nunique()
    top_category = filtered_data.groupby("Category")["Sales"].sum().idxmax()
    
    return {
        'total_sales': total_sales, 
        'total_orders': total_orders,
        'total_customers': total_customers, 
        'total_products': total_products,
        'top_category': top_category
    }


@st.cache_data
def train_models(data):
    """Train ML models on full dataset."""
    
    customer_df = data.groupby("Customer Name").agg({
        "Order ID": "count", "Sales": "sum"
    }).reset_index().rename(columns={"Order ID": "Total Orders", "Sales": "Total Sales"})
    
    customer_df["Purchased Again"] = (
        (customer_df["Total Orders"] > REPURCHASE_ORDERS_THRESHOLD) &
        (customer_df["Total Sales"] > REPURCHASE_SALES_THRESHOLD)
    ).astype(int)
    
    X = customer_df[["Total Orders", "Total Sales"]]
    y = customer_df["Purchased Again"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
   
    yearly_sales = data.groupby("year")["Sales"].sum().reset_index()
    forecast_model = LinearRegression()
    forecast_model.fit(yearly_sales[["year"]], yearly_sales["Sales"])
    
    return customer_df, model, accuracy, forecast_model

uploaded_file = st.sidebar.file_uploader("📁 Upload Sales CSV", type="csv")

if uploaded_file is not None:
    
    data = load_data(uploaded_file)
    st.sidebar.success(f"✅ Data loaded! {len(data)} rows")
    
   
    filtered_data = apply_filters(data)
    
    metrics = compute_metrics(filtered_data)
    
   
    customer_df, model, accuracy, forecast_model = train_models(data)
    
    st.title("🤖 Retail Analytics Pro Dashboard")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "🔮 Prediction", "📈 Forecast", "💬 Chatbot"])
    
    with tab1:
        st.subheader("📊 Executive Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        def kpi_card(title, value):
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{title}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col1: kpi_card("💰 Total Sales", f"${metrics['total_sales']:,.0f}")
        with col2: kpi_card("🧾 Total Orders", metrics['total_orders'])
        with col3: kpi_card("👥 Customers", metrics['total_customers'])
        with col4: kpi_card("📦 Products", metrics['total_products'])
        
        st.divider()
        
        st.subheader("📈 Monthly Sales Trend")
        monthly_sales = filtered_data.groupby(["year", "month_num"])["Sales"].sum().reset_index()
        monthly_sales["Date"] = pd.to_datetime(
            monthly_sales["year"].astype(str) + "-" + 
            monthly_sales["month_num"].astype(str) + "-01"
        )
        fig_trend = px.line(monthly_sales, x="Date", y="Sales", markers=True)
        fig_trend.update_layout(template="plotly_dark")
        st.plotly_chart(fig_trend, use_container_width=True)
        
        st.subheader("💼 Sales by Category")
        sales_by_cat = filtered_data.groupby("Category")["Sales"].sum().reset_index()
        fig_cat = px.bar(sales_by_cat, x="Category", y="Sales", 
                        color="Sales", color_continuous_scale="Teal", text_auto=True)
        fig_cat.update_layout(template="plotly_dark")
        st.plotly_chart(fig_cat, use_container_width=True)
        st.success(f"🏆 Top Category: {metrics['top_category']}")
        
        st.subheader("🌍 Sales by Region")
        sales_by_region = filtered_data.groupby("Region")["Sales"].sum().reset_index()
        fig_region = px.pie(sales_by_region, names="Region", values="Sales", hole=0.5)
        fig_region.update_layout(template="plotly_dark")
        st.plotly_chart(fig_region, use_container_width=True)
    
    with tab2:
        st.subheader("🔮 Customer Purchase Prediction")
        cust_select = st.selectbox("Select Customer", customer_df["Customer Name"])
        
        if st.button("🔮 Predict Purchase Again", use_container_width=True):
            cust_data = customer_df[customer_df["Customer Name"] == cust_select]
            if not cust_data.empty:
                input_vals = [[cust_data["Total Orders"].values[0], cust_data["Total Sales"].values[0]]]
                pred = model.predict(input_vals)[0]
                prob = model.predict_proba(input_vals)[0][1]
                
                if pred == 1:
                    st.success(f"✅ Likely to purchase again! ({prob:.1%} probability)")
                else:
                    st.error(f"❌ Unlikely to purchase again ({prob:.1%} probability)")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📊 Total Orders", cust_data["Total Orders"].values[0])
                with col2:
                    st.metric("💰 Total Sales", f"${cust_data['Total Sales'].values[0]:,.0f}")
                st.metric("🎯 Model Accuracy", f"{accuracy:.1%}")
            else:
                st.error("❌ No data for selected customer")
   
    with tab3:
        st.subheader("📈 Sales Forecast (Next 4 Years)")
        
        yearly_sales = data.groupby("year")["Sales"].sum().reset_index()
        last_year = yearly_sales["year"].max()
        future_years = np.array([[last_year + i] for i in range(1, 5)])
        predicted_sales = forecast_model.predict(future_years)
        
        forecast_df = pd.DataFrame({
            "Year": future_years.flatten(),
            "Predicted Sales": predicted_sales
        })
        
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(
            x=yearly_sales["year"], y=yearly_sales["Sales"],
            mode="lines+markers", name="Actual", line=dict(color='cyan')
        ))
        fig_forecast.add_trace(go.Scatter(
            x=forecast_df["Year"], y=forecast_df["Predicted Sales"],
            mode="lines+markers", name="Forecast", line=dict(color='orange', dash='dash')
        ))
        fig_forecast.update_layout(template="plotly_dark", title="Sales Forecast")
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        st.dataframe(forecast_df, use_container_width=True)
    
    
    with tab4:
        st.subheader("💬 Retail Sales Chatbot")
        
        CHAT_RESPONSES = {
            "total sales": lambda: f"💰 Total Sales: ${metrics['total_sales']:,.0f}",
            "top category": lambda: f"🏆 Top Category: {metrics['top_category']}",
            "total customers": lambda: f"👥 Total Customers: {metrics['total_customers']}",
            "total products": lambda: f"📦 Total Products: {metrics['total_products']}",
            "top product": lambda: filtered_data.groupby("Product Name")["Sales"].sum().idxmax(),
            "top customer": lambda: filtered_data.groupby("Customer Name")["Sales"].sum().idxmax(),
            "total orders": lambda: f"🧾 Total Orders: {metrics['total_orders']}"
        }
        
        user_input = st.text_input("💭 Ask about your sales data (e.g., 'total sales', 'top product')")
        if st.button("🤖 Get Answer", use_container_width=True) and user_input:
            query_lower = user_input.lower()
            response_found = False
            
            for key, func in CHAT_RESPONSES.items():
                if key in query_lower:
                    st.success(func())
                    response_found = True
                    break
            
            if not response_found:
                st.info("🤖 Try asking: 'total sales', 'top category', 'top product', 'total customers'...")
        
        st.info("🔧 **Pro Tip**: Filters update all charts & metrics in real-time!")

else:
    st.warning("👈 **Please upload your sales CSV file in the sidebar to get started!**")
    st.info("📊 **Supported format**: CSV with columns like Order ID, Order Date, Customer Name, Category, Sales, Region")

st.markdown("---")



        

