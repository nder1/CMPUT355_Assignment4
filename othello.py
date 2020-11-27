# Computing 355 Assignment 4
# CCID: nder    Student ID: 1601471

# Import libraries
from random import randrange

# Initialize Glabal Variables
EMPTY = 0
BLACK = 1
WHITE = 2
BORDER = 3
POINT_CHARS = '.xo#'

# Game class
class Game:
    def __init__(self, player_colour, comp_colour, side_length):
        self.player = player_colour
        self.comp = comp_colour
        self.side = side_length
        
        self.half = int(self.side / 2)                                                              # integer conversion for create_board()
        
        self.board = []                                                                             # initialize empty board
        
    # Creates board with size of side_length plus borders
    def create_board(self):
        row = []
        for b in range(self.side + 2):                                                              # append top border row to board
            row.append(BORDER)
        self.board.append(row)
        
        for r in range(self.side):
            row = []
            row.append(BORDER)                                                                      # append border cell to left of row
            for c in range(self.side):
                row.append(EMPTY)
            row.append(BORDER)
            self.board.append(row)
            
        row = []
        for b in range(self.side + 2):                                                              # append bottom border row to board
            row.append(BORDER)
        self.board.append(row)   
        
        # Place starting pieces on board
        self.board[self.half][self.half] = WHITE
        self.board[self.half][self.half + 1] = BLACK
        self.board[self.half + 1][self.half] = BLACK
        self.board[self.half + 1][self.half + 1] = WHITE
    
    # Prints board row by row
    def show_board(self):
        print("# ", end='')
        for n in range(self.side + 2):
            print(str(n) + " ", end='')                                                             # print horizontal number indexes
        print()
        
        for r in range(len(self.board)):                                                            # number of rows, with appended borders
            print(str(r) + " ", end='')                                                             # print vertical number indexes
            for c in range(len(self.board[0])):                                                     # number/length of columns, including appended border cell
                print(POINT_CHARS[self.board[r][c]] + " ", end='')
            print()                                                                                 # add newline character
    
    # Checks if point is a legal move
    def check_legal_move(self, currP, currO, x, y):
        tempx = x
        tempy = y
        moved = False                                                                               # bool for if check find an adjacent endpoint but has not moved
        if x > 0 and x < self.side + 1 and y > 0 and y < self.side + 1:                             # check is given x and y are on board
            for y1 in range(-1, 2):                                                                 # offset y1 = -1, 0, 1
                for x1 in range(-1, 2):                                                             # offset x1 = -1, 0, 1
                    if not (y1 == 0 and x1 == 0):                                                   # do not check current point
                        while self.board[tempy + y1][tempx + x1] == currO:
                            tempy += y1                                                             # increase search for player's stone from next position
                            tempx += x1                                                             # increase search for player's stone from next position
                            moved = True                                                            # potential endpoint is at least one space away
                        if moved == True and self.board[tempy + y1][tempx + x1] == currP:
                            direction = [y1, x1]
                            return direction                                                        # (x, y) has adjacent opponent piece(s) followed by a player piece i.e. is legal move
                        
                        # Reset state for next check
                        tempx = x
                        tempy = y
                        moved = False
        return False                                                                                # chosen move is not legal
    
    # Changes all cells to current player's colour from (x, y) to another of player's points
    def execute_move(self, currP, x, y, direction):
        while self.board[y + direction[0]][x + direction[1]] != EMPTY and self.board[y + direction[0]][x + direction[1]] != BORDER:
            self.board[y][x] = currP
            x += direction[1]
            y += direction[0] 
            
    # Prompt player, check for legality and execute changes
    def player_turn(self):
        while True:
            print()
            prompt = input("Please make a move using x and y, separated by a space: ")              # prompt the player for a move
            point = prompt.split()                                                                  # split player's input into two parts, x and y
            if len(point) == 2  and point[0].isdigit() and point[1].isdigit():                      # checks that x and y are integers
                point[0] = int(point[0])                                                            # convert x into int
                point[1] = int(point[1])                                                            # convert y into int
                if point[0] > 0 and point[0] <= self.side and point[1] > 0 and point[1] <= self.side:
                    if self.board[point[1]][point[0]] == EMPTY:
                        for n in range(8):                                                          # check for 8 potential neighbouring cells/lines
                            direction = self.check_legal_move(self.player, self.comp, point[0], point[1])
                            if direction != False:
                                self.execute_move(self.player, point[0], point[1], direction)       # apply board changes using player's point
                        break

            print("Not a legal move. Please try again (e.g. 1 1).")
        
        
    # Computer makes a random legal move
    def comp_turn(self):
        potential_moves = []
        for r in range(1, self.side + 1):
            for c in range(1, self.side + 1):
                if self.board[r][c] == EMPTY and self.check_legal_move(self.comp, self.player, c, r):
                    point = [c, r]
                    potential_moves.append(point)                                                   # find all legal moves for computer
        comp_move = potential_moves[randrange(len(potential_moves))]                                # randomly pick a legal move
        direction = self.check_legal_move(self.comp, self.player, comp_move[0], comp_move[1])
        self.execute_move(self.comp, comp_move[0], comp_move[1], direction)
        print()
        print("The computer makes a move at (" + str(comp_move[0]) + ", " + str(comp_move[1]) + ").")
        
    # Check for any legal moves for either player, end if none are found
    def check_done(self, currP, currO):
        for r in range(1, self.side + 1):
            for c in range(1, self.side + 1):
                if self.board[r][c] == EMPTY and self.check_legal_move(currP, currO, c, r):
                    return False                                                                    # return if any legal moves are found
        return True                                                                                 # game is over if no more legal moves are found

    def check_win(self):
        player_points = 0
        comp_points = 0
        
        for r in range(self.side + 1):
            for c in range(self.side + 1):
                if self.board[r][c] == self.player:
                    player_points += 1
                elif self.board[r][c] == self.comp:
                    comp_points += 1
        
        if player_points > comp_points:
            return [self.player, player_points]
        elif player_points < comp_points:
            return [self.comp, comp_points]
        elif player_points == comp_points:
            return 0
        

