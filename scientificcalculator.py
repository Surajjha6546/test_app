import streamlit as st
import math
from functools import partial

# ───────────────────────── PAGE / THEME ─────────────────────────
st.set_page_config(page_title="Casio fx-991EX | Streamlit Pro", page_icon="🧮", layout="centered")

st.markdown("""
<style>
body {background: radial-gradient(circle at 25% 15%, #0b0f17 0%, #0a0d12 100%);}
.calc {
  max-width:460px;margin:40px auto;padding:20px;
  background:linear-gradient(180deg,#0d141f,#0a111a);
  border-radius:20px;border:1px solid #1a2538;
  box-shadow:0 0 30px rgba(0,255,213,.25);
}
.brand{text-align:center;color:#00ffd5;font-weight:800;font-size:20px;
margin-bottom:10px;text-shadow:0 0 8px #00ffd5;}
.display{background:#000;color:#00ff9d;font-family:Consolas,monospace;
font-size:30px;text-align:right;border-radius:10px;padding:12px;
margin-bottom:8px;overflow-x:auto;border:1px solid #111;}
.info{font-size:13px;color:#7ee7ff;text-align:right;margin-bottom:10px;}
button[kind="secondary"]{
  height:48px;border-radius:10px;font-weight:600;
  border:1px solid #1c2636;color:#e8f9ff;background:#121a27;}
.op   button[kind="secondary"]{border-color:#00ffa2;}
.func button[kind="secondary"]{border-color:#66a3ff;}
.eq   button[kind="secondary"]{border-color:#a8fddc;}
.dng  button[kind="secondary"]{border-color:#ff5f6a;}
.mem  button[kind="secondary"]{border-color:#ffaa00;}
.shift button[kind="secondary"]{border-color:#f1ff5e;color:#f8fa9d;}
</style>
""", unsafe_allow_html=True)

# ───────────────────────── STATE ─────────────────────────
if "disp" not in st.session_state: st.session_state.disp = ""
if "mem"  not in st.session_state: st.session_state.mem  = 0.0
if "ans"  not in st.session_state: st.session_state.ans  = 0.0
if "mode" not in st.session_state: st.session_state.mode = "DEG"   # DEG | RAD
if "shift" not in st.session_state: st.session_state.shift = False
if "history" not in st.session_state: st.session_state.history = []  # recent calcs

# ───────────────────────── MATH HELPERS ─────────────────────────
def tsin(x): return math.sin(math.radians(x)) if st.session_state.mode=="DEG" else math.sin(x)
def tcos(x): return math.cos(math.radians(x)) if st.session_state.mode=="DEG" else math.cos(x)
def ttan(x): return math.tan(math.radians(x)) if st.session_state.mode=="DEG" else math.tan(x)
def nPr(n,r): return math.factorial(int(n)) // math.factorial(int(n)-int(r))
def nCr(n,r): return math.comb(int(n), int(r))

ALLOWED = {"math": math, "tsin": tsin, "tcos": tcos, "ttan": ttan, "nPr": nPr, "nCr": nCr}

def _sanitize(expr: str) -> str:
    # Pretty to pythonic
    return (expr.replace("×", "*")
                .replace("÷", "/")
                .replace("^", "**")
                .replace("%", "/100")
                .replace("√", "math.sqrt(")    # we append '(' for UX; user must close it
                .replace("π", "math.pi")
                .replace("e", "math.e")
                .replace("sin", "tsin")
                .replace("cos", "tcos")
                .replace("tan", "ttan")
                .replace("ln", "math.log")
                .replace("log", "math.log10")
                .replace("Ans", str(st.session_state.ans)))

# ───────────────────────── ACTIONS ─────────────────────────
def press(token: str):
    # Always work with strings; token MUST be str
    if st.session_state.disp == "Error":
        st.session_state.disp = ""
    st.session_state.disp += token
    st.rerun()

def clear():
    st.session_state.disp = ""
    st.rerun()

def back():
    st.session_state.disp = st.session_state.disp[:-1]
    st.rerun()

def toggle_mode():
    st.session_state.mode = "RAD" if st.session_state.mode == "DEG" else "DEG"
    st.rerun()

def toggle_shift():
    st.session_state.shift = not st.session_state.shift
    st.rerun()

def equal():
    expr = st.session_state.disp.strip()
    if not expr:
        return
    try:
        sanitized = _sanitize(expr)
        result = eval(sanitized, ALLOWED)   # no builtins!
        st.session_state.ans = result
        st.session_state.history.insert(0, f"{expr} = {result}")
        st.session_state.history = st.session_state.history[:10]
        st.session_state.disp = str(result)
    except Exception:
        st.session_state.disp = "Error"
    st.rerun()

# Memory
def mem_add():
    try:
        val = eval(_sanitize(st.session_state.disp or "0"), ALLOWED)
        st.session_state.mem += float(val)
    except Exception:
        pass
    st.rerun()

