from utils import Error, clear_screen
import os
import time
try:
    import keyboard
except ImportError:
    os.system('pip3 install keyboard')
    import keyboard

tickspeed = 20
current_board = None


class Board:
    def __init__(self, name:str, width:int, height:int, touch={}) -> None:
        self.name = name
        self.width = range(width)
        self.height = range(height)
        self.positions = {}
        self.touch = touch
        self.touch['board'] = {}
        self.touch['pos'] = {}

        self.touch['board']['left'] = None
        self.touch['board']['right'] = None
        self.touch['board']['bottom'] = None
        self.touch['board']['top'] = None

        self.touch['pos']['left'] = None
        self.touch['pos']['right'] = None
        self.touch['pos']['bottom'] = None
        self.touch['pos']['top'] = None

        self.top_left = 0, 0
        self.top = round(self.width[-1]/2), 0
        self.top_right = self.width[-1], 0

        self.right = self.width[-1], round(self.height[-1]/2)

        self.left = 0, round(self.height[-1]/2)

        self.bottom_left = 0, self.height[-1]
        self.bottom = round(self.width[-1]/2), self.height[-1]
        self.bttom_right = self.width[-1], self.height[-1]
        
        for x in self.width:
            for y in self.height:
                self.positions[x, y] = None
        self.icon_list = []
    def add_new_transition(self, side, board, pos):
        self.touch['board'][side] = board
        self.touch['pos'][side] = pos

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
                elif type(self.positions[x, y]) == Entity or issubclass(type(self.positions[x, y]), Entity):
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
    def __init__(self, name:str, x:int, y:int, icon:str, board:Board) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.icon = icon
        self.board = board
        self.board.positions[self.pos] = self
        self.board.icon_list.append(self)
        self.debug = False
    def create_multiple(self, x, y):
        
        if type(x) == range and type(y) == range:
            for x in x:
                for y in y:
                    self.board.positions[x -1, y-1] = Entity(self.name, x-1, y-1, self.icon, self.board)
        elif type(x) == range:
            for x in x:
                self.board.positions[x-1, y] = Entity(self.name, x-1, y, self.icon, self.board)
        elif type(y) == range:
            for y in y:
                self.board.positions[x, y-1] = Entity(self.name, x, y-1, self.icon, self.board)
        else:
            self.board.positions[x, y] = Entity(self.name, x, y, self.icon, self.board)

    def __repr__(self) -> str:
        return self.name

class Alive_Entity(Entity):
    def __init__(self, name: str, x: int, y: int, icon: str, board: Board, health=10, damage=1) -> None:
        super().__init__(name, x, y, icon, board)
        self.max_health = health
        self.health = health
        self.damage = damage
    def check_death(self):
        if self.health <= 0:
            self.board.positions[self.pos] = None
            self.x = None
            self.y = None
            self.pos = (self.x, self.y)


class Player(Alive_Entity):
    def __init__(self, name: str, x: int, y: int, icon: str, board: Board, cols={}) -> None:
        global current_board
        self.cols = cols
        current_board = board
        super().__init__(name, x, y, icon, board)

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
        self.__move__(1, 0, '+', self.board.touch['board']['right'], self.board.touch['pos']['right'])
                
    def move_left(self):
        self.__move__(1, 0, '-', self.board.touch['board']['left'], self.board.touch['pos']['left'])

    def move_up(self):
        self.__move__(0, 1, '-', self.board.touch['board']['top'], self.board.touch['pos']['top'])

    def move_down(self):
        self.__move__(0, 1, '+', self.board.touch['board']['bottom'], self.board.touch['pos']['bottom'])

    def add_new_collision(self, object, lambda_func):
        self.cols[object] = {'obj':object, 'func':lambda_func}


    def __move__(self, x_val:int, y_val:int, plus_or_minus:str, new_board:Board, new_pos):
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
            if new_board != None:
                global current_board
                self.board.positions[self.pos] = None
                self.board.icon_list.remove(self)
                current_board = new_board
                self.board = current_board
                self.board.icon_list.append(self)
                if new_pos != None:
                    self.pos = new_pos
                    self.x = new_pos[0]
                    self.y = new_pos[1]
                    self.board.positions[new_pos] = self
                else:
                    self.pos = 0, 0
                    self.x = 0
                    self.y = 0
                    self.board.positions[0, 0] = self
            else:
                print('Cannot move that way!')

    def __update_pos__(self):
        self.pos = (self.x, self.y)
        self.board.positions[self.pos] = self

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
            if keyboard.is_pressed('ctrl+shift+4'):
                quit()

class Wall(Entity):
    def __init__(self, x: int, y: int, icon: str, board: Board) -> None:
        super().__init__('Wall', x, y, icon, board)