import math
import streamlit as st
from functools import partial

# ───────────────── config/theme ─────────────────
st.set_page_config(page_title="Casio fx-991 — Streamlit", page_icon="🧮", layout="centered")

st.markdown("""
<style>
:root{
  --bg:#0b0f16; --panel:#0e1420; --ink:#e5f4ff;
  --accent:#00ffd5; --btn:#121a28; --grid:#1a2335;
  --op:#17f0a6; --func:#67a8ff; --warn:#ff5d6c; --eq:#a4f9d6;
}
body {background: var(--bg);}
.calc {
  max-width: 460px; margin: 24px auto; padding: 18px 18px 12px;
  border-radius: 18px; background: linear-gradient(180deg,#0d1422,#0a121c);
  border: 1px solid var(--grid); box-shadow: 0 0 24px rgba(0,255,213,.25);
}
.brand { text-align:center; color: var(--accent); font-weight: 800; letter-spacing:.4px;
  text-shadow: 0 0 10px rgba(0,255,213,.6); margin-bottom: 10px; }
.display {
  background:#000; color:#adff9a; font-family: ui-monospace, Menlo, Consolas, monospace;
  font-size: 28px; padding: 12px 12px; text-align:right; border-radius: 10px;
  border: 1px solid var(--grid); overflow-x:auto; white-space:nowrap; margin-bottom: 10px;
}
.note { color:#9fb1c7; font-size:12px; text-align:right; margin-bottom: 10px; }

button[kind="secondary"]{
  width:100%; height:48px; border-radius: 10px; font-weight: 700; letter-spacing:.3px;
  border:1px solid var(--grid); background: var(--btn); color: var(--ink);
}
.op   button[kind="secondary"]{ border-color: var(--op);   }
.func button[kind="secondary"]{ border-color: var(--func); }
.eq   button[kind="secondary"]{ border-color: var(--eq);   }
.dng  button[kind="secondary"]{ border-color: var(--warn); }
</style>
""", unsafe_allow_html=True)

# ──────────────── state ────────────────
if "disp" not in st.session_state: st.session_state.disp = ""
if "mem"  not in st.session_state: st.session_state.mem  = 0.0
if "mode" not in st.session_state: st.session_state.mode = "DEG"  # DEG | RAD

# ──────────────── math helpers (safe) ────────────────
def trig_wrap(fn):
    if st.session_state.mode == "RAD":
        return lambda x: getattr(math, fn)(x)
    return lambda x: getattr(math, fn)(math.radians(x))

ALLOWED = {
    "sin": trig_wrap("sin"), "cos": trig_wrap("cos"), "tan": trig_wrap("tan"),
    "asin": (lambda x: math.degrees(math.asin(x)) if st.session_state.mode=="DEG" else math.asin(x)),
    "acos": (lambda x: math.degrees(math.acos(x)) if st.session_state.mode=="DEG" else math.acos(x)),
    "atan": (lambda x: math.degrees(math.atan(x)) if st.session_state.mode=="DEG" else math.atan(x)),
    "sqrt": math.sqrt, "log": math.log10, "ln": math.log, "exp": math.exp,
    "abs": abs, "fact": math.factorial, "pow": pow,
    "pi": math.pi, "e": math.e, "math": math,
}

def sanitize(expr:str)->str:
    return (expr.replace("π","math.pi")
                .replace("√","math.sqrt")
                .replace("^","**")
                .replace("×","*")
                .replace("÷","/"))

# ──────────────── actions ────────────────
def press(token:str):
    if st.session_state.disp == "Error": st.session_state.disp = ""
    st.session_state.disp += token
    st.rerun()

def clear(): st.session_state.disp = ""; st.rerun()
def back():  st.session_state.disp = st.session_state.disp[:-1]; st.rerun()

def evaluate():
    expr = sanitize(st.session_state.disp.strip())
    if not expr:
        return
    try:
        result = eval(expr, {"__builtins__": None}, ALLOWED)
        st.session_state.disp = str(result)
    except Exception:
        st.session_state.disp = "Error"
    st.rerun()

def mem_add():
    try:
        val = eval(sanitize(st.session_state.disp or "0"), {"__builtins__": None}, ALLOWED)
        st.session_state.mem += float(val)
    except Exception:
        pass
    st.rerun()

def mem_sub():
    try:
        val = eval(sanitize(st.session_state.disp or "0"), {"__builtins__": None}, ALLOWED)
        st.session_state.mem -= float(val)
    except Exception:
        pass
    st.rerun()

def mem_recall():  # MR — append to display
    st.session_state.disp += str(st.session_state.mem)
    st.rerun()

def mem_clear():
    st.session_state.mem = 0.0
    st.rerun()

def toggle_mode():
    st.session_state.mode = "RAD" if st.session_state.mode == "DEG" else "DEG"
    st.rerun()

# ──────────────── UI ────────────────
st.markdown("<div class='calc'>", unsafe_allow_html=True)
st.markdown("<div class='brand'>CASIO fx-991 • Pro</div>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.disp or '0'}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='note'>Mode: {st.session_state.mode} • Memory: {st.session_state.mem:g}</div>", unsafe_allow_html=True)

# Always 4 columns per row → no missing/wrapping buttons
def row(buttons, classes=None):
    cols = st.columns(4)
    for i, spec in enumerate(buttons):
        if spec is None:  # keep grid alignment
            continue
        label, handler, key = spec
        ctx = classes or ""
        with cols[i]:
            cdiv = f"<div class='{ctx}'>"  # style group wrapper
            st.markdown(cdiv, unsafe_allow_html=True)
            st.button(label, key=key, on_click=handler)

# Memory row
row([
    ("MC", mem_clear,  "mc"),
    ("MR", mem_recall, "mr"),
    ("M+", mem_add,    "mplus"),
    ("M−", mem_sub,    "mminus"),
])

# Functions
row([("sin(", partial(press,"sin("), "sin"),
     ("cos(", partial(press,"cos("), "cos"),
     ("tan(", partial(press,"tan("), "tan"),
     ("√(",   partial(press,"√("),   "sqrt")], classes="func")

row([("log(", partial(press,"log("), "log"),
     ("ln(",  partial(press,"ln("),  "ln"),
     ("(",    partial(press,"("),    "lp"),
     (")",    partial(press,")"),    "rp")], classes="func")

# Numbers + operators with pretty labels but correct payloads
row([("7", partial(press,"7"), "n7"),
     ("8", partial(press,"8"), "n8"),
     ("9", partial(press,"9"), "n9"),
     ("÷", partial(press,"÷"), "div")], classes="op")

row([("4", partial(press,"4"), "n4"),
     ("5", partial(press,"5"), "n5"),
     ("6", partial(press,"6"), "n6"),
     ("×", partial(press,"×"), "mul")], classes="op")

row([("1", partial(press,"1"), "n1"),
     ("2", partial(press,"2"), "n2"),
     ("3", partial(press,"3"), "n3"),
     ("−", partial(press,"−"), "sub")], classes="op")

row([("0", partial(press,"0"), "n0"),
     (".", partial(press,"."), "dot"),
     ("^", partial(press,"^"), "pow"),
     ("+", partial(press,"+"), "add")], classes="op")

row([("π", partial(press,"π"), "pi"),
     ("e", partial(press,"e"), "e"),
     ("!", partial(press,"fact("), "fact"),
     ("=", evaluate, "eq")], classes="eq")

row([("C", clear, "clr"),
     ("⌫", back,  "bksp"),
     (f"{st.session_state.mode}", toggle_mode, "mode"),
     None], classes="dng")  # keep 4 columns

st.markdown("</div>", unsafe_allow_html=True)

