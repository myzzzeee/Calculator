import streamlit as st
import math
import re

# Page Configuration
st.set_page_config(
    page_title="Myze's Calculator",
    layout="centered"
)
st.title("🧮 Myze's Calculator")

# Hide the form's own submit button (Enter key still triggers it)
st.markdown("""
<style>
div[data-testid="stFormSubmitButton"] button {
    visibility: hidden;
    height: 0px;
    margin: 0px;
    padding: 0px;
}
</style>
""", unsafe_allow_html=True)

# Session State
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "answer" not in st.session_state:
    st.session_state.answer = 0
if "calculated" not in st.session_state:
    st.session_state.calculated = False

# Helper Functions
def add(value):
    if st.session_state.expression == "Error" or st.session_state.calculated:
        st.session_state.expression = ""
        st.session_state.calculated = False
    st.session_state.expression += value

def clear():
    st.session_state.expression = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def balance_parentheses(expr):
    open_count = expr.count("(")
    close_count = expr.count(")")
    if open_count > close_count:
        expr += ")" * (open_count - close_count)
    return expr

def to_eval_string(expr):
    expr = expr.replace("sin(", "math.sin(")
    expr = expr.replace("cos(", "math.cos(")
    expr = expr.replace("tan(", "math.tan(")
    expr = expr.replace("exp(", "math.exp(")
    expr = expr.replace("√(", "math.sqrt(")
    expr = expr.replace("π", "math.pi")
    expr = expr.replace("^", "**")
    expr = re.sub(r"\be\b", "math.e", expr)
    return expr

def calculate():
    try:
        expression = balance_parentheses(st.session_state.expression)
        eval_string = to_eval_string(expression)
        result = eval(
            eval_string,
            {
                "__builtins__": None,
                "math": math
            }
        )
        st.session_state.answer = result
        st.session_state.expression = str(result)
        st.session_state.calculated = True
    except Exception:
        st.session_state.expression = "Error"

def on_button_click(button):
    if button == "AC":
        clear()
    elif button == "⌫":
        backspace()
    elif button == "=":
        calculate()
    elif button == "sin":
        add("sin(")
    elif button == "cos":
        add("cos(")
    elif button == "tan":
        add("tan(")
    elif button == "√":
        add("√(")
    elif button == "π":
        add("π")
    elif button == "e":
        add("e")
    elif button == "EXP":
        add("exp(")
    elif button == "Ans":
        add(str(st.session_state.answer))
    elif button == "^":
        add("^")
    else:
        add(button)

# Display (on top)
with st.form(key="expr_form", clear_on_submit=False):
    st.text_input("Output", key="expression")
    st.form_submit_button("=", use_container_width=True, on_click=calculate)

# Button Layout (internal values unchanged — "*" stays "*")
buttons = [
    ["AC", "⌫", "(", ")", "%"],
    ["sin", "cos", "tan", "√", "π"],
    ["7", "8", "9", "/", "^"],
    ["4", "5", "6", "*", "e"],
    ["1", "2", "3", "-", "EXP"],
    ["0", ".", "Ans", "+", "="]
]

# What gets shown on the button face vs. what gets added to the expression
display_map = {
    "*": "×"
}

# Buttons to style blue (scientific functions)
sci_keys = []
equals_key = None

for row_idx, row in enumerate(buttons):
    cols = st.columns(5)
    for col_idx, button in enumerate(row):
        label = display_map.get(button, button)
        key = f"btn_{row_idx}_{col_idx}"

        if button in ["sin", "cos", "tan", "√", "π", "EXP"]:
            sci_keys.append(key)

        if button == "=":
            equals_key = key
            cols[col_idx].button(
                label,
                key=key,
                use_container_width=True,
                on_click=on_button_click,
                args=(button,),
                type="primary"
            )
        else:
            cols[col_idx].button(
                label,
                key=key,
                use_container_width=True,
                on_click=on_button_click,
                args=(button,)
            )

# Style scientific function buttons blue
sci_selector = ", ".join([f'.st-key-{k} button' for k in sci_keys])
st.markdown(f"""
<style>
{sci_selector} {{
    color: #4da6ff !important;
    border-color: #4da6ff !important;
}}
</style>
""", unsafe_allow_html=True)
