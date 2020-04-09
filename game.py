import os
from enum import Enum
from textwrap import dedent


WIN_CONDITIONS = [
    # Horizontal Win
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    # Vertical Win
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    # Diagonal Win
    (0, 4, 8),
    (2, 4, 6)
]


class GameException(Exception):
    pass


class InvalidMoveException(GameException):
    def __init__(self):
        self.message = "Did not choose an EMPTY location on board"


class Mark(Enum):
    X = "X"
    O = "O"
    EMPTY = " "


class GameStatus(Enum):
    WIN = "win"
    TIE = "tie"
    ONGOING = "ongoing"


class Board:
    def __init__(self):
        self.board = [Mark.EMPTY] * 9
    
    def __getitem__(self, idx):
        return self.board[idx]
    
    def __setitem__(self, idx, mark: Mark):
        if self.board[idx] is not Mark.EMPTY:
            raise InvalidMoveException()

        self.board[idx] = mark

    def __repr__(self):
        values = [mark.value for mark in self.board]
        return dedent(
            """
            -------------
            | {} | {} | {} |
            -------------
            | {} | {} | {} |
            -------------
            | {} | {} | {} |
            -------------
            """.format(*values)
        )
    
    def status(self) -> bool:
        for i, j, k in WIN_CONDITIONS:
            if self.board[i] == self.board[j] == self.board[k] is not Mark.EMPTY:
                return GameStatus.WIN
        
        if all([self.board[i] is not Mark.EMPTY for i in range(9)]):
            return GameStatus.TIE
        
        return GameStatus.ONGOING

    def clear(self) -> None:
        self.board = [Mark.EMPTY] * 9


class Player:
    def __init__(self, name: str = None, mark: Mark = None):
        self.name = name
        self.mark = mark
        self.score = 0
    

class Game:
    def __init__(self):
        self.board = Board()
        self.game_number = 1

        self.p1 = Player(mark=Mark.X)
        self.p2 = Player(mark=Mark.O)

        self.current = self.p1
        self.message = "Have a great game!"

    def _restart(self) -> bool:
        self.current = self._next_player()

        if self.board.status() is GameStatus.WIN:
            self.current.score += 1
            self.message = f"{self.current.name} won! Congrats!"
        else:
            self.message = "It was a tie!"
        
        self._display()        
        self.game_number += 1
        self.board.clear()

        if self.game_number % 2:
            self.current = self.p1
        else:
            self.current = self.p2
        
        self.current.mark = Mark.X
        self._next_player().mark = Mark.O
        self.message = "New game, let's see who wins this one!"

        return input("Enter 999 to play again: ") == "999"
    
    def _next_player(self) -> Player:
        if self.current is self.p1:
            return self.p2
        return self.p1

    def _display(self) -> None:
        os.system('clear')
        print(dedent(
            f""" 
            ============ SCOREBOARD ============
            {self.p1.name}: {self.p1.score} wins | {self.p2.name}: {self.p2.score} wins
            ====================================

            MESSAGE: {self.message or 'Keep the pressure up!'}
            """
        ))

        print(f"GAME #{self.game_number}", end="")
        print(self.board)

        self.message = None
        
    def run(self) -> None:
        os.system('clear')
        print("Welcome to Tic-Tac-Toe. You already know the rules")

        self.p1.name = input("Name of player 1: ")
        self.p2.name = input("Name of player 2: ")
        
        while True:
            while self.board.status() is GameStatus.ONGOING:
                self._display()
                
                pos = input(f"{self.current.name}'s turn. Select where to move [1 - 9]: ")
                try: 
                    self.board[int(pos) - 1] = self.current.mark
                except IndexError:
                    self.message = "Please enter a number BETWEEN 1 - 9"
                except ValueError:
                    self.message = "Please enter a NUMBER between 1 - 9"
                except InvalidMoveException as e:
                    self.message = e.message
                else:
                    self.current = self._next_player()
            
            if not self._restart():
                break
            
        print("\nThanks for playing!\n")

if __name__ == '__main__':
    Game().run()
    