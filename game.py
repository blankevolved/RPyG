import skills
from game_logic import Entity, Board, tickspeed
from utils import clear_screen
area1 = Board('Main Board', 9, 5)



player = Entity('player', 0, 0, 'p', area1)
hi2 = Entity('enemy', 4, 2, 'e', area1)

player.cols[hi2] = {'obj':hi2, 'func':lambda: print('hello')}
clear_screen()
def main():
    print(player.return_stats())
    print(area1.create())
    player.start_inputs()

while True:
    main()
