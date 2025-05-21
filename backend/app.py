from flask import Flask, request, jsonify
from flask_cors import CORS
from sudoku import solve, is_valid
import random

app = Flask(__name__)
CORS(app)  # Allows frontend to access backend

@app.route('/solve', methods=['POST'])
def solve_board():
    data = request.get_json()
    board = data.get('board')
    if not board or len(board) != 9 or any(len(row) != 9 for row in board):
        return jsonify({'error': 'Invalid board size'}), 400

    board_copy = [row[:] for row in board]
    if solve(board_copy):
        return jsonify({'solution': board_copy})
    else:
        return jsonify({'error': 'No solution found'}), 400

@app.route('/generate', methods=['GET'])
def generate_board():
    # Start with empty board
    board = [[0]*9 for _ in range(9)]
    fill_random_cells(board)
    return jsonify({'board': board})

def fill_random_cells(board, count=20):
    filled = 0
    while filled < count:
        row, col = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        if board[row][col] == 0 and is_valid(board, row, col, num):
            board[row][col] = num
            filled += 1

if __name__ == '__main__':
    app.run(debug=True)
