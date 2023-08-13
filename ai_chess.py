# -*- coding: utf-8 -*-
"""ai_chess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1seC78xLIH3_sid0wT876W8MQdtnxHMAa
"""

!pip install chess --upgrade

"""#Getting our chess Board ready"""

import chess
board = chess.Board()
board

"""#Reward and punishment table for moves for different pieces"""

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

"""#Evaluating the board situation"""

def evaluate_board():
    if board.is_checkmate():
        if board.turn:
            # print('Black wins')
            return -9999
        else:
            # print('White wins')
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    white_pawn = len(board.pieces(chess.PAWN, chess.WHITE))
    black_pawn = len(board.pieces(chess.PAWN, chess.BLACK))
    white_bishop = len(board.pieces(chess.BISHOP, chess.WHITE))
    black_bishop = len(board.pieces(chess.BISHOP, chess.BLACK))
    white_knight = len(board.pieces(chess.KNIGHT, chess.WHITE))
    black_knight = len(board.pieces(chess.KNIGHT, chess.BLACK))
    white_rook = len(board.pieces(chess.ROOK, chess.WHITE))
    black_rook = len(board.pieces(chess.ROOK, chess.BLACK))
    white_queen = len(board.pieces(chess.QUEEN, chess.WHITE))
    black_queen = len(board.pieces(chess.QUEEN, chess.BLACK))
    white_king = len(board.pieces(chess.KING, chess.WHITE))
    black_king = len(board.pieces(chess.KING, chess.BLACK))

    pawn = 100 * (white_pawn - black_pawn) 
    knight = 320 * (white_knight - black_knight)
    bishop = 330 * (white_bishop - black_bishop)    
    rook = 500 * (white_rook - black_rook)
    queen = 900 * (white_queen - black_queen)
    
    material = pawn + knight + rook + bishop + queen
    
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])

    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])

    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])

    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])

    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])
    
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])

    eval = pawnsq + knightsq + bishopsq + rooksq + queensq + knightsq
    
    if board.turn:
        return eval
    else:
        return -eval

"""
# Searching the best move using minimax and alphabeta algorithm with negamax implementation"""

def alphabeta(alpha, beta, depth):
    best_score = -9999
    if depth == 0:
        return quiesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha,  depth- 1)
        board.pop()
        if score>alpha:
            alpha = score
        if score >= beta:
            return score
        if score > best_score:
            best_score = score
    return best_score

def quiesce(alpha, beta):
    stand_pat = evaluate_board()
    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = -quiesce(-beta, alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha

"""#Selecting move

"""

def select_move(depth):
    try:
        move = chess.polyglot.MemoryMappedReader("C:/Users/your_path/books/human.bin").weighted_choice(board).move
        return move
    except:
        best_move = chess.Move.null()
        best_value = -99999
        alpha = -100000
        beta = 100000
        for move in board.legal_moves:
            board.push(move)
            score = -alphabeta(-beta, -alpha, depth-1)
            
            if score > best_value:
                best_value = score
                best_move=move
            if score > alpha:
                alpha = score
            board.pop()
        return best_move

import chess.svg
import chess.pgn
import chess.engine
from IPython.display import SVG

board

board.push(select_move(5))
board

board.push_san("d5")
board

board.push(select_move(6))
board

board.push_san('Nf6')
board

board.push(select_move(4))
board

board.push_san("Rxh7")
board

board.push(select_move(4))
board

board.push_san('d4')
board

board.push(select_move(3))
board

board.push_san("Qxd5")
board

board.push(select_move(3))
board

board.push_san('e5')
board

board.push(select_move(5))
board

board.push_san('exf4')
board

board.push(select_move(5))
board

board.push_san("Nc6")
board

board.push(select_move(4))
board

board.push_san('Bb4+')
board

board.push(select_move(4))
board

board.push_san('Ng4')
board

board.push(select_move(4))
board

board.push_san('Bxg4')
board

board.push(select_move(4))
board

board.push_san('Qg5')
board

board.push(select_move(4))
board

board.push_san("Bxf3")
board

board.push(select_move(5))
board

def my_move(i):
    board.push_san(i)
    return board

def ai_move(d):
    board.push(select_move(d))
    return board

my_move('Bxe2')

ai_move(3)

my_move('Qxe3')

ai_move(5)

my_move('Rh5')

ai_move(5)

my_move('Qf4')

ai_move(5)

my_move('Qxg4')

ai_move(5)

my_move('Rf5')

ai_move(4)