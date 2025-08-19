import streamlit as st

# Set page config
st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: black;
            color: white;
        }
        h1 {
            color: green;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1>🧮 Simple Calculator</h1>", unsafe_allow_html=True)

# Input fields
num1 = st.number_input("Enter first number:", step=1.0, format="%.2f")
num2 = st.number_input("Enter second number:", step=1.0, format="%.2f")

# Operation selection
operation = st.selectbox("Choose an operation:", ["Addition", "Subtraction", "Multiplication", "Division"])

# Perform calculation
result = None
if st.button("Calculate"):
    if operation == "Addition":
        result = num1 + num2
    elif operation == "Subtraction":
        result = num1 - num2
    elif operation == "Multiplication":
        result = num1 * num2
    elif operation == "Division":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("Error: Cannot divide by zero!")

# Display result
if result is not None:
    st.success(f"Result: {result:.2f}")