def main():
    while True:                                                                                     # loop until valid board dimension entered
        side_length = int(input("Enter an even side length: "))                                     # prompt player for board dimensions
        if side_length > 0 and side_length % 2 == 0:
            break
        else:
            print("Invalid board dimension!")
    
    while True:                                                                                     # loop until player colour entered
        prompt = input("Would you like to be Black (x) or White (o)? ")                             # prompt player for prefered colour
        if prompt == "black" or prompt == "Black":                                                  # if player chooses black, computer is white
            player = BLACK
            computer = WHITE
            break
        elif prompt == "white" or prompt == "White":                                                # if player chooses white, computer is black
            player = WHITE
            computer = BLACK
            break
        else:
            print("Please enter black or white.")
    
        
    game = Game(player, computer, side_length)                                                      # create game class
    
    game.create_board()
    print("NOTE: (1, 1) is in the TOP LEFT of the board.")
    game.show_board()                                                                               # print initialized board

    # Player has chosen to be BLACK (x)
    if player == BLACK:
        while True: 
            if not game.check_done(player, computer):                                               # before player's turn, check if play has any moves
                game.player_turn()
                game.show_board()
            else: 
                break
            
            if not game.check_done(computer, player):                                               # before computer's turn, check if computer has any moves
                game.comp_turn()
                game.show_board()
            else:
                break
        
        print("No more moves!")
        
        win = game.check_win()
        if win[0] == game.player:                                                                   # player wins
            print("Congratulations! You won with", win[1], "points!")
        elif win[0] == game.comp:
            print("The computer wins with", win[1], "points.")                                      # computer wins
        elif win == 0:
            print("It's a tie!")                                                                    # I'd honestly be surprised if you could get a tie on a decently sized board
            
    # Player has chosen to be WHITE (o)
    elif player == WHITE:
        while True: 
            if not game.check_done(computer, player):                                               # before computer's turn, check if computer has any moves
                game.comp_turn()
                game.show_board()
            else:
                break
            
            if not game.check_done(player, computer):                                               # before player's turn, check if play has any moves
                game.player_turn()
                game.show_board()
            else: 
                break
            
        print("No more moves!")
        
        win = game.check_win()
        if win[0] == game.player:                                                                   # player wins
            print("Congratulations! You won with", win[1], "points!")
        elif win[0] == game.comp:
            print("The computer wins with", win[1], "points.")                                      # computer wins
        elif win == 0:
            print("It's a tie!")                                                                    # I'd honestly be surprised if you could get a tie on a decently sized board
    
    
main()