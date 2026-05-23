import streamlit as st


st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")


def calculate(expression: str) -> str:
    """Evaluate a basic calculator expression."""
    allowed_chars = set("0123456789+-*/.() ")
    if not expression or any(char not in allowed_chars for char in expression):
        return "Error"

    try:
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception:
        return "Error"

    if isinstance(result, float) and result.is_integer():
        return str(int(result))
    return str(result)


if "display" not in st.session_state:
    st.session_state.display = ""


st.title("Simple Calculator")

st.text_input(
    "Display",
    value=st.session_state.display,
    key="display_input",
    label_visibility="collapsed",
    disabled=True,
)

buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
]

for row in buttons:
    cols = st.columns(4)
    for col, label in zip(cols, row):
        if col.button(label, use_container_width=True):
            if label == "=":
                st.session_state.display = calculate(st.session_state.display)
            else:
                if st.session_state.display == "Error":
                    st.session_state.display = ""
                st.session_state.display += label
            st.rerun()

clear_col, backspace_col = st.columns(2)

if clear_col.button("Clear", use_container_width=True):
    st.session_state.display = ""
    st.rerun()

if backspace_col.button("Backspace", use_container_width=True):
    if st.session_state.display != "Error":
        st.session_state.display = st.session_state.display[:-1]
    else:
        st.session_state.display = ""
    st.rerun()
