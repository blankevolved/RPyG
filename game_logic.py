from utils import Error, clear_screen
import os
import time
try:
    import keyboard
except ImportError:
    os.system('pip3 install keyboard')
    import keyboard

tickspeed = 20

class Board:
    def __init__(self, name:str, width:int, height:int) -> None:
        self.name = name
        self.width = range(width)
        self.height = range(height)
        self.positions = {}
        for x in self.width:
            for y in self.height:
                self.positions[x, y] = None
        self.icon_list = []
    def create(self):
        # board var
        board = ''
        # length of current line
        cur_len = 0
        # get height and width
        for y in self.height:
            for x in self.width:
                # check if a variable position is = to None
                if self.positions[x, y] == None:
                    # if so append - to the board
                    board = board + '-'
                    # and increse length
                    cur_len = cur_len + 1
                # check if a variable position is the type of Entity
                elif type(self.positions[x, y]) == Entity:
                    # loop thru icon list
                    for i in self.icon_list:
                        # check if icons pos equal to our current x, y
                        if i.pos == (x, y):
                            # add icon to the board
                            board = board + i.icon
                            # increase length
                            cur_len = cur_len + 1
                # check if current length is greater than or equal too the max width value
                if cur_len >= self.width[-1] + 1:
                    # if so appened a new line char to the board
                    board = board + '\n'
                    # and set current length to 0
                    cur_len = 0
        ## return the board str to user
        return board
    def __repr__(self) -> str:
        return self.name

class Entity:
    def __init__(self, name:str, x:int, y:int, icon:str, board:Board, cols={}, health=10, damage=1) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.icon = icon
        self.board = board
        board.positions[self.pos] = self
        board.icon_list.append(self)
        self.health = health
        self.max_health = health
        self.damage = damage
        self.cols = cols
        self.debug = False
    def check_death(self):
        if self.health <= 0:
            self.board.positions[self.pos] = None
            self.x = None
            self.y = None
            self.pos = (self.x, self.y)
    def return_stats(self):
        stats = f'''HP: {self.health}/{self.max_health}
DMG: {self.damage}
'''
        if self.debug == True:
            stats = stats + f'''
POS: {self.pos}
X: {self.x}
Y: {self.y}
'''
        return stats
    def move_right(self):
        self.__move__(1, 0, '+', 'right')
                
    def move_left(self):
        self.__move__(1, 0, '-', 'left')

    def move_up(self):
        self.__move__(0, 1, '-', 'up')

    def move_down(self):
        self.__move__(0, 1, '+', 'down')
    
    def __move__(self, x_val:int, y_val:int, plus_or_minus:str, cannot_move_msg:str):
        try:
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

    def start_inputs(self):
        time.sleep(4/tickspeed)
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
            if keyboard.is_pressed('ctrl+3'):
                clear_screen()
                if self.debug == False:
                    self.debug = True
                elif self.debug == True:
                    self.debug = False
                break



    def __update_pos__(self):
        self.pos = (self.x, self.y)
        self.board.positions[self.pos] = self
    def __repr__(self) -> str:
        return self.name