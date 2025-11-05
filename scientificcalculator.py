import streamlit as st
import math

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Casio fx-991EX", page_icon="🧮", layout="centered")

st.markdown("""
<style>
body {background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);color:white;}
.calc-container {max-width:380px;margin:auto;padding:1rem;border-radius:20px;background:#111;box-shadow:0 0 20px #00ff99;}
.display {background:#000;color:#0f0;font-size:28px;text-align:right;padding:10px;border-radius:10px;margin-bottom:15px;}
button {width:100%;height:55px;font-size:18px;border:none;border-radius:8px;margin:3px;}
.btn-func {background:#444;color:#0ff;}
.btn-op {background:#00ff99;color:#000;font-weight:bold;}
.btn-num {background:#222;color:#fff;}
.btn-special {background:#ff4444;color:white;}
.btn-equal {background:#0f0;color:black;font-weight:bold;}
</style>
""", unsafe_allow_html=True)

# ---------------- STATE ----------------
if "display" not in st.session_state:
    st.session_state.display = ""
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- FUNCTIONS ----------------
def press(key):
    if key == "C":
        st.session_state.display = ""
    elif key == "⌫":
        st.session_state.display = st.session_state.display[:-1]
    elif key == "=":
        evaluate()
    else:
        st.session_state.display += key

def evaluate():
    expr = st.session_state.display
    expr = expr.replace("^", "**").replace("π", "math.pi").replace("√", "math.sqrt")
    try:
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
        st.session_state.history.insert(0, f"{expr} = {result}")
        st.session_state.history = st.session_state.history[:5]
        st.session_state.display = str(result)
    except Exception:
        st.session_state.display = "Error"

# ---------------- UI ----------------
st.markdown("<div class='calc-container'>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.display or 0}</div>", unsafe_allow_html=True)

# Button grid
layout = [
    ["sin(", "cos(", "tan(", "log("],
    ["ln(", "√(", "(", ")"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "^", "+"],
    ["π", "e", "x!", "="],
    ["C", "⌫"]
]

for row in layout:
    cols = st.columns(len(row))
    for i, label in enumerate(row):
        style = "btn-num"
        if label in ["sin(", "cos(", "tan(", "log(", "ln(", "√(", "π", "e", "x!"]:
            style = "btn-func"
        elif label in ["+", "-", "*", "/", "^"]:
            style = "btn-op"
        elif label == "=":
            style = "btn-equal"
        elif label in ["C", "⌫"]:
            style = "btn-special"
        cols[i].markdown(f"<button class='{style}' onClick='window.location.reload()'>{label}</button>", unsafe_allow_html=True)
        if st.button(label, key=label):
            if label == "x!":
                press("fact(")
            else:
                press(label)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- HISTORY ----------------
st.divider()
st.subheader("🧠 Replay Memory")
if not st.session_state.history:
    st.caption("No calculations yet.")
else:
    for entry in st.session_state.history:
        cols = st.columns([6, 1])
        cols[0].markdown(f"`{entry}`")
        if cols[1].button("↩", key=f"recall_{entry}"):
            st.session_state.display = entry.split("=")[0].strip()
            st.experimental_rerun()
