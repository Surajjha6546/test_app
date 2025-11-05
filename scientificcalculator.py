import streamlit as st
import math
from functools import partial

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Casio fx-991EX | Streamlit", page_icon="🧮", layout="centered")

st.markdown("""
<style>
body {background: radial-gradient(circle at 25% 15%, #0b0f17 0%, #0a0d12 100%);}
.calc {
  max-width:460px;margin:40px auto;padding:20px;
  background:linear-gradient(180deg,#0d141f,#0a111a);
  border-radius:20px;border:1px solid #1a2538;
  box-shadow:0 0 30px rgba(0,255,213,.3);
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

# ---------------- STATE ----------------
if "disp" not in st.session_state: st.session_state.disp = ""
if "mem" not in st.session_state: st.session_state.mem = 0.0
if "mode" not in st.session_state: st.session_state.mode = "DEG"
if "shift" not in st.session_state: st.session_state.shift = False
if "history" not in st.session_state: st.session_state.history = []  # calculation recall

# ---------------- SAFE MATH ----------------
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

def sanitize(expr):
    return (expr.replace("π","math.pi")
                .replace("√","math.sqrt")
                .replace("^","**")
                .replace("×","*")
                .replace("÷","/"))

# ---------------- ACTIONS ----------------
def press(x):
    if st.session_state.disp == "Error": st.session_state.disp = ""
    st.session_state.disp += x
    st.rerun()

def clear(): st.session_state.disp = ""; st.rerun()
def back(): st.session_state.disp = st.session_state.disp[:-1]; st.rerun()
def toggle_mode(): st.session_state.mode = "RAD" if st.session_state.mode=="DEG" else "DEG"; st.rerun()
def toggle_shift(): st.session_state.shift = not st.session_state.shift; st.rerun()

def evaluate():
    expr = sanitize(st.session_state.disp.strip())
    if not expr: return
    try:
        result = eval(expr, {"__builtins__": None}, ALLOWED)
        st.session_state.history.insert(0, f"{expr} = {result}")
        st.session_state.history = st.session_state.history[:8]
        st.session_state.disp = str(result)
    except Exception:
        st.session_state.disp = "Error"
    st.rerun()

# Memory
def mem_add():
    try:
        val = eval(sanitize(st.session_state.disp or "0"), {"__builtins__": None}, ALLOWED)
        st.session_state.mem += float(val)
    except: pass
    st.rerun()
def mem_sub():
    try:
        val = eval(sanitize(st.session_state.disp or "0"), {"__builtins__": None}, ALLOWED)
        st.session_state.mem -= float(val)
    except: pass
    st.rerun()
def mem_clear(): st.session_state.mem = 0.0; st.rerun()
def mem_recall():
    st.session_state.disp += str(st.session_state.mem)
    st.rerun()

# ---------------- SHIFT MAPPING ----------------
shift_map = {"sin(": "asin(", "cos(": "acos(", "tan(": "atan(",
             "log(": "10**", "ln(": "exp(", "√(": "^2", "π": "e"}

def shifted(x): return shift_map.get(x, x)

# ---------------- UI ----------------
st.markdown("<div class='calc'>", unsafe_allow_html=True)
st.markdown("<div class='brand'>CASIO fx-991EX • Streamlit</div>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.disp or '0'}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='info'>Mode: {st.session_state.mode} | SHIFT: {'ON' if st.session_state.shift else 'OFF'} | Memory: {st.session_state.mem:.4g}</div>", unsafe_allow_html=True)

def make_row(buttons, cls=""):
    cols = st.columns(4)
    for i,(label,fn,key) in enumerate(buttons):
        with cols[i]:
            st.button(label, key=key, on_click=fn)

# memory
make_row([("MC", mem_clear, "mc"),("MR", mem_recall, "mr"),("M+", mem_add, "m+"),("M−", mem_sub, "m-")],"mem")

# trig + funcs
make_row([(shifted("sin(") if st.session_state.shift else "sin(", partial(press, shifted("sin(") if st.session_state.shift else "sin("),"sin"),
          (shifted("cos(") if st.session_state.shift else "cos(", partial(press, shifted("cos(") if st.session_state.shift else "cos("),"cos"),
          (shifted("tan(") if st.session_state.shift else "tan(", partial(press, shifted("tan(") if st.session_state.shift else "tan("),"tan"),
          (shifted("√(") if st.session_state.shift else "√(", partial(press, shifted("√(") if st.session_state.shift else "√("),"sqrt")],"func")

make_row([(shifted("log(") if st.session_state.shift else "log(", partial(press, shifted("log(") if st.session_state.shift else "log("),"log"),
          (shifted("ln(") if st.session_state.shift else "ln(", partial(press, shifted("ln(") if st.session_state.shift else "ln("),"ln"),
          ("(", partial(press,"("), "("),
          (")", partial(press,")"), ")")],"func")

# numbers & ops (unique keys so + never disappears)
make_row([("7", partial(press,"7"), "n7"),("8", partial(press,"8"), "n8"),("9", partial(press,"9"), "n9"),("÷", partial(press,"÷"), "div")],"op")
make_row([("4", partial(press,"4"), "n4"),("5", partial(press,"5"), "n5"),("6", partial(press,"6"), "n6"),("×", partial(press,"×"), "mul")],"op")
make_row([("1", partial(press,"1"), "n1"),("2", partial(press,"2"), "n2"),("3", partial(press,"3"), "n3"),("−", partial(press,"−"), "sub")],"op")
make_row([("0", partial(press,"0"), "n0"),(".", partial(press,"."), "dot"),("^", partial(press,"^"), "pow"),("+", partial(press,"+"), "plus")],"op")

# constants / eq
make_row([(shifted("π") if st.session_state.shift else "π", partial(press, shifted("π") if st.session_state.shift else "π"), "pi"),
          ("e", partial(press,"e"), "e"),
          ("!", partial(press,"fact("), "fact"),
          ("=", evaluate, "eq")],"eq")

# controls bottom
make_row([("C", clear, "clr"),("⌫", back, "bksp"),("SHIFT", toggle_shift, "shift"),(st.session_state.mode, toggle_mode, "mode")],"dng")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- HISTORY INLINE ----------------
st.subheader("🧠 Recent Calculations (Replay)")
if st.session_state.history:
    for h in st.session_state.history[:6]:
        st.markdown(f"`{h}`")
else:
    st.caption("No calculations yet.")
