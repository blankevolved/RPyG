class Skill:
    def __init__(self, name:str, max_xp:int):
        self.name = name
        self.xp = 0
        self.max_xp = max_xp
        self.level = 0

FARMING = Skill('farming', 50)