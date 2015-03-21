global EVASION_DISTANCE
EVASION_DISTANCE= 6

class World_Island(object):
    def __init__(self, island):
        self.island = island
        self.target = None
        
    def update_data(self, game):
        self.island = game.get_island(self.island.id)
        if self.target is None:
            target = None
        else:
            target = self.target.pirate.id

        
class My_Pirate(object):
    def __init__(self, game, pirate):
        self.pirate = pirate
        self.power = self.calculate_power(game)
        self.target = None
        
    def is_capturing(self, game):
        return game.is_capturing(self.pirate)
    
    def update_data(self, game):
        self.pirate = game.get_my_pirate(self.pirate.id)
        self.power = self.calculate_power(game)
        if (self.pirate.is_lost):
            self.set_target(game, None)

    def set_target(self, game, target):
        if target is None: # Ship is lost - Release island
            if not self.target is None: 
                self.target.target = None # Release the target
            self.target = target
        elif target.target is None: # Target exists and doesn't have a target yet
            if not self.target is None:
                self.target.target = None # Release current target
            self.target = target
            self.target.target = self
            
    def calculate_power(self, game):
        power = 0
        if not self.pirate.is_lost and not self.is_capturing(game): # If pirate is free
            pirates = game.my_pirates()
            power = 1
            for pirate in pirates:
                if (game.in_range(self.pirate, pirate) and not pirate.is_cloaked and not game.is_capturing(pirate)):
                    power += 1
        return power
    
    def move_towards_target(self, game, enemy_pirates):
        if not self.pirate.is_lost:
            direction, close_enemies = self.get_direction(game, enemy_pirates) # Get info
            enemy_powers = [0] #If there are no powers the max function will pick the 0
            for enemy in close_enemies:
                enemy_powers.append(enemy.power)
            max_enemy_power = max(enemy_powers) # Biggest danger
            power_dif = max_enemy_power - self.power if not self.is_capturing(game) else max_enemy_power - self.power + 1 # If self is capturing it will run away in this turn, thus it will regain it's power
            if direction != '-':
                game.set_sail(self.pirate, direction)
                has_mission = False
            else: # pirate has nothing to do
                has_mission = True
            return has_mission, self.pirate.location, power_dif
        else:
            return True, self.pirate.initial_loc, 0 # Returns true just so the script won't attempt to let him help
        
    def get_direction(self, game, enemy_pirates):
        close_enemies = []
        for enemy in enemy_pirates:
            if game.distance(self.pirate, enemy.pirate) < EVASION_DISTANCE and enemy.power >= self.power:
                close_enemies.append(enemy)
                
        if len(close_enemies): # If there's danger
            pivot = self.get_pivot(game, close_enemies) # Get "Escape route"
            directions = game.get_directions(self.pirate, pivot)
            return self.reverse_direction(directions[-1]), close_enemies
        if not self.target is None:
            game.debug(str((self.pirate.id, self.target.island)))
            return game.get_directions(self.pirate, self.target.island)[0], close_enemies
        return '-', close_enemies
    
    def get_pivot(self, game, pirates):
        total_weight = 0
        weights = []
        for enemy in pirates:
            temp = EVASION_DISTANCE - game.distance(self.pirate, enemy.pirate)
            total_weight += temp
            weights.append(temp)

        row, col = 0, 0
        for i in xrange(len(pirates)):
            row += (pirates[i].pirate.location[0]*weights[i])
            col += (pirates[i].pirate.location[1]*weights[i])
        col = int(col/total_weight)
        row = int(row/total_weight)
        return (row, col)

    def reverse_direction(self, direction):
        changes = {'n':'s', 's':'n', 'e':'w', 'w':'e', '-':'-'}
        try:
            return changes[direction]
        except Exception, e:
            game.debug('An error occured: '+e)
            return '-' # Default value
    
    def go_help(self, game, target):
        directions = game.get_directions(self.pirate, target)
        game.set_sail(self.pirate, directions[-1])
        
    
class Enemy_Pirate(object):
    def __init__(self, game, pirate):
        self.pirate = pirate
        self.power = self.calculate_power(game)
        
    def is_capturing(self, game):
        return game.is_capturing(self.pirate)
    
    def update_data(self, game):
        self.pirate = game.get_enemy_pirate(self.pirate.id)
        self.power = self.calculate_power(game)
        
    def calculate_power(self, game):
        power = 0
        if not self.pirate.is_lost and not self.is_capturing(game): # If pirate is free
            pirates = game.enemy_pirates()
            power = 1
            for pirate in pirates:
                if (game.in_range(self.pirate, pirate) and not pirate.is_cloaked and not game.is_capturing(pirate)):
                    power += 1
        return power
