from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_url_path='/static')

board = [''] * 9
current_player = 'X'
user_started = False

def check_win(player):
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)            # Diagonals
    ]
    
    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] == player:
            return True
    return False


def minimax(board, depth, is_maximizing):
    if check_win('O'):
        return 1
    if check_win('X'):
        return -1
    if '' not in board:
        return 0
    
    if is_maximizing:
        max_eval = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                eval = minimax(board, depth + 1, False)
                board[i] = ''
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                eval = minimax(board, depth + 1, True)
                board[i] = ''
                min_eval = min(min_eval, eval)
        return min_eval
    
    

@app.route('/')
def index():
    global user_started, board
    if not user_started:
        board = [''] * 9  # Reset the board
        return render_template('start.html')
    return render_template('index.html', board=board, message="")

@app.route('/start_game')
def start_game():
    global user_started
    user_started = True
    return render_template('index.html', board=board, message="")

@app.route('/restart_game', methods=['POST'])
def restart_game():
    global user_started, board
    user_started = True
    board = [''] * 9
    return redirect(url_for('index'))

@app.route('/make_move', methods=['GET'])
def make_move():
    global current_player, user_started
    
    if not user_started:
        return render_template('start.html')
    
    position = int(request.args.get('position'))
    
    if board[position] == '':
        board[position] = 'X'
        if check_win('X'):
            user_started = False
            return render_template('index.html', board=board, message="You win! Click below to try again.")
        elif '' not in board:
            user_started = False
            return render_template('index.html', board=board, message="It's a tie! Click below to try again.")
        
        best_move = -1
        best_score = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                move_score = minimax(board, 0, False)
                board[i] = ''
                if move_score > best_score:
                    best_score = move_score
                    best_move = i
        
        if best_move != -1:
            board[best_move] = 'O'
            if check_win('O'):
                user_started = False
                return render_template('index.html', board=board, message="AI wins! Click below to try again.")
        else:
            user_started = False
            return render_template('index.html', board=board, message="It's a tie! Click below to try again.")
    
    return render_template('index.html', board=board, message="")

if __name__ == "__main__":
    app.run(debug=True)
