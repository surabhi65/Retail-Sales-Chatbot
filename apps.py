import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="DataForge Analytics",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* MAIN BACKGROUND */
.main { background: linear-gradient(135deg, #0E1117 0%, #1A1F2E 100%); }

section[data-testid="stSidebar"] { 
    background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
    border-right: 1px solid #0ea5e9;
}
.metric-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2) !important;
    padding: 20px !important; 
    border-radius: 15px !important;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    border: 1px solid rgba(255,255,255,0.1);
    transition: all 0.3s ease;
}
.metric-container:hover { 
    transform: translateY(-3px); 
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4); 
}
section[data-testid="stSidebar"] h3 { 
    color: #0ea5e9 !important; 
    font-weight: 700 !important;
    text-shadow: 0 0 10px rgba(14, 165, 233, 0.5);
}
section[data-testid="stSidebar"] label { 
    color: #e0f2fe !important; 
    font-weight: 500 !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    border: 2px solid #0369a1 !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] .stSlider > div > div > div {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] div[role="combobox"] {
    background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
    border: 2px solid #0369a1 !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def smart_load_any_file(uploaded_file):
    """🚀 DataForge file loader - enterprise-grade"""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        if df.columns.duplicated().any():
            cols = list(df.columns)
            seen = {}
            for i, col in enumerate(cols):
                base = col
                counter = 1
                while col in seen:
                    col = f"{base}_{counter}"
                    counter += 1
                seen[col] = True
                cols[i] = col
            df.columns = cols
        
        df.columns = (df.columns.astype(str)
                     .str.lower().str.strip()
                     .str.replace(' ', '_')
                     .str.replace('-', '_')
                     .str.replace('[()]', '', regex=True)
                     .str.replace('.', '_'))
        return df
    except Exception as e:
        st.error(f"❌ File error: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def detect_columns(df):
    """🔍 Auto-detect column types"""
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    return numeric_cols, categorical_cols

@st.cache_data
def detect_date_column(df):
    """📅 Smart date detection"""
    for col in df.columns:
        if any(x in col for x in ["date", "month", "year", "time"]):
            try:
                pd.to_datetime(df[col], errors='coerce')
                return col
            except:
                continue
    return None

st.sidebar.markdown("# 🔥 **DataForge Analytics**")
uploaded_file = st.sidebar.file_uploader(
    "📁 Upload CSV/Excel", 
    type=['csv', 'xlsx', 'xls']
)

if uploaded_file:
    with st.spinner("🔥 DataForge Analysis Engine Active..."):
        raw_df = smart_load_any_file(uploaded_file)
    
    if not raw_df.empty:
        numeric_cols, categorical_cols = detect_columns(raw_df)
        date_col = detect_date_column(raw_df)
        
        if not numeric_cols:
            st.error("❌ No numeric columns. Upload data with numbers.")
            st.stop()
        
        metric_col = st.sidebar.selectbox(
            "📊 Main Metric", numeric_cols, index=0
        )
        
        st.sidebar.markdown("## 🔎 **Enterprise Filters**")
        df = raw_df.copy()
        
        for col in categorical_cols[:5]:
            unique_vals = df[col].dropna().unique()
            if len(unique_vals) <= 50:
                selected_vals = st.sidebar.multiselect(
                    f"{col.title()}",
                    options=unique_vals,
                    default=unique_vals[:3]
                )
                if selected_vals:
                    df = df[df[col].isin(selected_vals)]
        
        for col in numeric_cols[:3]:
            if col != metric_col:
                min_val, max_val = float(df[col].min()), float(df[col].max())
                if min_val != max_val:
                    selected_range = st.sidebar.slider(
                        f"{col.title()} Range",
                        min_value=min_val, max_value=max_val,
                        value=(min_val, max_val),
                        step=(max_val-min_val)/100
                    )
                    df = df[(df[col] >= selected_range[0]) & (df[col] <= selected_range[1])]
        
        st.markdown("### 🔥 **DataForge Analytics Platform**")
        st.caption("🚀 Universal CSV/Excel → Instant Executive Intelligence")
        
        total_value = df[metric_col].sum()
        growth_pct = None
        
        if date_col and metric_col and len(df) > 1:
            try:
                trend_df = df.groupby(date_col)[metric_col].sum().reset_index()
                trend_df = trend_df.sort_values(date_col)
                if len(trend_df) >= 2:
                    current = trend_df.iloc[-1][metric_col]
                    previous = trend_df.iloc[-2][metric_col]
                    if previous != 0:
                        growth_pct = ((current - previous) / previous) * 100
            except:
                pass
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(f"💰 {metric_col.title()}", f"{total_value:,.0f}",
                     delta=f"{growth_pct:.1f}%" if growth_pct else None)
        with col2: st.metric("📊 Filtered Rows", f"{len(df):,}")
        with col3: st.metric("🎯 Categories", f"{len(categorical_cols)}")
        with col4: st.metric("📈 Quality", f"{(1-df.isnull().mean().mean())*100:.1f}%")
        
        st.divider()
        col_export, _ = st.columns([1, 4])
        with col_export:
            csv_filtered = df.to_csv(index=False).encode('utf-8')
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M')
            st.download_button(label="💾 Export Clean Data",data=csv_filtered,file_name=f"dataforge_filtered_{timestamp}.csv",mime="text/csv")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🥧 Contribution", "🏆 Leaderboard", "🔍 Intelligence"])
        
        with tab1:
            if date_col and metric_col:
                trend_df = df.groupby(date_col)[metric_col].sum().reset_index()
                fig = px.line(trend_df.sort_values(date_col), x=date_col, y=metric_col,
                            title=f"📈 {metric_col.title()} Trend", markers=True)
                fig.update_layout(template="plotly_dark", height=500)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📅 Date column needed for trends")
        
        with tab2:
            if categorical_cols:
                contrib_col = st.selectbox("🏷️ By:", categorical_cols)
                contrib_df = (df.groupby(contrib_col)[metric_col].sum()
                             .reset_index().sort_values(metric_col, ascending=False).head(15))
                
                fig = px.pie(contrib_df, names=contrib_col, values=metric_col,
                           hole=0.4, title=f"🥧 {contrib_col.title()} Share")
                fig.update_traces(textinfo='percent+label')
                fig.update_layout(template="plotly_dark", height=500)
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(contrib_df)
        
        with tab3:
            if categorical_cols:
                rank_col = st.selectbox("🏆 Rank:", categorical_cols, key="rank")
                order = st.radio("Show:", ["Top 10", "Bottom 10"], horizontal=True)
                
                rank_df = df.groupby(rank_col)[metric_col].sum().reset_index()
                n = 10
                
                if order == "Top 10":
                    rank_df = rank_df.nlargest(n, metric_col)
                else:
                    rank_df = rank_df.nsmallest(n, metric_col)
                
                fig = px.bar(rank_df, x=metric_col, y=rank_col, orientation='h',
                           title=f"{order} {rank_col.title()}", text=metric_col)
                fig.update_layout(template="plotly_dark", height=500,
                               yaxis_categoryorder='array', 
                               yaxis_categoryarray=rank_df[rank_col].tolist())
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(rank_df.round(2))
        
        with tab4:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔍 Missing Values")
                missing = df.isnull().sum()
                missing_cols = missing[missing > 0].sort_values(ascending=False)
                
                if len(missing_cols) > 0:
                    total_missing = missing_cols.sum()
                    total_cells = len(df) * len(df.columns)
                    completeness_pct = (1 - total_missing/total_cells) * 100
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("🚨 Total Missing", f"{total_missing:,}")
                    with col_b:
                        st.metric("📊 %  Complete", f"{completeness_pct:.1f}%")
                    
                    missing_df = missing_cols.reset_index().rename(columns={0: "Count"})
                    st.dataframe(missing_df, use_container_width=True)
                    
                    if len(missing_cols) > 0:
                        top_missing_col = missing_cols.index[0]
                        available_cols = ['product_id', 'product_name', top_missing_col, 'category']
                        safe_cols = [col for col in df.columns if col in available_cols]
                        
                        if len(safe_cols) >= 2:  
                            sample_rows = df[df[top_missing_col].isnull()][safe_cols].head(5)
                            with st.expander(f"📋 Sample rows missing '{top_missing_col}' ({len(df[df[top_missing_col].isnull()])} rows)"):
                                st.dataframe(sample_rows)
                        else:
                            st.info("⚠️ Can't show sample rows - insufficient columns")
                else:
                    st.success("✅ Perfect data! No missing values found.")
            
            with col2:
                st.subheader("📊 Summary Statistics")
                desc = df.describe().round(2)
                st.dataframe(desc, use_container_width=True)
                
                st.subheader("🏷️ Column Types")
                dtype_df = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes,
                    'Non-Null': [f"{len(df)-df[col].isnull().sum():,}" for col in df.columns],
                    'Missing': [f"{df[col].isnull().sum():,}" for col in df.columns]
                })
                st.dataframe(dtype_df, use_container_width=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem;">
        <h1 style="color: #0ea5e9; font-size: 4rem; margin-bottom: 1rem; text-shadow: 0 0 20px rgba(14,165,233,0.5);">
            🔥 DataForge Analytics
        </h1>
        <h2 style="color: #fff; font-size: 2rem; margin-bottom: 2rem;">
            Universal Enterprise Intelligence
        </h2>
        <p style="color: #aaa; font-size: 1.4rem; max-width: 700px; margin: 0 auto;">
            🚀 Upload ANY CSV/Excel → Instant executive dashboard with AI-powered insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### ✨ **Production Features**
    - **💎 Light Blue Enterprise Filters** - Auto-generated
    - **📈 Real Growth Tracking** - Live deltas  
    - **🔥 Universal Loading** - Any messy CSV/Excel
    - **⚡ Cached Performance** - Enterprise speed
    - **💾 Timestamped Exports** - Production ready
    - **🔍 Enhanced Data Quality** - Missing values analysis + samples
    """)
