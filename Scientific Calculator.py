import streamlit as st
import math

# -----------------------------------
# App Configuration
# -----------------------------------
st.set_page_config(page_title="Casio fx-991EX", page_icon="🧮", layout="centered")

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
        color: white;
        background-color: #1e1e1e;
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
st.caption("Built with Streamlit • Degree Mode • Python Powered")

# -----------------------------------
# Initialize Session State
# -----------------------------------
if "display" not in st.session_state:
    st.session_state.display = ""

# -----------------------------------
# Helper Functions
# -----------------------------------
def append(symbol):
    st.session_state.display += symbol

def clear_display():
    st.session_state.display = ""

def backspace():
    st.session_state.display = st.session_state.display[:-1]

def evaluate():
    expr = st.session_state.display
    expr = expr.replace("^", "**")
    expr = expr.replace("π", "math.pi").replace("√", "math.sqrt")

    try:
        # Safe evaluation scope
        allowed = {
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
            "pow": pow,
            "math": math
        }
        result = eval(expr, {"__builtins__": None}, allowed)
        st.session_state.display = str(result)
    except Exception:
        st.session_state.display = "Error"

# -----------------------------------
# Display Screen
# -----------------------------------
st.text_input("Display", value=st.session_state.display, key="display_box", disabled=True)

# -----------------------------------
# Buttons Layout
# -----------------------------------
button_layout = [
    ["sin(", "cos(", "tan(", "log("],
    ["ln(", "√(", "(", ")"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "^", "+"],
    ["π", "e", "x!", "="],
    ["C", "⌫"]
]

for row in button_layout:
    cols = st.columns(4)
    for i, label in enumerate(row):
        if label == "=":
            cols[i].button("=", on_click=evaluate)
        elif label == "C":
            cols[i].button("C", on_click=clear_display)
        elif label == "⌫":
            cols[i].button("⌫", on_click=backspace)
        elif label == "x!":
            cols[i].button("x!", on_click=append, args=("fact(",))
        elif label == "√(":
            cols[i].button("√", on_click=append, args=("√(",))
        elif label == "π":
            cols[i].button("π", on_click=append, args=("π",))
        elif label == "e":
            cols[i].button("e", on_click=append, args=("e",))
        elif label:
            cols[i].button(label, on_click=append, args=(label,))

st.caption("Mode: Degrees | Supports sin, cos, tan, log, ln, sqrt, factorial, π, e, powers, etc.")


