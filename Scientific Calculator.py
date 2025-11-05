import streamlit as st
import math

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Scientific Calculator (Casio fx-991)", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #111, #222);
        color: white;
        font-family: 'Consolas', monospace;
    }
    h1, h2, h3, h4 {
        text-align: center;
        color: #00ff99;
    }
    .stButton>button {
        width: 100%;
        background: #333;
        color: white;
        border-radius: 8px;
        border: 1px solid #00ff99;
    }
    .stButton>button:hover {
        background: #00ff99;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Casio fx-991EX — Scientific Calculator")
st.caption("Built with Streamlit & Python — emulate Casio logic and precision")

# --- Input ---
expression = st.text_input("Enter expression:", placeholder="e.g. sin(30) + log(10) + 5^2")

# --- Function mapping (safe eval replacement) ---
allowed_funcs = {
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
    "fact": math.factorial,
    "abs": abs,
    "pow": pow
}

# --- Safe Evaluator ---
def evaluate_expression(expr):
    try:
        expr = expr.replace("^", "**")  # handle power symbol
        # Replace function names safely
        for name in allowed_funcs.keys():
            if name in expr:
                expr = expr.replace(name, f"allowed_funcs['{name}']")
        result = eval(expr, {"__builtins__": None}, {"allowed_funcs": allowed_funcs})
        return result
    except Exception as e:
        return f"Error: {e}"

# --- Calculate Button ---
if st.button("Calculate"):
    if expression.strip() == "":
        st.warning("Enter a valid expression.")
    else:
        output = evaluate_expression(expression)
        st.success(f"**Result:** {output}")

# --- Quick Buttons ---
st.divider()
st.subheader("Common Operations")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("π"):
        st.session_state["expression"] = expression + "pi"
with col2:
    if st.button("e"):
        st.session_state["expression"] = expression + "e"
with col3:
    if st.button("sin()"):
        st.session_state["expression"] = expression + "sin()"
with col4:
    if st.button("√"):
        st.session_state["expression"] = expression + "sqrt()"

# Memory Section
st.divider()
st.subheader("🧠 Memory Functions")
if "memory" not in st.session_state:
    st.session_state.memory = 0.0

mcol1, mcol2, mcol3, mcol4 = st.columns(4)
with mcol1:
    if st.button("M+"):
        try:
            st.session_state.memory += float(evaluate_expression(expression))
            st.success(f"Memory: {st.session_state.memory}")
        except:
            st.error("Invalid for M+")
with mcol2:
    if st.button("M-"):
        try:
            st.session_state.memory -= float(evaluate_expression(expression))
            st.success(f"Memory: {st.session_state.memory}")
        except:
            st.error("Invalid for M-")
with mcol3:
    if st.button("MR"):
        st.info(f"Memory Recall: {st.session_state.memory}")
with mcol4:
    if st.button("MC"):
        st.session_state.memory = 0.0
        st.info("Memory Cleared")

st.caption("⚡ Powered by Streamlit • Designed to mimic Casio fx-991EX logic")
