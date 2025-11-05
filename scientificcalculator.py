import streamlit as st
import math
from functools import partial

# ──────────────────────────────────────────────────────────────
#  CONFIG + THEME
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Casio fx-991 | Streamlit", page_icon="🧮", layout="centered")

st.markdown("""
<style>
body {background:#0b0e13;}
.calc {max-width:420px;margin:auto;padding:24px;border-radius:20px;
background:linear-gradient(180deg,#0e141f,#0d1a26);box-shadow:0 0 25px #00ffd580;}
.title {text-align:center;color:#00ffd5;font-weight:700;font-size:20px;
margin-bottom:15px;text-shadow:0 0 8px #00ffd5;}
.display {background:#000;color:#0f0;font-family:monospace;
font-size:28px;padding:12px 10px;text-align:right;border-radius:10px;margin-bottom:10px;}
button[kind="secondary"] {height:46px;font-size:17px;border-radius:10px;font-weight:600;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
#  STATE
# ──────────────────────────────────────────────────────────────
if "disp" not in st.session_state: st.session_state.disp = ""
if "mem" not in st.session_state: st.session_state.mem = 0.0
if "mode" not in st.session_state: st.session_state.mode = "DEG"  # DEG or RAD

# ──────────────────────────────────────────────────────────────
#  SAFE EVAL FUNCTIONS
# ──────────────────────────────────────────────────────────────
def trig_wrap(func):
    if st.session_state.mode == "RAD":
        return lambda x: getattr(math, func)(x)
    return lambda x: getattr(math, func)(math.radians(x))

ALLOWED = {
    "sin":  trig_wrap("sin"), "cos":  trig_wrap("cos"), "tan":  trig_wrap("tan"),
    "asin": lambda x: math.degrees(math.asin(x)) if st.session_state.mode=="DEG" else math.asin(x),
    "acos": lambda x: math.degrees(math.acos(x)) if st.session_state.mode=="DEG" else math.acos(x),
    "atan": lambda x: math.degrees(math.atan(x)) if st.session_state.mode=="DEG" else math.atan(x),
    "sqrt": math.sqrt, "log": math.log10, "ln": math.log, "exp": math.exp,
    "abs": abs, "fact": math.factorial, "pow": pow,
    "pi": math.pi, "e": math.e, "math": math
}

def sanitize(expr:str)->str:
    return expr.replace("π","math.pi").replace("√","math.sqrt").replace("^","**")

# ──────────────────────────────────────────────────────────────
#  ACTIONS
# ──────────────────────────────────────────────────────────────
def press(x):
    if st.session_state.disp=="Error": st.session_state.disp=""
    st.session_state.disp += x
    st.rerun()

def clear(): st.session_state.disp=""; st.rerun()
def back(): st.session_state.disp=st.session_state.disp[:-1]; st.rerun()

def eval_expr():
    expr = sanitize(st.session_state.disp)
    try:
        result = eval(expr, {"__builtins__": None}, ALLOWED)
        st.session_state.disp = str(result)
    except Exception:
        st.session_state.disp = "Error"
    st.rerun()

def mem_add(): st.session_state.mem += float(eval(sanitize(st.session_state.disp),{"__builtins__":None},ALLOWED) or 0); st.rerun()
def mem_sub(): st.session_state.mem -= float(eval(sanitize(st.session_state.disp),{"__builtins__":None},ALLOWED) or 0); st.rerun()
def mem_recall(): st.session_state.disp += str(st.session_state.mem); st.rerun()
def mem_clear(): st.session_state.mem=0.0; st.rerun()

def toggle_mode():
    st.session_state.mode = "RAD" if st.session_state.mode=="DEG" else "DEG"
    st.rerun()

# ──────────────────────────────────────────────────────────────
#  DISPLAY + UI
# ──────────────────────────────────────────────────────────────
st.markdown("<div class='calc'>", unsafe_allow_html=True)
st.markdown("<div class='title'>CASIO fx-991 | Ultra-Fast</div>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.disp or '0'}</div>", unsafe_allow_html=True)

# button rows (always 4 per row)
rows = [
    [("MC",mem_clear),("MR",mem_recall),("M+",mem_add),("M-",mem_sub)],
    [("sin(",partial(press,"sin(")),("cos(",partial(press,"cos(")),("tan(",partial(press,"tan(")),("√(",partial(press,"√("))],
    [("log(",partial(press,"log(")),("ln(",partial(press,"ln(")),(("(",partial(press,"("))),((")",partial(press,")")))],
    [("7",partial(press,"7")),("8",partial(press,"8")),("9",partial(press,"9")),("/",partial(press,"/"))],
    [("4",partial(press,"4")),("5",partial(press,"5")),("6",partial(press,"6")),("*",partial(press,"*"))],
    [("1",partial(press,"1")),("2",partial(press,"2")),("3",partial(press,"3")),("-",partial(press,"-"))],
    [("0",partial(press,"0")),(".",partial(press,".")),("^",partial(press,"^")),( "+",partial(press,"+"))],
    [("π",partial(press,"π")),("e",partial(press,"e")),("!",partial(press,"fact(")),("=",eval_expr)],
    [("C",clear),(st.session_state.mode,toggle_mode),("⌫",back)]
]

for i,row in enumerate(rows):
    cols = st.columns(4)
    for j,(lbl,action) in enumerate(row):
        if lbl=="": continue
        cols[j].button(lbl,key=f"{i}_{j}_{lbl}",on_click=action)

st.markdown("</div>", unsafe_allow_html=True)
st.caption(f"Mode: {st.session_state.mode} | Supports sin, cos, tan, log, ln, √, ^, π, e, factorial, memory, and DEG/RAD toggle.")
