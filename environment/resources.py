#TODO: Implement Resource Classes 
class Berry:
    def __init__(self, position):
        self.position = position
        self.type = 'berry'

class Wood:
    def __init__(self, position):
        self.position = position
        self.type = 'wood'

class Animal:
    def __init__(self, position):
        self.position = position
        self.is_hunted = False
    
    
    def move(self):
        # Animal's movement behavior (random or stationary)
        pass
