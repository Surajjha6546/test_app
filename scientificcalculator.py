import math
import streamlit as st
from functools import partial

st.set_page_config(page_title="Casio fx-991EX", page_icon="🧮", layout="centered")

# ---------- Styles ----------
st.markdown("""
<style>
.calc {max-width:420px;margin:auto;padding:16px;border-radius:16px;
background:#0f1115;box-shadow:0 6px 24px rgba(0,0,0,.5);}
.display {font-family:monospace;background:#000;color:#0f0;font-size:28px;
padding:12px 10px;text-align:right;border-radius:10px;margin-bottom:10px;overflow-x:auto;}
button[kind="secondary"] {height:46px;border-radius:10px;font-size:16px;padding:0;margin:2px;}
</style>
""", unsafe_allow_html=True)

# ---------- State ----------
if "disp" not in st.session_state: st.session_state.disp = ""
if "hist" not in st.session_state: st.session_state.hist = []

# ---------- Math helpers ----------
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
    "pi":   math.pi,
    "e":    math.e,
    "math": math,
}

def _sanitize(expr:str)->str:
    return expr.replace("π","math.pi").replace("√","math.sqrt").replace("^","**")

def evaluate():
    expr=_sanitize(st.session_state.disp)
    try:
        result=eval(expr,{"__builtins__":None},ALLOWED)
        st.session_state.hist.insert(0,f"{st.session_state.disp} = {result}")
        st.session_state.hist=st.session_state.hist[:8]
        st.session_state.disp=str(result)
    except Exception:
        st.session_state.disp="Error"
    st.rerun()

def press(x): 
    if st.session_state.disp=="Error": st.session_state.disp=""
    st.session_state.disp+=x; st.rerun()

def clear(): st.session_state.disp=""; st.rerun()
def back(): st.session_state.disp=st.session_state.disp[:-1]; st.rerun()
def recall(entry): st.session_state.disp=entry.split("=")[0].strip(); st.rerun()

# ---------- Display ----------
st.markdown("<div class='calc'>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.disp or '0'}</div>", unsafe_allow_html=True)

# ---------- Keypad (consistent 4 columns per row) ----------
rows = [
    [("sin","sin(","func"),("cos","cos(","func"),("tan","tan(","func"),("log","log(","func")],
    [("ln","ln(","func"),("√","√(","func"),("(","(","func"),(")"," )","func")],
    [("7","7","num"),("8","8","num"),("9","9","num"),("/","/","op")],
    [("4","4","num"),("5","5","num"),("6","6","num"),("*","*","op")],
    [("1","1","num"),("2","2","num"),("3","3","num"),("-","-","op")],
    [("0","0","num"),(".",".","num"),("^","^","op"),("+","+","op")],
    [("π","π","func"),("e","e","func"),("x!","fact(","func"),("=","=","eq")],
    [("C","C","clr"),("⌫","⌫","clr"),("","",None),("","",None)],  # keep 4 cols
]

for r,row in enumerate(rows):
    cols=st.columns(4)
    for c,(lbl,payload,typ) in enumerate(row):
        if not lbl: continue
        key=f"{r}_{c}_{lbl}"
        if typ=="eq":  cols[c].button(lbl,key=key,on_click=evaluate)
        elif typ=="clr" and lbl=="C": cols[c].button(lbl,key=key,on_click=clear)
        elif typ=="clr": cols[c].button(lbl,key=key,on_click=back)
        else: cols[c].button(lbl,key=key,on_click=partial(press,payload))

st.markdown("</div>", unsafe_allow_html=True)

# ---------- Replay ----------
st.divider()
st.subheader("🧠 Replay Memory")
if not st.session_state.hist:
    st.caption("No calculations yet.")
else:
    for i,entry in enumerate(st.session_state.hist):
        c1,c2=st.columns([0.85,0.15])
        c1.code(entry,language="text")
        c2.button("↩",key=f"recall_{i}",on_click=partial(recall,entry))


