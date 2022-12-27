import skills
from areas import Entity, Board
from utils import clear_screen
import time
area1 = Board(10, 5)



hi1 = Entity('player', 0, 0, 'i', area1)
hi2 = Entity('enemy', 1, 0, 'p', area1)
hi2.health = 0
hi2.check_death()
tickspeed = 20
hi1.cols[hi2] = {'obj':hi2, 'func':lambda: print('hello')}
clear_screen()
def main():
    print(hi1.pos)
    print(area1.create())
    time.sleep(4/tickspeed)
    hi1.start_movement_input()

while True:
    main()