def mem_sub():
    try:
        val = eval(_sanitize(st.session_state.disp or "0"), ALLOWED)
        st.session_state.mem -= float(val)
    except Exception:
        pass
    st.rerun()

def mem_clear():
    st.session_state.mem = 0.0
    st.rerun()

def mem_recall():
    st.session_state.disp += str(st.session_state.mem)
    st.rerun()

# ───────────────────────── SHIFT MAP ─────────────────────────
# What the key *prints* when SHIFT is ON
SHIFT_MAP = {
    "sin(": "asin(",   # inverse trig
    "cos(": "acos(",
    "tan(": "atan(",
    "log(": "10**",    # 10^x
    "ln(":  "exp(",    # e^x
    "√(":   "**2",     # x^2 (acts on the left value)
    "π":    "e"        # quick constant swap
}

def shifted(symbol: str) -> str:
    return SHIFT_MAP.get(symbol, symbol)

# ───────────────────────── UI ─────────────────────────
st.markdown("<div class='calc'>", unsafe_allow_html=True)
st.markdown("<div class='brand'>CASIO fx-991EX • Streamlit Pro</div>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.disp or '0'}</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='info'>Mode: {st.session_state.mode} &nbsp;|&nbsp; "
    f"SHIFT: {'ON' if st.session_state.shift else 'OFF'} &nbsp;|&nbsp; "
    f"Mem: {st.session_state.mem:.4g} &nbsp;|&nbsp; Ans: {st.session_state.ans:.4g}</div>",
    unsafe_allow_html=True
)

def make_row(btns):
    cols = st.columns(4)
    for i, (label, handler, key) in enumerate(btns):
        # Ensure labels are ALWAYS strings
        label = str(label)
        with cols[i]:
            st.button(label, key=key, on_click=handler, use_container_width=True)

# Memory row
make_row([("MC", mem_clear, "k_mc"),
          ("MR", mem_recall, "k_mr"),
          ("M+", mem_add,    "k_mplus"),
          ("M−", mem_sub,    "k_mminus")])

# Trig / function rows (SHIFT aware)
make_row([(shifted("sin(") if st.session_state.shift else "sin(", partial(press, shifted("sin(") if st.session_state.shift else "sin("), "k_sin"),
          (shifted("cos(") if st.session_state.shift else "cos(", partial(press, shifted("cos(") if st.session_state.shift else "cos("), "k_cos"),
          (shifted("tan(") if st.session_state.shift else "tan(", partial(press, shifted("tan(") if st.session_state.shift else "tan("), "k_tan"),
          (shifted("√(")  if st.session_state.shift else "√(",  partial(press, shifted("√(")  if st.session_state.shift else "√("),  "k_sqrt")])

make_row([(shifted("log(") if st.session_state.shift else "log(", partial(press, shifted("log(") if st.session_state.shift else "log("), "k_log"),
          (shifted("ln(")  if st.session_state.shift else "ln(",  partial(press, shifted("ln(")  if st.session_state.shift else "ln("),  "k_ln"),
          ("(",  partial(press, "("), "k_lp"),
          (")",  partial(press, ")"), "k_rp")])

# Digits & ops
make_row([("7", partial(press, "7"), "k_7"),
          ("8", partial(press, "8"), "k_8"),
          ("9", partial(press, "9"), "k_div"),
          ("÷", partial(press, "÷"), "k_op_div")])

make_row([("4", partial(press, "4"), "k_4"),
          ("5", partial(press, "5"), "k_5"),
          ("6", partial(press, "6"), "k_mul"),
          ("×", partial(press, "×"), "k_op_mul")])

make_row([("1", partial(press, "1"), "k_1"),
          ("2", partial(press, "2"), "k_2"),
          ("3", partial(press, "3"), "k_sub"),
          ("−", partial(press, "−"), "k_op_sub")])

make_row([("0", partial(press, "0"), "k_0"),
          (".", partial(press, "."), "k_dot"),
          ("^", partial(press, "^"), "k_pow"),
          ("+", partial(press, "+"), "k_op_add")])

# Constants / equals
make_row([(shifted("π") if st.session_state.shift else "π", partial(press, shifted("π") if st.session_state.shift else "π"), "k_pi"),
          ("e", partial(press, "e"), "k_e"),
          ("!", partial(press, "math.factorial("), "k_fact"),
          ("=", equal, "k_eq")])

# Controls (use ASCII-safe DEL instead of ⌫)
make_row([("C", clear, "k_clear"),
          ("DEL", back, "k_del"),
          ("SHIFT", toggle_shift, "k_shift"),
          (st.session_state.mode, toggle_mode, "k_mode")])

st.markdown("</div>", unsafe_allow_html=True)

# ───────────────────────── HISTORY ─────────────────────────
st.subheader("🧾 Recent Calculations (Replay)")
if st.session_state.history:
    for h in st.session_state.history[:10]:
        st.markdown(f"`{h}`")
else:
    st.caption("No calculations yet.")
