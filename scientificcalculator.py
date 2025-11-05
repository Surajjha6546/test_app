import streamlit as st
import math
from functools import partial

# ─────────────────────────────────────
# PAGE + THEME
# ─────────────────────────────────────
st.set_page_config(page_title="Casio fx-991EX | Streamlit", page_icon="🧮", layout="centered")

st.markdown("""
<style>
body {background: radial-gradient(circle at 30% 10%, #0b0f17 0%, #0a0d12 100%);}
.calc {
  max-width: 460px; margin: 40px auto; padding: 20px 20px 12px;
  background: linear-gradient(180deg,#0d141f,#0a111a);
  border-radius: 20px; border: 1px solid #1a2538;
  box-shadow: 0 0 30px rgba(0,255,213,.3);
}
.brand {text-align:center; color:#00ffd5; font-weight:800; font-size:20px;
  margin-bottom:10px; text-shadow:0 0 8px #00ffd5;}
.display {
  background:#000; color:#00ff9d; font-family:Consolas,monospace;
  font-size:30px; text-align:right; border-radius:10px;
  padding:12px; margin-bottom:8px; overflow-x:auto; border:1px solid #111;
}
.mem-status {font-size:13px; color:#7ee7ff; text-align:right; margin-bottom:12px;}
button[kind="secondary"] {
  height:48px; border-radius:10px; font-weight:600;
  border:1px solid #1c2636; color:#e8f9ff; background:#121a27;
}
.op   button[kind="secondary"] {border-color:#00ffa2;}
.func button[kind="secondary"] {border-color:#66a3ff;}
.eq   button[kind="secondary"] {border-color:#a8fddc;}
.dng  button[kind="secondary"] {border-color:#ff5f6a;}
.mem  button[kind="secondary"] {border-color:#ffaa00;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────
# STATE
# ─────────────────────────────────────
if "disp" not in st.session_state: st.session_state.disp = ""
if "mem" not in st.session_state:  st.session_state.mem  = 0.0
if "mode" not in st.session_state: st.session_state.mode = "DEG"  # DEG or RAD
if "mem_log" not in st.session_state: st.session_state.mem_log = []  # memory recall log

# ─────────────────────────────────────
# SAFE MATH + SANITIZER
# ─────────────────────────────────────
def trig_wrap(fn):
    if st.session_state.mode == "RAD":
        return lambda x: getattr(math, fn)(x)
    return lambda x: getattr(math, fn)(math.radians(x))

ALLOWED = {
    "sin": trig_wrap("sin"), "cos": trig_wrap("cos"), "tan": trig_wrap("tan"),
    "asin": lambda x: math.degrees(math.asin(x)) if st.session_state.mode=="DEG" else math.asin(x),
    "acos": lambda x: math.degrees(math.acos(x)) if st.session_state.mode=="DEG" else math.acos(x),
    "atan": lambda x: math.degrees(math.atan(x)) if st.session_state.mode=="DEG" else math.atan(x),
    "sqrt": math.sqrt, "log": math.log10, "ln": math.log, "exp": math.exp,
    "abs": abs, "fact": math.factorial, "pow": pow,
    "pi": math.pi, "e": math.e, "math": math
}

def sanitize(expr:str)->str:
    return (expr.replace("π","math.pi")
                .replace("√","math.sqrt")
                .replace("^","**")
                .replace("×","*")
                .replace("÷","/"))

# ─────────────────────────────────────
# ACTIONS
# ─────────────────────────────────────
def press(x):
    if st.session_state.disp == "Error": st.session_state.disp = ""
    st.session_state.disp += x
    st.rerun()

def clear():
    st.session_state.disp = ""
    st.rerun()

def backspace():
    st.session_state.disp = st.session_state.disp[:-1]
    st.rerun()

def evaluate():
    expr = sanitize(st.session_state.disp.strip())
    try:
        result = eval(expr, {"__builtins__": None}, ALLOWED)
        st.session_state.disp = str(result)
    except Exception:
        st.session_state.disp = "Error"
    st.rerun()

def toggle_mode():
    st.session_state.mode = "RAD" if st.session_state.mode == "DEG" else "DEG"
    st.rerun()

# Memory controls
def mem_add():
    try:
        val = eval(sanitize(st.session_state.disp or "0"), {"__builtins__": None}, ALLOWED)
        st.session_state.mem += float(val)
        st.session_state.mem_log.insert(0, f"M+ {val}")
    except: pass
    st.rerun()

def mem_sub():
    try:
        val = eval(sanitize(st.session_state.disp or "0"), {"__builtins__": None}, ALLOWED)
        st.session_state.mem -= float(val)
        st.session_state.mem_log.insert(0, f"M− {val}")
    except: pass
    st.rerun()

def mem_clear():
    st.session_state.mem = 0.0
    st.session_state.mem_log.insert(0, "MC")
    st.rerun()

def mem_recall():
    st.session_state.disp += str(st.session_state.mem)
    st.session_state.mem_log.insert(0, f"MR → {st.session_state.mem}")
    st.rerun()

# ─────────────────────────────────────
# UI STRUCTURE
# ─────────────────────────────────────
st.markdown("<div class='calc'>", unsafe_allow_html=True)
st.markdown("<div class='brand'>CASIO fx-991EX | Professional</div>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.disp or '0'}</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='mem-status'>Mode: {st.session_state.mode} | Memory: {st.session_state.mem:.4g}</div>",
    unsafe_allow_html=True
)

def row(buttons, cls=""):
    cols = st.columns(4)
    for i, (lbl, fn, key) in enumerate(buttons):
        if lbl == "": continue
        with cols[i]:
            cdiv = f"<div class='{cls}'>" 
            st.markdown(cdiv, unsafe_allow_html=True)
            st.button(lbl, key=key, on_click=fn)

# Memory row
row([("MC", mem_clear, "MC"), ("MR", mem_recall, "MR"),
     ("M+", mem_add, "M+"), ("M−", mem_sub, "M-")], "mem")

# Functions
row([("sin(", partial(press,"sin("), "sin"),
     ("cos(", partial(press,"cos("), "cos"),
     ("tan(", partial(press,"tan("), "tan"),
     ("√(", partial(press,"√("), "sqrt")], "func")

row([("log(", partial(press,"log("), "log"),
     ("ln(", partial(press,"ln("), "ln"),
     ("(", partial(press,"("), "("),
     (")", partial(press,")"), ")")], "func")

# Digits & ops (operators shown as symbols but compute as Python)
row([("7", partial(press,"7"), "7"),
     ("8", partial(press,"8"), "8"),
     ("9", partial(press,"9"), "9"),
     ("÷", partial(press,"÷"), "div")], "op")

row([("4", partial(press,"4"), "4"),
     ("5", partial(press,"5"), "5"),
     ("6", partial(press,"6"), "6"),
     ("×", partial(press,"×"), "mul")], "op")

row([("1", partial(press,"1"), "1"),
     ("2", partial(press,"2"), "2"),
     ("3", partial(press,"3"), "3"),
     ("−", partial(press,"−"), "sub")], "op")

row([("0", partial(press,"0"), "0"),
     (".", partial(press,"."), "."),
     ("^", partial(press,"^"), "^"),
     ("+", partial(press,"+"), "add")], "op")

# constants / factorial / equals
row([("π", partial(press,"π"), "pi"),
     ("e", partial(press,"e"), "e"),
     ("!", partial(press,"fact("), "fact"),
     ("=", evaluate, "eq")], "eq")

# last row
row([("C", clear, "C"),
     ("⌫", backspace, "back"),
     (f"{st.session_state.mode}", toggle_mode, "mode"),
     ("MR Log", lambda: None, "logbtn")], "dng")

st.markdown("</div>", unsafe_allow_html=True)

# Memory recall log (visible scroll)
with st.expander("🧠 Memory Recall History"):
    if st.session_state.mem_log:
        for entry in st.session_state.mem_log[:10]:
            st.write(entry)
    else:
        st.caption("No memory actions yet.")
