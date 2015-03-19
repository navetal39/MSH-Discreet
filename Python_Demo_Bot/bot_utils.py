def patroll(game, pir):
    ''' Unimplemented. Yet... (#Libermna_Style)
    '''

    return (pir.id, 5-pir.id)


def compare_islands(island_data1, island_data2):
    if island_data1[0] > island_data2[0]:
        return island_data2
    else:
        return island_data1

def compare_distances(game, pir1, pir2, target):
    distance1 = game.distance(pir1, target)
    distance2 = game.distance(pir2, target)
    if distance1 <= distance2:
        return 1
    else:
        return 2

def closest_island(game, pir, fleet, mission, targeted = ''):
    if pir is None: # If the fleet is dead
        return (0,0), 'N/A'
    
    if targeted == '': # Normal scenario
        
        potential_islands_list = game.not_my_islands()
        enemy_islands = game.enemy_islands()
        neutral_islands = game.neutral_islands()
        if len(enemy_islands) == 0 and len(neutral_islands):
            relevant_islands_list = neutral_islands
            actual_mission = 'capture'
        elif len(enemy_islands) and len(neutral_islands) == 0:
            relevant_islands_list = enemy_islands
            actual_mission = 'neutralize'
        else:
            actual_mission = mission
            if mission == 'neutralize':
                relevant_islands_list = enemy_islands
            else:
                relevant_islands_list = neutral_islands

        #If already on an island - stay on it!
        potential_locations = [i.location for i in potential_islands_list]
        for ship in fleet:
            if ship.location in potential_locations:
                return ship.location
            
    else: # A collision happened
        if mission == 'neutralize':
            relevant_islands_list = game.enemy_islands()
        elif mission == 'capture':
            relevant_islands_list = game.neutral_islands()
        else:
            pass
        relevant_islands_list.remove(targeted) # Remove the one that causes the conflict
        actual_mission = mission
        

    distances_list = [(game.distance(pir, i), i) for i in relevant_islands_list]
    if len(distances_list) == 0:
        return patroll(game, pir), 'patroll'
    else:
        closest_island_data = reduce(compare_islands, distances_list)
        return closest_island_data[1], actual_mission
