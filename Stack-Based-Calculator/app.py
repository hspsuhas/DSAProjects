import streamlit as st

st.markdown(
    """
    <style>
    [data-baseweb="input"] {
        margin-top: -30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def infix_to_postfix(expression):
    stack = []
    postfix = ""
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}

    for token in expression.split():
        if token.isdigit():
            postfix += token + " "
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack[-1] != "(":
                postfix += stack.pop() + " "
            stack.pop() 
        else:
            while stack and stack[-1] != "(" and precedence[token] <= precedence[stack[-1]]:
                postfix += stack.pop() + " "
            stack.append(token)

    while stack:
        postfix += stack.pop() + " "

    return postfix.strip()

def evaluate_expression(expression):
    stack = []
    tokens = expression.split()

    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token in "+-*/":
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = calculate(operand1, operand2, token)
            stack.append(result)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack[-1] != "(":
                operand2 = stack.pop()
                operand1 = stack.pop()
                operator = stack.pop()
                result = calculate(operand1, operand2, operator)
                stack.append(result)
            stack.pop()

    return stack.pop()

def calculate(operand1, operand2, operator):
    if operator == "+":
        return operand1 + operand2
    elif operator == "-":
        return operand1 - operand2
    elif operator == "*":
        return operand1 * operand2
    elif operator == "/":
        if operand2 == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return operand1 / operand2

st.title("Stack-Based Calculator")

st.write("#### Enter an Expression")

expression = st.text_input("")

if st.button("Evaluate"):
    try:
        postfix = infix_to_postfix(expression)
        result = evaluate_expression(postfix)
        st.write("### Result:", result)
    except ZeroDivisionError as e:
        st.error(str(e))
    except Exception as e:
        st.error("Invalid expression")
