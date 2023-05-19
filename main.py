import time
import tkinter as tk
import pygame

from checkers import board
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax, minimax_alphabeta
from minimax.algorithm import random_moves

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    white_turn = False
    red_turn = True

    def get_integer_from_gui():
        root = tk.Tk()
        root.title("Enter Difficulty")
        root.geometry("300x200")

        # Create a label to prompt the user to enter an integer
        label = tk.Label(root, text="Enter Difficulty:")
        label.pack(pady=20)

        # Create an Entry widget to allow the user to enter the integer
        entry = tk.Entry(root,width=30)

        entry.pack(padx=20)

        # Create a function to get the integer value and destroy the window
        def submit():
            nonlocal integer
            # Get the integer entered by the user
            integer_str = entry.get()

            # Check if the input is an integer
            try:
                integer = int(integer_str)
                root.destroy()
            except ValueError:
                # If the input is not an integer, show an error message
                error_label = tk.Label(root, text="Invalid input. Please enter an integer.")
                error_label.pack(pady=5)

        # Create a button to submit the integer
        submit_button = tk.Button(root, text="Submit", command=submit)
        submit_button.pack(pady=30)

        # Initialize the integer variable to None
        integer = None

        # Start the mainloop to display the GUI
        root.mainloop()

        # Return the integer entered by the user
        return integer

    # Call the function to get the integer from the GUI
    integer = get_integer_from_gui()

    # Use the integer variable however you like
    print("The user entered the integer:", integer)

    while run:
        clock.tick(FPS)


        if integer == 2:
            if red_turn and not white_turn:
                # value, new_board = minimax(game.get_board(), 9, RED, game)
                random = random_moves(game.get_board(), game)
                game.ai_move(random)
                game.change_turn()

                white_turn = True
                red_turn = False
                time.sleep(0.5)
            elif not red_turn and white_turn:
                value, new_board = minimax_alphabeta(game.get_board(), 5, WHITE, game, float('-inf'), float('inf'))
                game.ai_move(new_board)
                game.change_turn()
                white_turn = False
                red_turn = True
                time.sleep(0.5)
        elif integer == 1:
            if red_turn and not white_turn:
                # value, new_board = minimax(game.get_board(), 9, RED, game)
                random = random_moves(game.get_board(), game)
                game.ai_move(random)
                game.change_turn()
                white_turn = True
                red_turn = False
                time.sleep(0.5)
            elif not red_turn and white_turn:
                value, new_board = minimax(game.get_board(), 3, WHITE, game)
                game.ai_move(new_board)
                game.change_turn()
                white_turn = False
                red_turn = True
                time.sleep(0.5)



        
        # if game.turn == WHITE:
        #     value, new_board = minimax_alphabeta(game.get_board(), 4, WHITE, game, float('-inf'), float('inf'))
        #     game.ai_move(new_board)
        #     game.change_turn()
        #
        # else:


        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    
    pygame.quit()

main()