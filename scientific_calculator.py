import streamlit as st
import math

# Set page config
st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: white;
            color: black;
        }
        h1 {
            color: black;
            text-align: center;
        }
        .button-grid {
            display: grid;
            grid-template-columns: repeat(4, 80px);
            gap: 10px;
            justify-content: center;
            text-align: center;
        }
        .button {
            width: 80px;
            height: 50px;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            background-color: #ddd;
            color: black;
            border: 2px solid black;
            border-radius: 5px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #bbb;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1>🧮 Scientific Calculator</h1>", unsafe_allow_html=True)

# Calculator display
calculation = st.text_input("Calculation:", value="", key="calc_display")

# Define button layout
number_pad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["0", ".", "C"]
]

operators = ["/", "*", "-", "+", "="]
functions = ["√", "^", "log", "sin", "cos", "tan"]

# Display number pad
st.markdown('<div class="button-grid">', unsafe_allow_html=True)
for row in number_pad:
    cols = st.columns(3)
    for i, button in enumerate(row):
        if cols[i].button(button):
            if button == "C":
                calculation = ""
            else:
                calculation += button

st.markdown("</div>", unsafe_allow_html=True)

# Display operators
st.markdown('<div class="button-grid">', unsafe_allow_html=True)
cols = st.columns(5)
for i, button in enumerate(operators):
    if cols[i].button(button):
        if button == "=":
            try:
                calculation = calculation.replace("√", "math.sqrt")
                calculation = calculation.replace("^", "**")
                calculation = calculation.replace("log", "math.log")
                calculation = calculation.replace("sin", "math.sin(math.radians")
                calculation = calculation.replace("cos", "math.cos(math.radians")
                calculation = calculation.replace("tan", "math.tan(math.radians")

                result = eval(calculation + (")" if calculation.endswith("(") else ""))
                st.success(f"Result: {result}")
            except Exception as e:
                st.error("Invalid Calculation")
        else:
            calculation += button

st.markdown("</div>", unsafe_allow_html=True)

# Display function buttons
st.markdown('<div class="button-grid">', unsafe_allow_html=True)
cols = st.columns(6)
for i, button in enumerate(functions):
    if cols[i].button(button):
        calculation += button

st.markdown("</div>", unsafe_allow_html=True)

# Update display
st.session_state.calc_display = calculation
