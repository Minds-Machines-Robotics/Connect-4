#imports
import asyncio
import websockets
import pygame
import sys
import math
import random
import numpy as np

# colors!
Blue = (0, 0, 255)
Black = (0,0,0)
RED = (255, 0 , 0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

# create empty board
def create_board():
  board = np.zeros((ROW_COUNT,COLUMN_COUNT))
  return board

#check the location of the last placed pices for wins
def check_for_wins(board, player):
  for col in range(len(board[0])):
    for row in range(len(board)):
      if (col < 4) and \
        (board[row][col] == player and board[row][col+1] == player and \
        board[row][col+2] == player and board[row][col+3] == player):
          return True
      if (row > 2) and \
        (board[row][col] == player and board[row-1][col] == player and \
        board[row-2][col] == player and board[row-3][col] == player):
          return True
      if (col < 4 and row > 2) and \
        (board[row][col] == player and board[row-1][col+1] == player and \
        board[row-2][col+2] == player and board[row-3][col+3] == player):
          return True
      if (col > 2 and row > 2) and \
        (board[row][col] == player and board[row-1][col-1] == player and \
        board[row-2][col-2] == player and board[row-3][col-3] == player):
          return True

  return False

#add a piece at the lowest availible row
def add_piece(board, col, player):
  win = [False, 0]
  if -1 < col < 7:
    for row in range(len(board) - 1, -1, -1):
      if board[row][col] == 0:
        if player == 1:
          board[row][col] = 1
          win[0] = check_for_wins(board, 1)
        else:
          board[row][col] = 2
          win[0] = check_for_wins(board, 2)
        if win[0] is True:
          win[1] = player
        return True, win
  print('Invalid move!')
  return False, win

#print board to console
def print_board(board):
  for row in board:
    print(row)

  print("")

#pygame visual board display
#use for debugging and AI visualization 
def draw_board(board):
  for col in range(len(board[0])):
    for row in range(len(board)):
      pygame.draw.rect(screen, Blue, \
      (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
      if board[row][col] == 0:
        pygame.draw.circle(screen, Black, \
        (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2))\
        , RADIUS)
      elif board[row][col] == 1:
        pygame.draw.circle(screen, RED, \
        (int(col*SQUARESIZE+SQUARESIZE/2),int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),\
        RADIUS)
      else:
        pygame.draw.circle(screen, YELLOW, \
        (int(col*SQUARESIZE+SQUARESIZE/2),int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),\
        RADIUS)
    pygame.display.update()

def find_legal_moves(board):
  legal = []
  for col in range(len(board[0])):
    if board[0][col] == 0:
      legal.append(col)
  return legal
  
count = 1
board = create_board()

pygame.init()

SQUARESIZE = 100

width = 7 * SQUARESIZE

height = 7 * SQUARESIZE

size = (width , height)

RADIUS = int(SQUARESIZE/2 -5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
print_board(board)

game = True
winner = [False, ""]
while game:

  if count %2 == 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

      pressed = pygame.mouse.get_pressed()

      if pressed[0]:
        # human play
        mouse_position = pygame.mouse.get_pos()
        posx = mouse_position[0]
        piece = int(math.floor(posx/SQUARESIZE))
        placed, winner = add_piece(board, piece, count%2)
        if placed:
          count+=1
          print_board(board)
          draw_board(board)

  # computer play
  if count %2 == 0 and winner[0] is False:
    pygame.time.wait(2000)
    piece = random.choice(find_legal_moves(board))
    placed, winner = add_piece(board, piece, count%2)
    if placed:
      count+=1
      print_board(board)
      draw_board(board)

  # check for win
  if winner[0] is True:
    if winner[1] == 1:
      print("Player 1 wins!")
    else:
      print("Player 2 wins!")
    game = False


  if not game:
    pygame.time.wait(2000)
