import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("supply_chain_data.csv")
df.columns = df.columns.str.lower().str.replace(' ', '_')
df['shipping_cost_per_unit'] = df['shipping_costs'] / df['order_quantities']

# Sidebar filters
st.sidebar.header("Filters")
selected_supplier = st.sidebar.selectbox("Select Supplier", df['supplier_name'].unique())
selected_carrier = st.sidebar.selectbox("Select Carrier", df['shipping_carriers'].unique())

# Filter data
filtered_df = df[(df['supplier_name'] == selected_supplier) & (df['shipping_carriers'] == selected_carrier)]

# KPIs
st.title("📦 Supply Chain Performance Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered_df['revenue_generated'].sum():,.0f}")
col2.metric("Avg Defect Rate", f"{filtered_df['defect_rates'].mean():.2f}%")
col3.metric("Avg Lead Time", f"{filtered_df['lead_time'].mean():.1f} days")

# Chart 1: Revenue by Product Type
st.subheader("Revenue by Product Type")
fig1 = px.bar(filtered_df, x='product_type', y='revenue_generated', color='product_type')
st.plotly_chart(fig1)

# Chart 2: Shipping Cost per Unit by Carrier
st.subheader("Shipping Cost per Unit")
fig2 = px.box(df, x='shipping_carriers', y='shipping_cost_per_unit', color='shipping_carriers')
st.plotly_chart(fig2)

# Chart 3: Lead Time vs Defect Rate
st.subheader("Lead Time vs Defect Rate")
fig3 = px.scatter(filtered_df, x='lead_time', y='defect_rates', size='production_volumes', color='product_type',
                  hover_data=['sku'])
st.plotly_chart(fig3)
