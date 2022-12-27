from utils import Error
import os
from utils import clear_screen
try:
    import keyboard
except ImportError:
    os.system('pip3 install keyboard')
    import keyboard
class Board:
    def __init__(self, width:int, height:int) -> None:
        self.width = range(width)
        self.height = range(height)
        self.positions = {}
        for x in self.width:
            for y in self.height:
                self.positions[x, y] = None
        self.icon_list = []
    def create(self):
        board = ''
        cur_len = 0
        for y in self.height:
            for x in self.width:
                if self.positions[x, y] == None:
                    board = board + '-'
                    cur_len = cur_len + 1
                elif type(self.positions[x, y]) == Entity:
                    for i in self.icon_list:
                        if i.pos == (x, y):
                            board = board + i.icon
                            cur_len = cur_len + 1
                if cur_len >= self.width[-1] + 1:
                    board = board + '\n'
                    cur_len = 0
        return board

class Entity:
    def __init__(self, name:str, x:int, y:int, icon:str, board:Board, skills_list=[], cols={}, health=10, damage=1) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.icon = icon
        self.board = board
        self.skills_list = skills_list
        board.positions[self.pos] = self
        board.icon_list.append(self)
        self.health = health
        self.max_health = health
        self.damage = damage
        self.cols = cols
    def check_death(self):
        if self.health <= 0:
            print(self.board.positions[self.pos])
            self.board.positions[self.pos] = None
            self.x = None
            self.y = None
            self.pos = (self.x, self.y)
    def move_right(self):
        self.__move__(1, 0, '+', 'right')
                
    def move_left(self):
        self.__move__(1, 0, '-', 'left')

    def move_up(self):
        self.__move__(0, 1, '-', 'up')

    def move_down(self):
        self.__move__(0, 1, '+', 'down')
    
    def __move__(self, x_val:int, y_val:int, plus_or_minus:str, cannot_move_msg:str, debug=False):
        try:
            if debug == True:
                print('pos')
                print(self.board.positions[self.x + x_val, self.y + y_val])
                print('obj')
                print(self.cols[c]['obj'])
            for c in self.cols:
                if plus_or_minus == '+':
                    if self.board.positions[self.x + x_val, self.y + y_val] == None:
                        self.board.positions[self.pos] = None
                        self.x = self.x + x_val
                        self.y = self.y + y_val
                        self.__update_pos__()
                    elif self.board.positions[self.x + x_val, self.y + y_val] == self.cols[c]['obj']:
                        self.cols[c]['func']()
                elif plus_or_minus == '-':
                    if self.board.positions[self.x - x_val, self.y - y_val] == None:
                        self.board.positions[self.pos] = None
                        self.x = self.x - x_val
                        self.y = self.y - y_val
                        self.__update_pos__()
                    elif self.board.positions[self.x - x_val, self.y - y_val] == self.cols[c]['obj']:
                        self.cols[c]['func']()
        except:
            print(Error.cannot_move_x(cannot_move_msg))

    def start_movement_input(self):
        while True:
            if keyboard.is_pressed('right_arrow'):
                clear_screen()
                self.move_right()
                break
            if keyboard.is_pressed('left_arrow'):
                clear_screen()
                self.move_left()
                break
            if keyboard.is_pressed('up_arrow'):
                clear_screen()
                self.move_up()
                break
            if keyboard.is_pressed('down_arrow'):
                clear_screen()
                self.move_down()
                break


    def __update_pos__(self):
        self.pos = (self.x, self.y)
        self.board.positions[self.pos] = self
    def __repr__(self) -> str:
        return self.name