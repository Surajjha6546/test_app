import streamlit as st

# --- App Config ---
st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")

# --- Title ---
st.title("🧮 Simple Calculator")
st.write("Perform basic arithmetic operations easily.")

# --- User Inputs ---
num1 = st.number_input("Enter first number:", step=1.0, format="%.6f")
num2 = st.number_input("Enter second number:", step=1.0, format="%.6f")
operation = st.selectbox("Select Operation:", ("Addition", "Subtraction", "Multiplication", "Division"))

# --- Compute Result ---
if st.button("Calculate"):
    try:
        if operation == "Addition":
            result = num1 + num2
        elif operation == "Subtraction":
            result = num1 - num2
        elif operation == "Multiplication":
            result = num1 * num2
        elif operation == "Division":
            if num2 == 0:
                st.error("🚫 Division by zero is not allowed.")
                st.stop()
            result = num1 / num2
        st.success(f"✅ **Result:** {result:.6f}")
    except Exception as e:
        st.error(f"Error: {e}")
