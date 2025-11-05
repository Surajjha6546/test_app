import streamlit as st
import math

# -------------------------------------------------------
# PAGE + STYLE
# -------------------------------------------------------
st.set_page_config(page_title="Casio fx-991EX | Streamlit", page_icon="🧮", layout="centered")

st.markdown("""
<style>
body {background: radial-gradient(circle at 25% 15%, #0b0f17 0%, #0a0d12 100%);}
h1 {text-align:center;color:#00ffaa;text-shadow:0 0 10px #00ffaa;}
.calc {max-width:480px;margin:auto;padding:15px 20px 20px;border-radius:20px;
background:linear-gradient(180deg,#0e141f,#0a111a);box-shadow:0 0 25px rgba(0,255,213,.25);}
input[type=text] {font-size:20px !important;height:3em !important;text-align:right;}
button[kind="secondary"]{height:52px;font-weight:700;border-radius:10px;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# STATE INITIALIZATION
# -------------------------------------------------------
expr    = st.session_state.get("expr", "")
memory  = st.session_state.get("memory", 0.0)
ans     = st.session_state.get("ans", 0.0)
history = st.session_state.get("history", [])
mode    = st.session_state.get("mode", "DEG")

# -------------------------------------------------------
# MATH HELPERS
# -------------------------------------------------------
def tsin(x): return math.sin(math.radians(x)) if mode == "DEG" else math.sin(x)
def tcos(x): return math.cos(math.radians(x)) if mode == "DEG" else math.cos(x)
def ttan(x): return math.tan(math.radians(x)) if mode == "DEG" else math.tan(x)
def nPr(n, r): return math.factorial(int(n)) // math.factorial(int(n) - int(r))
def nCr(n, r): return math.comb(int(n), int(r))

# -------------------------------------------------------
# EVALUATION
# -------------------------------------------------------
def evaluate_expression(expr):
    try:
        expr = (expr.replace("×","*").replace("÷","/").replace("^","**").replace("%","/100")
                    .replace("√","math.sqrt").replace("π","math.pi").replace("e","math.e")
                    .replace("sin","tsin").replace("cos","tcos").replace("tan","ttan")
                    .replace("ln","math.log").replace("log","math.log10")
                    .replace("nPr","nPr").replace("nCr","nCr")
                    .replace("Ans", str(ans)))
        result = eval(expr, {"math":math,"tsin":tsin,"tcos":tcos,"ttan":ttan,"nPr":nPr,"nCr":nCr})
        return result
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# -------------------------------------------------------
# HEADER + INPUT FIELD
# -------------------------------------------------------
st.markdown("<div class='calc'>", unsafe_allow_html=True)
st.markdown("<h1>Casio fx-991EX Scientific Calculator</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([3,1])
with col1:
    expr = st.text_input("Expression", expr, label_visibility="collapsed")
with col2:
    if st.button(mode, use_container_width=True):
        mode = "RAD" if mode == "DEG" else "DEG"

st.caption(f"Memory: {round(memory,6)} | Ans: {round(ans,6)}")

# -------------------------------------------------------
# BUTTON GRID
# -------------------------------------------------------
rows = [
    ["AC","DEL","(",")","%"],
    ["sin","cos","tan","ln","log"],
    ["7","8","9","÷","√"],
    ["4","5","6","×","-"],
    ["1","2","3","+","="],
    ["0",".","Ans","π","e"],
    ["M+","M-","MR","MC","±"],
    ["nCr","nPr","x²","^","!"]
]

def process_input(label, expr, memory, ans, history):
    if label == "AC": expr = ""
    elif label == "DEL": expr = expr[:-1]
    elif label == "=":
        result = evaluate_expression(expr)
        if result is not None:
            ans = result
            history.insert(0,(expr,result))
            expr = str(result)
    elif label == "√": expr += "√("
    elif label == "x²": expr += "**2"
    elif label == "±": expr += "(-"
    elif label == "!": expr += "math.factorial("
    elif label == "M+":
        try: memory += float(eval(expr or "0"))
        except: pass
    elif label == "M-":
        try: memory -= float(eval(expr or "0"))
        except: pass
    elif label == "MR": expr += str(memory)
    elif label == "MC": memory = 0
    else: expr += label
    return expr, memory, ans, history

# -------------------------------------------------------
# DRAW BUTTONS
# -------------------------------------------------------
for row in rows:
    cols = st.columns(5)
    for i, label in enumerate(row):
        if cols[i].button(label, use_container_width=True, key=f"{row}-{label}"):
            expr, memory, ans, history = process_input(label, expr, memory, ans, history)
            st.session_state.expr = expr
            st.session_state.memory = memory
            st.session_state.ans = ans
            st.session_state.history = history
            st.session_state.mode = mode
            st.rerun()

# -------------------------------------------------------
# HISTORY INLINE
# -------------------------------------------------------
st.markdown("### 🧮 Recent Calculations")
if history:
    for e, r in history[:10]:
        st.code(f"{e} = {r}")
else:
    st.caption("No calculations yet.")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# FOOTER INFO
# -------------------------------------------------------
st.markdown("---")
st.markdown("""
**Features**
- Degree/Radian toggle for trig  
- sin, cos, tan, ln, log, √, x², %, π, e, factorial, nCr, nPr  
- Memory: M+, M-, MR, MC  
- Ans recall and 10-step calculation history  
- Works perfectly on Streamlit Cloud/Desktop  
""")
