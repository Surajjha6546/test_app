import streamlit as st
import math

# -------------------------------
# Streamlit App Configuration
# -------------------------------
st.set_page_config(page_title="Casio fx-991EX Calculator", page_icon="🧮", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(145deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .stTextInput > div > div > input {
        text-align: right;
        font-size: 24px;
        height: 3em;
        border-radius: 10px;
    }
    .stButton>button {
        width: 100%;
        height: 3em;
        font-size: 18px;
        border-radius: 8px;
        background: #333;
        color: white;
        border: 1px solid #00ff99;
    }
    .stButton>button:hover {
        background: #00ff99;
        color: black;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧮 Casio fx-991EX — Scientific Calculator")
st.caption("Built with Streamlit • Python-powered • Degree mode")

# -------------------------------
# Initialize Session State
# -------------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""

# -------------------------------
# Helper Functions
# -------------------------------
def append_symbol(symbol: str):
    st.session_state.expression += symbol

def clear_expression():
    st.session_state.expression = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def evaluate_expression():
    expr = st.session_state.expression.replace("^", "**")
    try:
        # Safe math evaluation
        result = eval(expr, {"__builtins__": None}, {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "asin": lambda x: math.degrees(math.asin(x)),
            "acos": lambda x: math.degrees(math.acos(x)),
            "atan": lambda x: math.degrees(math.atan(x)),
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "fact": math.factorial,
            "pow": pow
        })
        st.session_state.expression = str(result)
    except Exception:
        st.session_state.expression = "Error"

# -------------------------------
# Display
# -------------------------------
st.text_input("Display", st.session_state.expression, key="display", disabled=True)

# -------------------------------
# Button Layout (Casio-like)
# -------------------------------
buttons = [
    ["sin(", "cos(", "tan(", "log("],
    ["√(", "ln(", "(", ")",],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "^", "+"],
    ["π", "e", "x!", "="],
    ["C", "⌫", "", ""]
]

for row in buttons:
    cols = st.columns(4)
    for i, label in enumerate(row):
        if not label:
            continue

        if label == "=":
            cols[i].button("=", on_click=evaluate_expression)
        elif label == "C":
            cols[i].button("C", on_click=clear_expression)
        elif label == "⌫":
            cols[i].button("⌫", on_click=backspace)
        elif label == "π":
            cols[i].button("π", on_click=append_symbol, args=("math.pi",))
        elif label == "e":
            cols[i].button("e", on_click=append_symbol, args=("math.e",))
        elif label == "√(":
            cols[i].button("√", on_click=append_symbol, args=("sqrt(",))
        elif label == "x!":
            cols[i].button("x!", on_click=append_symbol, args=("fact(",))
        else:
            cols[i].button(label, on_click=append_symbol, args=(label,))

st.caption("Mode: Degrees | Functions: sin, cos, tan, log, ln, sqrt, factorial, exp, π, e")

