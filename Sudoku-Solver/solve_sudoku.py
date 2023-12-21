def find_empty(board,n):
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0: return (i, j)

def valid(board, pos, num, n, r, c):
    for i in range(n):
        if board[i][pos[1]] == num and (i, pos[1]) != pos: 
            return False
    for j in range(n):
        if board[pos[0]][j] == num and (pos[0], j) != pos:  
            return False
    si = pos[0] - pos[0] % r
    sj = pos[1] - pos[1] % c
    for i in range(r):
        for j in range(c):
            if board[si + i][sj + j] == num and (si + i,sj + j) != pos:
                return False
    return True

def row_check(matrix, row, n):
	st = set()
	for i in range(0, n):
		if matrix[row][i] in st:
			return False
		if matrix[row][i] != 0:
			st.add(matrix[row][i])
	return True


def col_check(matrix, col, n):
	st = set()
	for i in range(0, n):
		if matrix[i][col] in st:
			return False
		if matrix[i][col] != 0:
			st.add(matrix[i][col])
	return True

def box_check(matrix, startRow, startCol, r, c):
	st = set()
	for row in range(0, r):
		for col in range(0, c):
			curr = matrix[row + startRow][col + startCol]
			if curr in st:
				return False
			if curr != 0:
				st.add(curr)
	return True

def isValid(matrix, row, col, n, r, c):
    a,b,c=row_check(matrix, row, n),col_check(matrix, col, n),box_check(matrix, row - row % r, col - col % c, r, c)
    if(not a and b and c): msg = "Identical numbers in row"
    elif(a and not b and c): msg = "Identical numbers in column"
    elif(a and b and not c): msg = "Identical numbers in box"
    elif(not a and not b and c): msg = "Identical numbers in row and column"
    elif(not a and b and not c): msg = "Identical numbers in row and box"
    elif(a and not b and not c): msg = "Identical numbers in column and box"
    elif(not a and not b and not c): msg = "Identical numbers in row, column and box"
    else: msg = ""
    return (msg,(a and b and c))

def input_valid(matrix,n,r,c):
    for i in range(0, n):
        for j in range(0, n):
            msg,check = isValid(matrix, i, j, n, r, c)
            if (not check):
                return (msg,False)
    return (msg,True)

def solve_sudoku(board,n,r,c):
    empty = find_empty(board,n)
    if not empty:  
        return True
    for nums in range(n):
        if valid(board, empty, nums + 1, n, r, c):
            board[empty[0]][empty[1]] = nums + 1
            if solve_sudoku(board, n, r, c): 
                return True
            board[empty[0]][empty[1]] = 0 
    return False
