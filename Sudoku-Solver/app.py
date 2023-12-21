import re
import streamlit as st
from board import four_board, six_board, nine_board, eight_board , matrix_to_df
from solve_sudoku import solve_sudoku, input_valid

st.set_page_config(
    page_title="Sudoku Solver",
    page_icon="🧊",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# Sudoku Solver\nThis App can solve 4X4, 6X6, 8X8, 9X9 Sudoku puzzles  \n~Suhas Prabhu"
    }
)

st.markdown(
    """
    <style>
    [data-baseweb="select"] {
        margin-top: -30px;
    }
    [data-baseweb="textarea"] {
        margin-top: -30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Sudoku Solver")

st.write("### Select the type of Sudoku to be solved")
type = st.selectbox(
    '',
    ('4X4','6X6','8X8','9X9')
)

if (type == '4X4'):
    board = four_board
    size,n,r,c=200,4,2,2
elif (type == '6X6'):
    board = six_board
    size,n,r,c=300,6,2,3
elif (type == '8X8'):
    board = eight_board
    size,n,r,c=350,8,2,4
elif (type == '9X9'):
    board = nine_board
    size,n,r,c=350,9,3,3

st.write("### Enter the Puzzle below")
input_data = st.text_area(label="",value=board, height=size)

input = []

for line in input_data.split("\n"):
    if not "-" in line:
        vals = re.findall("[0-n]", line.rstrip())
        val = [int(x) for x in vals]
        input.append(val)

if st.button("Solve!"):
    st.header('Solution')
    msg,check=input_valid(input,n,r,c)
    if(check):
        if(solve_sudoku(input,n,r,c)):
            st.write(matrix_to_df(input,n))
        else: st.write("Invalid Sudoku!!")
    else: 
        st.write("""### """, msg)
    
else:
    st.header('Board Layout')
    st.write(matrix_to_df(input,n))
