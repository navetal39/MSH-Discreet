global EVASION_DISTANCE
EVASION_DISTANCE= 6

class World_Island(object):
    def __init__(self, island):
        self.island = island
        self.targets = []
        
    def update_data(self, game):
        self.island = game.get_island(self.island.id)
        target = [pirate.pirate.id for pirate in self.targets]
        game.debug("Island {}, targeted by pirates: {}".format(self.island.id, target))

        
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

    def set_target(self, game, target, force = False):
        if target is None: # Ship is lost - Release island
            if not self.target is None: 
                self.target.targets.remove(self) # Release the target
            self.target = target
        elif target.targets == [] or force: # Target exists and doesn't have a target yet
            if not self.target is None:
                self.target.targets.remove(self) # Release current target
            self.target = target
            self.target.targets.append(self)
            
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
            game.set_sail(self.pirate, self.get_direction(game, enemy_pirates))
        
    def get_direction(self, game, enemy_pirates):
        close_enemies = []
        for enemy in enemy_pirates:
            if game.distance(self.pirate, enemy.pirate) < EVASION_DISTANCE and enemy.power >= self.power:
                close_enemies.append(enemy.pirate)
                
        if len(close_enemies): # If there's danger
            pivot = self.get_pivot(game, close_enemies) # Get "Escape route"
            directions = game.get_directions(self.pirate, pivot)
            direction = self.reverse_direction(directions[game.get_turn()%2-1])
            turn_count = 0
            while not game.is_passable(game.destination(self.pirate, direction)):
                if turn_count == 2: # Prevent ship from running into the enemies
                    continue
                direction = self.turn_direction(direction)
                turn_count += 1
                if turn_count == 4: # Prevent never-ending loop
                    break
            return direction
        if not self.target is None:
            directions = game.get_directions(self.pirate, self.target.island)
            direction = directions[game.get_turn()%2-1]
            turn_count = 0
            while not game.is_passable(game.destination(self.pirate, direction)):
                direction = self.turn_direction(direction)
                turn_count += 1
                if turn_count == 4: # Prevent never-ending loop
                    break
            return direction
        return '-' # Default value
    
    def get_pivot(self, game, pirates):
        total_weight = 0
        weights = []
        for enemy in pirates:
            temp = EVASION_DISTANCE - game.distance(self.pirate, enemy)
            total_weight += temp
            weights.append(temp)

        row, col = 0, 0
        for i in xrange(len(pirates)):
            row += (pirates[i].location[0]*weights[i])
            col += (pirates[i].location[1]*weights[i])
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
    def turn_direction(self, direction):
        changes = {'n':'w', 's':'e', 'e':'n', 'w':'s', '-':'-'}
        try:
            return changes[direction]
        except Exception, e:
            game.debug('An error occured: '+e)
            return '-' # Default value
    
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
