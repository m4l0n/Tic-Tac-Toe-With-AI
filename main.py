import tkinter.messagebox
from tkinter import *
import numpy as np

board_size = 600
symbol_size = (board_size / 3 - board_size / 8) / 2
symbol_thickness = 10
symbol_x_colour = '#78A6B8'
symbol_o_colour = '#F65073'
green = '#7BC043'


class Tic_Tac_Toe():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=board_size, height=board_size)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)

        self.initialise_board()
        self.player_x_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_x_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.x_wins = False
        self.o_wins = False

        self.x_score = 0
        self.o_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialise_board(self):
        # Draw Y-axis lines
        for i in range(2):
            self.canvas.create_line((i + 1) * board_size / 3, 0, (i + 1) * board_size / 3, board_size)

        # Draw X-axis lines
        for i in range(2):
            self.canvas.create_line(0, (i + 1) * board_size / 3, board_size, (i + 1) * board_size / 3)

    def play_again(self):
        self.initialise_board()
        # self.player_x_starts = not self.player_x_starts
        self.player_x_turns = self.player_x_starts
        self.board_status = np.zeros(shape=(3, 3))

    def draw_o(self, logical_position):
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_o_colour)

    def draw_x(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_x_colour)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size,
                                width = symbol_thickness,
                                fill = symbol_x_colour)

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            # if self.player_x_turns:
            #     if not self.is_grid_occupied(logical_position):
            #         self.draw_x(logical_position)
            #         self.board_status[logical_position[0]][logical_position[1]] = -1
            #         self.player_x_turns = not self.player_x_turns
            # else:
            #     if not self.is_grid_occupied(logical_position):
            #         self.draw_o(logical_position)
            #         self.board_status[logical_position[0]][logical_position[1]] = 1
            #         self.player_x_turns = not self.player_x_turns
            if self.player_x_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_x(logical_position)
                    self.board_status[logical_position[1]][logical_position[0]] = -1
                    self.player_x_turns = not self.player_x_turns
                    if self.check_gameover():
                        self.display_gameover()
                    else:
                        self.ai_turn()
                else:
                    tkinter.messagebox.showerror(title="Error", message="The box has been selected!")

        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def ai_turn(self):
        logical_position = self.find_best_move(self.board_status)
        self.draw_o(logical_position)
        self.board_status[logical_position[1]][logical_position[0]] = 1
        self.player_x_turns = not self.player_x_turns
        if self.check_gameover():
            self.display_gameover()

    def minimax(self, board_status, depth, isMax):
        if self.check_winner('X', board_status):
            return -10

        if self.check_winner('O', board_status):
            return 10

        if self.check_tie(board_status):
            return 0
        # Maximiser
        if isMax:
            best = -1000

            for i in range(3):
                for j in range(3):
                    if (board_status[i][j] == 0):
                        board_status[i][j] = 1
                        best = max(best, self.minimax(board_status, depth + 1, not isMax))
                        board_status[i][j] = 0
            return best
        # Minimiser
        else:
            best = 1000

            for i in range(3):
                for j in range(3):
                    if (board_status[i][j] == 0):
                        board_status[i][j] = -1
                        best = min(best, self.minimax(board_status, depth + 1, not isMax))
                        board_status[i][j] = 0
            return best

    def find_best_move(self, board_status):
        best_value = -1000
        best_move = [-1, -1]
        for i in range(3):
            for j in range(3):
                if (board_status[i][j] == 0):
                    board_status[i][j] = 1
                    move_value = self.minimax(board_status, 0, False)
                    # Undo the move
                    board_status[i][j] = 0
                    if (move_value > best_value):
                        best_move = [j, i]
                        best_value = move_value
        return best_move

    # Convert grid position to absolute position (x,y coordinate) on the program screen
    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (board_size / 3) * logical_position + board_size / 6

    # Convert absolute position of the click event to grid position
    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (board_size / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[1]][logical_position[0]] == 0:
            return False
        else:
            return True

    def check_winner(self, player, board_status):
        player = -1 if player == 'X' else 1
        # Check for winner in vertical or horizontal lines
        for i in range(3):
            if board_status[i][0] == board_status[i][1] == board_status[i][2] == player:
                return True
            if board_status[0][i] == board_status[1][i] == board_status[2][i] == player:
                return True
        # Check for winner in diagonal lines
        if board_status[0][0] == board_status[1][1] == board_status[2][2] == player:
            return True
        if board_status[0][2] == board_status[1][1] == board_status[2][0] == player:
            return True

        return False

    def check_tie(self, board_status):
        r, c = np.where(board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True
        return tie

    def check_gameover(self):
        self.x_wins = self.check_winner('X', self.board_status)
        if not self.x_wins:
            self.o_wins = self.check_winner('O', self.board_status)

        if not self.o_wins:
            self.tie = self.check_tie(self.board_status)

        gameover = self.x_wins or self.o_wins or self.tie

        if self.x_wins:
            print('X wins')
        if self.o_wins:
            print('O wins')
        if self.tie:
            print('It\'s a tie')

        return gameover

    def display_gameover(self):
        if self.x_wins:
            self.x_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_x_colour
        elif self.o_wins:
            self.o_score += 1
            text = 'Winner: Bot (O)'
            color = symbol_o_colour
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(board_size / 2, board_size / 4, font = "cmr 40 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(board_size / 2, 5 * board_size / 10, font = "cmr 40 bold", fill=green, text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.x_score) + '\n'
        score_text += 'Bot (O) : ' + str(self.o_score) + '\n'
        score_text += 'Tie : ' + str(self.tie_score)
        self.canvas.create_text(board_size / 2, 3 * board_size / 5, font="cmr 30 bold", fill=green, text=score_text)
        self.reset_board = True

        score_text = 'Click to Play again \n'
        self.canvas.create_text(board_size / 2, 15 * board_size / 16, font="cmr 20 bold", fill="gray", text=score_text)


if __name__ == "__main__":
    game_instance = Tic_Tac_Toe()
    game_instance.mainloop()
