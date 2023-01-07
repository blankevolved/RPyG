from game_logic import Entity, Board, Player, Wall, current_board



area2 = Board('2nd board', 10, 5)
area1 = Board('Main Board', 9, 5)
current_board = area1
player = Player('player', 0, 0, 'p', current_board)
hi2 = Entity('enemy', 4, 2, 'e', area2)
wall = Wall(None, None, '=', area1)

wall.create_multiple(range(10), 4)
wall.create_multiple(8, range(5))
player.add_new_collision(hi2, lambda: print('hello'))
area1.add_new_transition('left', area2, area2.right)
area2.add_new_transition('right', area1, area1.left)

def main():
    from game_logic import current_board
    player.board = current_board
    print(player.return_stats())
    print(current_board.create())
    player.start_inputs()

while True:
    main()
