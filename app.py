import math
import re

import streamlit as st


st.set_page_config(page_title="Calculator", page_icon="calculator", layout="wide")


def calculate(expression: str) -> str:
    """Evaluate a basic calculator expression."""
    allowed_chars = set("0123456789+-*/.() ")
    if not expression or any(char not in allowed_chars for char in expression):
        return "Error"

    try:
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception:
        return "Error"

    return format_number(result)


def format_number(value: float) -> str:
    if not math.isfinite(float(value)):
        return "Error"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return f"{value:.12g}"


def current_number() -> float | None:
    try:
        return float(st.session_state.display)
    except ValueError:
        return None


def replace_current_number(value: float) -> None:
    st.session_state.display = format_number(value)


def append_value(value: str) -> None:
    if st.session_state.display in {"0", "Error"}:
        st.session_state.display = ""
    st.session_state.display += value


def append_operator(value: str) -> None:
    if st.session_state.display == "Error":
        st.session_state.display = "0"
    st.session_state.display += value


def handle_button(label: str) -> None:
    display = st.session_state.display

    if label == "=":
        st.session_state.display = calculate(display)
    elif label == "C":
        st.session_state.display = "0"
    elif label == "CE":
        st.session_state.display = "0"
    elif label == "backspace":
        st.session_state.display = display[:-1] or "0" if display != "Error" else "0"
    elif label == "+/-":
        if display.startswith("-"):
            st.session_state.display = display[1:]
        elif display not in {"0", "Error"}:
            st.session_state.display = f"-{display}"
    elif label == ".":
        parts = re.split(r"[+\-*/]", display)
        if "." not in parts[-1]:
            if display in {"0", "Error"}:
                st.session_state.display = "0."
            else:
                append_value(".")
    elif label == "%":
        number = current_number()
        if number is not None:
            replace_current_number(number / 100)
        else:
            st.session_state.display = "Error"
    elif label == "1/x":
        number = current_number()
        if number:
            replace_current_number(1 / number)
        else:
            st.session_state.display = "Error"
    elif label == "x^2":
        number = current_number()
        if number is not None:
            replace_current_number(number**2)
        else:
            st.session_state.display = "Error"
    elif label == "sqrt":
        number = current_number()
        if number is not None and number >= 0:
            replace_current_number(math.sqrt(number))
        else:
            st.session_state.display = "Error"
    elif label in {"/", "*", "-", "+"}:
        if display[-1:] in {"/", "*", "-", "+"}:
            st.session_state.display = display[:-1] + label
        else:
            append_operator(label)
    else:
        append_value(label)


if "display" not in st.session_state:
    st.session_state.display = "0"


st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 20% 0%, #fff8ef 0, transparent 28%),
                linear-gradient(135deg, #fbf6ee 0%, #f5f4ed 100%);
            color: #111111;
        }

        .block-container {
            max-width: 1120px;
            padding: 0.35rem 0.4rem 0.4rem;
        }

        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"] {
            display: none;
        }

        .calculator-app {
            font-family: "Segoe UI", Arial, sans-serif;
        }

        .window-title {
            align-items: center;
            display: flex;
            gap: 14px;
            height: 30px;
            padding-left: 20px;
            font-size: 15px;
            color: #242424;
        }

        .app-icon {
            color: #1a76c4;
            font-size: 17px;
        }

        .mode-row {
            align-items: center;
            display: flex;
            gap: 18px;
            height: 80px;
            padding: 0 18px;
        }

        .menu-icon,
        .history-icon {
            font-size: 24px;
            line-height: 1;
        }

        .mode-title {
            font-size: 25px;
            font-weight: 700;
        }

        .display-box {
            align-items: center;
            background: rgba(255, 255, 255, 0.35);
            border: 2px solid #1c1c1c;
            border-radius: 5px;
            display: flex;
            height: 174px;
            justify-content: flex-end;
            margin-top: 24px;
            padding: 0 18px;
            width: 100%;
        }

        .display-value {
            color: #000000;
            font-size: clamp(54px, 7vw, 88px);
            font-weight: 700;
            line-height: 1;
            overflow: hidden;
            text-align: right;
            text-overflow: ellipsis;
            white-space: nowrap;
            width: 100%;
        }

        .memory-row {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            padding: 18px 28px 16px;
            color: #1f1f1f;
            font-size: 15px;
        }

        .memory-disabled {
            color: #9b9b9b;
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 4px;
        }

        div[data-testid="column"] {
            padding: 0;
        }

        .stButton > button {
            background: rgba(255, 255, 255, 0.58);
            border: 1px solid #ded8cd;
            border-radius: 5px;
            color: #1d1d1d;
            font-size: 28px;
            font-weight: 400;
            height: 122px;
            margin: 0 0 4px;
            transition: background 120ms ease, border-color 120ms ease;
        }

        .stButton > button:hover {
            background: rgba(255, 255, 255, 0.9);
            border-color: #c7c0b7;
            color: #000000;
        }

        div[data-testid="stHorizontalBlock"]:last-of-type
        div[data-testid="column"]:last-child .stButton > button {
            background: #0876c9;
            border-color: #0876c9;
            color: #ffffff;
            font-size: 36px;
        }

        div[data-testid="stHorizontalBlock"]:last-of-type
        div[data-testid="column"]:last-child .stButton > button:hover {
            background: #0067b8;
            color: #ffffff;
        }

        @media (max-width: 700px) {
            .block-container {
                padding: 0.25rem;
            }

            .display-box {
                height: 120px;
                margin-top: 8px;
            }

            .display-value {
                font-size: 52px;
            }

            .memory-row {
                padding: 14px 12px;
            }

            .stButton > button {
                height: 76px;
                font-size: 22px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

display_text = st.session_state.display or "0"

st.markdown(
    f"""
    <div class="calculator-app">
        <div class="window-title">
            <span class="app-icon">▦</span>
            <span>Calculator</span>
        </div>
        <div class="mode-row">
            <span class="menu-icon">☰</span>
            <span class="mode-title">Standard</span>
            <span class="history-icon">↱</span>
        </div>
        <div class="display-box">
            <div class="display-value">{display_text}</div>
        </div>
        <div class="memory-row">
            <span class="memory-disabled">MC</span>
            <span class="memory-disabled">MR</span>
            <span>M+</span>
            <span>M-</span>
            <span>MS</span>
            <span></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

buttons = [
    [("%", "%"), ("CE", "CE"), ("C", "C"), ("⌫", "backspace")],
    [("1/x", "1/x"), ("x²", "x^2"), ("²√x", "sqrt"), ("÷", "/")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("×", "*")],
    [("4", "4"), ("5", "5"), ("6", "6"), ("−", "-")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("+", "+")],
    [("+/-", "+/-"), ("0", "0"), (".", "."), ("=", "=")],
]

for row_index, row in enumerate(buttons):
    cols = st.columns(4)
    for col_index, (label, value) in enumerate(row):
        with cols[col_index]:
            key = f"button-{row_index}-{col_index}-{value}"
            if st.button(label, key=key, use_container_width=True):
                handle_button(value)
                st.rerun()
