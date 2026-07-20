import streamlit as st
import math

st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="centered")

# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------
if "expr" not in st.session_state:
    st.session_state.expr = ""
if "angle_mode" not in st.session_state:
    st.session_state.angle_mode = "Degrees"

st.title("Myze's Scientific Calculator")

st.session_state.angle_mode = st.radio(
    "Angle mode (used for sin/cos/tan)",
    ["Degrees", "Radians"],
    horizontal=True,
    index=0 if st.session_state.angle_mode == "Degrees" else 1,
)

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def press(token):
    st.session_state.expr += token

def clear():
    st.session_state.expr = ""

def backspace():
    st.session_state.expr = st.session_state.expr[:-1]

def root(x, n):
    if n == 0:
        raise ValueError("Root degree cannot be 0")
    if x < 0:
        if n % 2 == 0:
            raise ValueError("Even root of a negative number is undefined")
        return -((-x) ** (1 / n))
    return x ** (1 / n)

def logn(x, n):
    if x <= 0 or n <= 0 or n == 1:
        raise ValueError("Invalid log arguments")
    return math.log(x, n)

def evaluate(expr):
    if not expr.strip():
        return None

    # auto-close any unmatched parentheses
    open_count = expr.count("(")
    close_count = expr.count(")")
    expr += ")" * max(0, open_count - close_count)

    # normalize calculator symbols to Python syntax
    normalized = (
        expr.replace("×", "*")
        .replace("÷", "/")
        .replace("−", "-")
        .replace("^", "**")
        .replace("%", "/100")  # % acts as a percent unless used inside mod(...)
    )

    if st.session_state.angle_mode == "Degrees":
        sin_f = lambda x: math.sin(math.radians(x))
        cos_f = lambda x: math.cos(math.radians(x))
        tan_f = lambda x: math.tan(math.radians(x))
    else:
        sin_f, cos_f, tan_f = math.sin, math.cos, math.tan

    safe_names = {
        "sin": sin_f,
        "cos": cos_f,
        "tan": tan_f,
        "log": math.log10,      # log base 10
        "ln": math.log,          # natural log
        "logn": logn,            # log base n -> logn(x, n)
        "sqrt": math.sqrt,
        "root": root,            # nth root -> root(x, n)
        "mod": lambda a, b: math.fmod(a, b),
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
    }

    return eval(normalized, {"__builtins__": {}}, safe_names)

# ---------------------------------------------------------
# Display
# ---------------------------------------------------------
display_value = st.session_state.expr if st.session_state.expr else "0"
st.markdown(
    f"""
    <div style="
        background-color:#1e1e1e;
        color:#ffffff;
        font-size:32px;
        font-family:monospace;
        padding:18px;
        border-radius:8px;
        text-align:right;
        min-height:50px;
        overflow-x:auto;
        white-space:nowrap;
        margin-bottom:10px;
    ">{display_value}</div>
    """,
    unsafe_allow_html=True,
)

result_placeholder = st.empty()

# ---------------------------------------------------------
# Button layout
# ---------------------------------------------------------
rows = [
    [("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("log", "log("), ("ln", "ln(")],
    [("√", "sqrt("), ("x²", "**2"), ("xʸ", "**"), ("ⁿ√x", "root("), ("logₙ", "logn(")],
    [("(", "("), (")", ")"), (",", ","), ("mod", "mod("), ("π", "pi")],
    ["7", "8", "9", "÷", "C"],
    ["4", "5", "6", "×", "⌫"],
    ["1", "2", "3", "−", "%"],
    ["0", ".", "=", "+", "e"],
]

for row in rows:
    cols = st.columns(len(row))
    for col, item in zip(cols, row):
        if isinstance(item, tuple):
            label, token = item
        else:
            label = token = item

        if col.button(label, use_container_width=True, key=f"btn_{label}_{token}"):
            if label == "C":
                clear()
            elif label == "⌫":
                backspace()
            elif label == "=":
                try:
                    value = evaluate(st.session_state.expr)
                    st.session_state.expr = str(value)
                except Exception as e:
                    st.session_state.expr = ""
                    result_placeholder.error(f"Error: {e}")
            else:
                press(token)
            st.rerun()

