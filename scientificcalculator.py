import math
import streamlit as st
from functools import partial

# ────────────────── Page & Theme ──────────────────
st.set_page_config(page_title="Casio fx-991EX (Streamlit)", page_icon="🧮", layout="centered")

st.markdown("""
<style>
/* container */
.calc {
  max-width: 420px; margin: 24px auto; padding: 16px;
  background: #0f1115; border-radius: 16px; box-shadow: 0 6px 24px rgba(0,0,0,.5);
  border: 1px solid #1f2430;
}
/* display */
.display {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  background: #0b0d10; color: #d9f99d;
  border: 1px solid #242b36; border-radius: 12px;
  padding: 14px 12px; text-align: right; font-size: 28px;
  overflow-x: auto; white-space: nowrap;
}
/* subtle caption */
.caption { color: #9aa4b2; font-size: 12px; margin-top: 4px; text-align: right; }
/* tighten default buttons */
button[kind="secondary"] {
  height: 48px; border-radius: 10px; font-weight: 600;
}
/* color groups */
.btn-num   { border: 1px solid #2a3441; }
.btn-op    { border: 1px solid #34d399; }
.btn-func  { border: 1px solid #60a5fa; }
.btn-eq    { border: 1px solid #a7f3d0; }
.btn-danger{ border: 1px solid #fb7185; }
</style>
""", unsafe_allow_html=True)

# ────────────────── State ──────────────────
if "disp" not in st.session_state: st.session_state.disp = ""
if "hist" not in st.session_state: st.session_state.hist = []   # list of "expr = result" (latest first)

# ────────────────── Safe eval helpers (Degree mode) ──────────────────
ALLOWED = {
    "sin":  lambda x: math.sin(math.radians(x)),
    "cos":  lambda x: math.cos(math.radians(x)),
    "tan":  lambda x: math.tan(math.radians(x)),
    "asin": lambda x: math.degrees(math.asin(x)),
    "acos": lambda x: math.degrees(math.acos(x)),
    "atan": lambda x: math.degrees(math.atan(x)),
    "sqrt": math.sqrt,
    "log":  math.log10,
    "ln":   math.log,
    "exp":  math.exp,
    "abs":  abs,
    "fact": math.factorial,
    "pow":  pow,
    "pi":   math.pi,          # allows typing "pi"
    "e":    math.e,           # allows typing "e"
    "math": math,             # used after replacements
}

def _sanitize(expr: str) -> str:
    # Friendly symbols → executable
    return (
        expr.replace("π", "math.pi")
            .replace("√", "math.sqrt")
            .replace("^", "**")
    )

def eval_now() -> None:
    raw = st.session_state.disp.strip()
    if not raw:
        return
    expr = _sanitize(raw)
    try:
        result = eval(expr, {"__builtins__": None}, ALLOWED)
        # store history (cap 8)
        st.session_state.hist.insert(0, f"{raw} = {result}")
        st.session_state.hist = st.session_state.hist[:8]
        st.session_state.disp = str(result)
    except Exception:
        st.session_state.disp = "Error"
    st.rerun()

def press(text: str) -> None:
    # Basic input guard: if last result was "Error", start fresh
    if st.session_state.disp == "Error":
        st.session_state.disp = ""
    st.session_state.disp += text
    st.rerun()

def backspace() -> None:
    st.session_state.disp = st.session_state.disp[:-1]
    st.rerun()

def clear_all() -> None:
    st.session_state.disp = ""
    st.rerun()

def recall(entry: str) -> None:
    # take the left side of "expr = result"
    st.session_state.disp = entry.split("=", 1)[0].strip()
    st.rerun()

# ────────────────── UI: Display ──────────────────
st.markdown("<div class='calc'>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.disp or '0'}</div>", unsafe_allow_html=True)
st.markdown("<div class='caption'>Mode: Degrees • sin, cos, tan, asin, acos, atan, log, ln, √, ^, !, π, e</div>", unsafe_allow_html=True)
st.write("")

# ────────────────── UI: Keypad ──────────────────
# label, payload, style
rows = [
    # functions
    [("sin", "sin(", "btn-func"), ("cos", "cos(", "btn-func"), ("tan", "tan(", "btn-func"), ("log", "log(", "btn-func")],
    [("ln",  "ln(",  "btn-func"), ("√",   "√(",  "btn-func"), ("(",   "(",   "btn-func"), (")",   ")",   "btn-func")],
    # numbers/operators
    [("7","7","btn-num"), ("8","8","btn-num"), ("9","9","btn-num"), ("/","/","btn-op")],
    [("4","4","btn-num"), ("5","5","btn-num"), ("6","6","btn-num"), ("*","*","btn-op")],
    [("1","1","btn-num"), ("2","2","btn-num"), ("3","3","btn-num"), ("-","-","btn-op")],
    [("0","0","btn-num"), (".",".","btn-num"), ("^","^","btn-op"),  ("+","+", "btn-op")],
    # constants / factorial / equals
    [("π","π","btn-func"), ("e","e","btn-func"), ("x!","fact(","btn-func"), ("=","=","btn-eq")],
    # clear / backspace
    [("C","C","btn-danger"), ("⌫","⌫","btn-danger")],
]

for r, row in enumerate(rows):
    cols = st.columns(len(row))
    for c, (label, payload, style) in enumerate(row):
        key = f"k_{r}_{c}_{label}"
        # Visual tag by injecting a tiny styled label before the Streamlit button
        cols[c].markdown(f"<div class='{style}' style='margin-bottom:4px'></div>", unsafe_allow_html=True)
        if label == "=":
            cols[c].button(label, key=key, on_click=eval_now)
        elif label == "C":
            cols[c].button(label, key=key, on_click=clear_all)
        elif label == "⌫":
            cols[c].button(label, key=key, on_click=backspace)
        else:
            cols[c].button(label, key=key, on_click=partial(press, payload))

st.markdown("</div>", unsafe_allow_html=True)

# ────────────────── UI: Replay History ──────────────────
with st.expander("🧠 Replay (last 8)"):
    if not st.session_state.hist:
        st.caption("No calculations yet.")
    else:
        for i, entry in enumerate(st.session_state.hist):
            c1, c2 = st.columns([0.85, 0.15])
            c1.code(entry, language="text")
            c2.button("↩", key=f"recall_{i}", on_click=partial(recall, entry))

