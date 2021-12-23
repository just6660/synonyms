from copy import copy, deepcopy

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] != " "):
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):

    #these variables will be set open or closed
    start_bound = ""
    end_bound = ""

    #check if out of bounds
    if((max(x_end, y_end) > len(board) - 1) or (min(x_end, y_end) < 0)):
        return "CLOSED"

    #end bounds
    if (min(d_y + y_end, d_x + x_end) < 0) or (max(d_y + y_end, d_x + x_end) > len(board) - 1):
        end_bound = "CLOSED"
    elif(board[d_y + y_end][d_x + x_end] == " "):
        end_bound = "OPEN"
    else:
        end_bound = "CLOSED"

    #start bounds
    if (min(y_end - (d_y * length), x_end - (d_x * length)) < 0) or (max(y_end - (d_y * length), x_end - (d_x * length)) > len(board) - 1):
        start_bound = "CLOSED"
    elif(board[y_end - (length * d_y)][x_end - (length * d_x)]) == " ":
        start_bound = "OPEN"
    else:
        start_bound = "CLOSED"

    #compare start and end bounds
    if(start_bound == "OPEN" and end_bound == "OPEN"):
        return "OPEN"
    elif(start_bound == "CLOSED" and end_bound == "CLOSED"):
        return "CLOSED"
    else:
        return "SEMIOPEN"

def return_length_of_row(board, col, y_start, x_start, d_y, d_x):

    length = 1

    for i in range(len(board)):

        if (max(d_y + y_start, d_x + x_start) > len(board) - 1) or (min(d_y +  y_start, d_x + x_start) < 0 ) or board[d_y + y_start][d_x + x_start] != col:
            return length
        length += 1
        y_start += d_y
        x_start += d_x
    

def detect_row(board, col, y_start, x_start, length, d_y, d_x):

    open_seq_count = 0
    semi_open_seq_count = 0
    cur_length = 0

    for i in range(len(board)):
        if(board[y_start][x_start] == col):
            cur_length =  return_length_of_row(board, col, y_start, x_start, d_y, d_x)
            if(cur_length == length):
                type = is_bounded(board, y_start + (length-1)*d_y, x_start + (length-1)*d_x, length, d_y, d_x)
                if(type == "OPEN"):
                    open_seq_count += 1
                elif(type == "SEMIOPEN"):
                    semi_open_seq_count += 1
                
                y_start += d_y*(length - 1)
                x_start += d_x*(length - 1)
            else:

                y_start += d_y*(cur_length - 1)
                x_start += d_x*(cur_length - 1)

        y_start += d_y
        x_start += d_x

        if(y_start > 7 or x_start > 7):
            break

    return open_seq_count, semi_open_seq_count
    
def detect_row_5(board, col, y_start, x_start, length, d_y, d_x):
    
    is_found = False
    cur_length = 0

    for i in range(len(board)):
        if(board[y_start][x_start] == col):
            cur_length = return_length_of_row(board,col,y_start,x_start,d_y,d_x)
            if(cur_length == 5):
                is_found = True
            else:
                y_start += d_y*(cur_length - 1)
                x_start += d_x*(cur_length - 1)

        y_start += d_y
        x_start += d_x

        if(y_start > 7 or x_start > 7):
            break

    return is_found

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0

    #horizontals
    for i in range(len(board)):
        count_tuple = detect_row(board,col,i,0,length,0,1)
        open_seq_count += count_tuple[0]
        semi_open_seq_count += count_tuple[1]

    #verticals
    for j in range(len(board)):
        count_tuple = detect_row(board,col,0,j,length,1,0)
        open_seq_count += count_tuple[0]
        semi_open_seq_count += count_tuple[1]

    #diagonals
    for x in range(2):
        #dir(1,1)
        if(x==0):
            for k in range(len(board)-1):
                count_tuple = detect_row(board,col,6-k,0,length,1,1)
                open_seq_count += count_tuple[0]
                semi_open_seq_count += count_tuple[1]

                count_tuple = detect_row(board,col,0,k+1,length,1,1)
                open_seq_count += count_tuple[0]
                semi_open_seq_count += count_tuple[1]
        #dir(1,-1)
        elif(x==1):
            for l in range(len(board)-1):
                count_tuple = detect_row(board,col,0,1+l,length,1,-1)
                open_seq_count += count_tuple[0]
                semi_open_seq_count += count_tuple[1]

                count_tuple = detect_row(board,col,1+l,7,length,1,- 1)
                open_seq_count += count_tuple[0]
                semi_open_seq_count += count_tuple[1]

    return open_seq_count, semi_open_seq_count

def detect_rows_5(board, col):

    length = 5

    #horizontals
    for i in range(len(board)):
        if(detect_row_5(board,col,i,0,length,0,1)):
            return True

    #verticals
    for j in range(len(board)):
        if(detect_row_5(board,col,0,j,length,1,0)):
            return True

    #diagonals
    for x in range(2):
        #dir(1,1)
        if(x==0):
            for k in range(len(board)-1):
                if(detect_row_5(board,col,6-k,0,length,1,1)):
                    return True
                if(detect_row_5(board,col,0,k+1,length,1,1)):
                    return True
        #dir(1,-1)
        elif(x==1):
            for l in range(len(board)-1):
                if(detect_row_5(board,col,0,1+l,length,1,-1)):
                    return True
                if(detect_row_5(board,col,1+l,7,length,1,-1)):
                    return True

    return False
    

def search_max(board):

    max_score = score(board)
    best_move = (-1,-1)

    #create deep copy of board
    test_board = deepcopy(board)

    #test every space
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(test_board[i][j] != " "):
                continue
            test_board[i][j] = "b"
            test_score = score(test_board)
            if(test_score > max_score):
                max_score = test_score
                best_move = i,j
            test_board[i][j] = " "

    #checks
    if(best_move == (-1,-1)):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if(board[i][j] ==  " "):
                    return i,j

    else:
        return best_move

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):

    #check white
    if detect_rows_5(board, "w"):
        return "White won"

    #check black
    elif detect_rows_5(board, "b"):
        return "Black won"

    #check filled
    filled = True

    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] == " "):
                filled = False
                break

    if filled == True:
        return "Draw"

    else:
        return "Continue playing"


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':
    play_gomoku(8)

