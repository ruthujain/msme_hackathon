import streamlit as st
import pandas as pd
import numpy as np

# Setting the page configuration
st.set_page_config(
    page_title="MSME Unified Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Financing", "Compliance", "ONDC Analytics", "Shipment Tracking"])

# Home Page
if page == "Home":
    st.title("Welcome to the MSME Unified Platform")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Revenue", "₹10,00,000", "+5%")
    with col2:
        st.metric("Pending Invoices", "₹2,00,000")
    with col3:
        st.metric("Available Credit", "₹3,00,000")

    st.write("### Notifications")
    notifications = ["Loan approved for ₹1,00,000", "Shipment #1234 delivered", "Pending compliance for Invoice #5678"]
    for note in notifications:
        st.write(f"- {note}")

# Financing Section
elif page == "Financing":
    st.title("Financing Options")
    
    st.write("Compare loan options from different funding sources:")
    
    # Sample financing data
    data = {
        "Lender": ["Bank A", "NBFC B", "P2P Platform C"],
        "Interest Rate (% APR)": [10.5, 12.0, 14.0],
        "Loan Term (Months)": [12, 24, 36],
        "Max Loan Amount (₹)": [500000, 300000, 200000],
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    
    st.write("### Apply for a Loan")
    loan_amount = st.number_input("Loan Amount (₹):", min_value=10000, max_value=500000, step=1000)
    loan_term = st.selectbox("Loan Term (Months):", [12, 24, 36])
    submit = st.button("Apply")
    if submit:
        st.success(f"Loan application for ₹{loan_amount} submitted successfully!")

# Compliance Section
elif page == "Compliance":
    st.title("Compliance Tools")
    
    st.write("### HSN Classification")
    product_description = st.text_input("Enter Product Description:")
    if product_description:
        hsn_code = "6110"  # Placeholder for HSN classification logic
        st.write(f"**Suggested HSN Code:** {hsn_code}")
    
    st.write("### Document Validation")
    uploaded_file = st.file_uploader("Upload Trade Document:")
    if uploaded_file:
        st.success("Document uploaded successfully and validated!")

# ONDC Analytics Section
elif page == "ONDC Analytics":
    st.title("ONDC Sales Analytics")
    
    st.write("### Sales Overview")
    sales_data = {
        "Product": ["Leather Wallet", "Belt", "Bag"],
        "Units Sold": [120, 75, 40],
        "Revenue (₹)": [60000, 37500, 20000],
    }
    sales_df = pd.DataFrame(sales_data)
    st.bar_chart(sales_df.set_index("Product"))

    st.write("### Top Buyers")
    buyers_data = pd.DataFrame({
        "Buyer Name": ["ABC Traders", "XYZ Stores", "Global Imports"],
        "Purchases (₹)": [45000, 30000, 20000],
    })
    st.dataframe(buyers_data, use_container_width=True)

    st.write("### Integration with ONDC")
    st.write("Fetching real-time sales and order updates from ONDC...")
    ondc_data = pd.DataFrame({
        "Order ID": ["ONDC1234", "ONDC5678", "ONDC91011"],
        "Status": ["Delivered", "Shipped", "Pending"],
        "Amount (₹)": [15000, 20000, 5000],
        "Buyer": ["ABC Traders", "XYZ Stores", "Global Imports"],
    })
    st.dataframe(ondc_data, use_container_width=True)

# Shipment Tracking Section
elif page == "Shipment Tracking":
    st.title("Shipment Tracking")
    
    st.write("### Track Your Shipments")
    shipment_id = st.text_input("Enter Shipment ID:")
    if shipment_id:
        st.write(f"Shipment ID {shipment_id} is currently **In Transit**.")
    
    st.write("### Recent Shipments")
    shipments = pd.DataFrame({
        "Shipment ID": ["1234", "5678", "91011"],
        "Status": ["Delivered", "In Transit", "Pending Pickup"],
        "Expected Delivery": ["2024-12-10", "2024-12-15", "2024-12-20"],
    })
    st.dataframe(shipments, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### Support")
st.sidebar.info("Contact us at support@msmeplatform.com")
