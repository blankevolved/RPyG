from os import name, system

class Error:
    def cannot_move_x(x:str):
        return 'Cannot move ' + x

def clear_screen():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')