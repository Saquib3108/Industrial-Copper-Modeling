import streamlit as st
import pickle
import numpy as np
from streamlit_option_menu import option_menu

# Function to predict status (Won/Lose)
def predict_status(ctry, itmtp, aplcn, wth, prdrf, qtlg, cstlg, tknslg, slgplg, itmdt, itmmn, itmyr, deldtdy, deldtmn, deldtyr):
    # Convert date components from string to int
    itdd, itdm, itdy = int(itmdt), int(itmmn), int(itmyr)
    dydd, dydm, dydy = int(deldtdy), int(deldtmn), int(deldtyr)

    # Load the classification model
    with open("C:/Users/DELL/Documents/Capstone Project/classification_model.pkl", "rb") as f:
        model_class = pickle.load(f)

    # Create input data array
    user_data = np.array([[ctry, itmtp, aplcn, wth, prdrf, qtlg, cstlg, tknslg, slgplg, itdd, itdm, itdy, dydd, dydm, dydy]])
    
    # Predict probabilities for each class
    y_pred_prob = model_class.predict_proba(user_data)
    
    # Define threshold for considering a status as "lost"
    lost_threshold = 0.5
    
    # Return status based on probability threshold
    return "lost" if y_pred_prob[0][0] > lost_threshold else "won"

# Function to predict selling price
def predict_selling_price(ctry, sts, itmtp, aplcn, wth, prdrf, qtlg, cstlg, tknslg, itmdt, itmmn, itmyr, deldtdy, deldtmn, deldtyr):
    # Convert date components from string to int
    itdd, itdm, itdy = int(itmdt), int(itmmn), int(itmyr)
    dydd, dydm, dydy = int(deldtdy), int(deldtmn), int(deldtyr)

    # Load the regression model
    with open("C:/Users/DELL/Documents/Capstone Project/regression_model.pkl", "rb") as f:
        model_regg = pickle.load(f)
        
    # Create input data array
    user_data = np.array([[ctry, sts, itmtp, aplcn, wth, prdrf, qtlg, cstlg, tknslg, itdd, itdm, itdy, dydd, dydm, dydy]])
    
    # Predict the selling price
    y_pred = model_regg.predict(user_data)
    ac_y_pred = np.exp(y_pred[0])
    
    return ac_y_pred

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Main title
st.title(":blue[**INDUSTRIAL COPPER MODELING**]")

# Sidebar menu
with st.sidebar:
    option = option_menu('MAIN MENU', options=["PREDICT SELLING PRICE", "PREDICT STATUS"])

if option == "PREDICT STATUS":
    st.header("PREDICT STATUS (Won / Lose)")
    st.write(" ")

    col1, col2 = st.columns(2)
    
    with col1:
        country = st.number_input("Enter the Value for COUNTRY", min_value=25.0, max_value=113.0)
        item_type = st.number_input("Enter the Value for ITEM TYPE", min_value=0.0, max_value=6.0)
        application = st.number_input("Enter the Value for APPLICATION", min_value=2.0, max_value=87.5)
        width = st.number_input("Enter the Value for WIDTH", min_value=700.0, max_value=1980.0)
        product_ref = st.number_input("Enter the Value for PRODUCT_REF", min_value=611728, max_value=1722207579)
        quantity_tons_log = st.number_input("Enter the Value for QUANTITY_TONS (Log Value)", min_value=-0.322, max_value=6.924, format="%0.15f")
        customer_log = st.number_input("Enter the Value for CUSTOMER (Log Value)", min_value=17.21910, max_value=17.23015, format="%0.15f")
        thickness_log = st.number_input("Enter the Value for THICKNESS (Log Value)", min_value=-1.71479, max_value=3.28154, format="%0.15f")
    
    with col2:
        selling_price_log = st.number_input("Enter the Value for SELLING PRICE (Log Value)", min_value=5.97503, max_value=7.39036, format="%0.15f")
        item_date_day = st.selectbox("Select the Day for ITEM DATE", [str(i) for i in range(1, 32)])
        item_date_month = st.selectbox("Select the Month for ITEM DATE", [str(i) for i in range(1, 13)])
        item_date_year = st.selectbox("Select the Year for ITEM DATE", ["2020", "2021"])
        delivery_date_day = st.selectbox("Select the Day for DELIVERY DATE", [str(i) for i in range(1, 32)])
        delivery_date_month = st.selectbox("Select the Month for DELIVERY DATE", [str(i) for i in range(1, 13)])
        delivery_date_year = st.selectbox("Select the Year for DELIVERY DATE", ["2020", "2021", "2022"])
        
    button = st.button(":violet[***PREDICT THE STATUS***]", use_container_width=True)
    
    if button:
        status = predict_status(country, item_type, application, width, product_ref, quantity_tons_log,
                            customer_log, thickness_log, selling_price_log, item_date_day,
                            item_date_month, item_date_year, delivery_date_day, delivery_date_month,
                            delivery_date_year)
    
        if status == "won":
            st.write("## :green[**The Status is WON**]")
        else:
            st.write("## :red[**The Status is LOSE**]")

if option == "PREDICT SELLING PRICE":
    st.header("PREDICT SELLING PRICE")
    st.write(" ")

    col1, col2 = st.columns(2)
    
    with col1:
        country = st.number_input("Enter the Value for COUNTRY", min_value=25.0, max_value=113.0)
        status = st.number_input("Enter the Value for STATUS", min_value=0.0, max_value=8.0)
        item_type = st.number_input("Enter the Value for ITEM TYPE", min_value=0.0, max_value=6.0)
        application = st.number_input("Enter the Value for APPLICATION", min_value=2.0, max_value=87.5)
        width = st.number_input("Enter the Value for WIDTH", min_value=700.0, max_value=1980.0)
        product_ref = st.number_input("Enter the Value for PRODUCT_REF", min_value=611728, max_value=1722207579)
        quantity_tons_log = st.number_input("Enter the Value for QUANTITY_TONS (Log Value)", min_value=-0.322, max_value=6.924, format="%0.15f")
        customer_log = st.number_input("Enter the Value for CUSTOMER (Log Value)", min_value=17.21910565821408, max_value=17.230155364880137, format="%0.15f")
        
    with col2:
        thickness_log = st.number_input("Enter the Value for THICKNESS (Log Value)", min_value=-1.7147984280919266, max_value=3.281543137578373, format="%0.15f")
        item_date_day = st.selectbox("Select the Day for ITEM DATE", [str(i) for i in range(1, 32)])
        item_date_month = st.selectbox("Select the Month for ITEM DATE", [str(i) for i in range(1, 13)])
        item_date_year = st.selectbox("Select the Year for ITEM DATE", ["2020", "2021"])
        delivery_date_day = st.selectbox("Select the Day for DELIVERY DATE", [str(i) for i in range(1, 32)])
        delivery_date_month = st.selectbox("Select the Month for DELIVERY DATE", [str(i) for i in range(1, 13)])
        delivery_date_year = st.selectbox("Select the Year for DELIVERY DATE", ["2020", "2021", "2022"])

    button = st.button(":violet[***PREDICT THE SELLING PRICE***]", use_container_width=True)
    
    if button:
        price = predict_selling_price(country, status, item_type, application, width, product_ref, quantity_tons_log,
                                   customer_log, thickness_log, item_date_day,
                                   item_date_month, item_date_year, delivery_date_day, delivery_date_month,
                                   delivery_date_year)
        
        st.write("## :green[**The Selling Price is :**]", price)