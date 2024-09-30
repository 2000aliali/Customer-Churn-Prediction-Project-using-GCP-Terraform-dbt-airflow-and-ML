import streamlit as st
import pandas as pd
import joblib

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        color: #4CAF50;
        text-align: center;
        font-weight: bold;
    }
    .sub-title {
        font-size: 22px;
        color: #0e76a8;
        text-align: center;
    }
    .prediction-positive {
        font-size: 24px;
        color: green;
        text-align: center;
        font-weight: bold;
    }
    .prediction-negative {
        font-size: 24px;
        color: red;
        text-align: center;
        font-weight: bold;
    }
    .input-container {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        color: #555;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Header
st.markdown('<div class="main-title">Customer Churn Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Predict whether a customer will exit based on the input features.</div>', unsafe_allow_html=True)

# Load the trained model
model = joblib.load('random_forest_model20.pkl')

# Load the saved label encoders
gender_encoder = joblib.load('gender_label_encoder21.pkl')
geography_encoder = joblib.load('geography_label_encoder20.pkl')

# Layout columns for input
st.markdown('<div class="input-container">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    credit_score = st.number_input('Credit Score', min_value=0, max_value=1000, step=1)
    geography = st.selectbox('Geography', options=['France', 'Germany', 'Spain'])  # List all possible categories
    gender = st.selectbox('Gender', options=['Male', 'Female'])
    age = st.number_input('Age', min_value=0, max_value=120, step=1)

with col2:
    tenure = st.number_input('Tenure (years)', min_value=0, max_value=10, step=1)
    balance = st.number_input('Balance', min_value=0.0, format="%.2f")
    num_of_products = st.number_input('Number of Products', min_value=1, max_value=4, step=1)
    has_cr_card = st.selectbox('Has Credit Card', options=[0, 1])  # 0 = No, 1 = Yes
    is_active_member = st.selectbox('Is Active Member', options=[0, 1])  # 0 = No, 1 = Yes
    estimated_salary = st.number_input('Estimated Salary', min_value=0.0, format="%.2f")

# End of input container
st.markdown('</div>', unsafe_allow_html=True)

# Preprocess the user input
# Apply label encoding for categorical features
geography_encoded = geography_encoder.transform([geography])[0]
gender_encoded = gender_encoder.transform([gender])[0]

# Create a DataFrame for prediction
data = {
    'creditscore': [credit_score],
    'geography': [geography_encoded],
    'gender': [gender_encoded],
    'age': [age],
    'tenure': [tenure],
    'balance': [balance],
    'numofproducts': [num_of_products],
    'hascrcard': [has_cr_card],
    'isactivemember': [is_active_member],
    'estimatedsalary': [estimated_salary]
}

processed_data = pd.DataFrame(data)

# Display the processed data (optional)
st.write("### Processed Input Data:")
st.dataframe(processed_data)

# Make predictions
if st.button('Predict'):
    prediction = model.predict(processed_data)
    if prediction[0] == 1:
        st.markdown('<div class="prediction-negative">The customer is predicted to exit.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="prediction-positive">The customer is predicted to stay.</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Customer Churn Prediction Dashboard</div>', unsafe_allow_html=True)
