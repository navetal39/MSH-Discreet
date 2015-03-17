def patroll(game, pir):
    ''' Unimplemented. Yet... (#Libermna_Style)
    '''

    return (pir.id, 5-pir.id)

def compare_islands(island_data1, island_data2):
    if island_data1[0] > island_data2[0]:
        return island_data2
    else:
        return island_data1

def closest_island(game, pir, fleet, mission):
    potential_islands_list = game.not_my_islands()
    potential_locations = [i.location for i in potential_islands_list]

    for ship in fleet:
        if ship.location in potential_locations:
            return ship.location
        
    enemy_islands = game.enemy_islands()
    neutral_islands = game.neutral_islands()
    if len(enemy_islands) == 0 and len(neutral_islands):
        relevant_island_list = neutral_islands
    elif len(enemy_islands) and len(neutral_islands) == 0:
        relevant_island_list = enemy_islands
    elif len(enemy_islands) == 0 and len(neutral_islands) == 0:
        return patroll(game, pir)
    else:
        if mission == 'neutralize':
            relevant_island_list = enemy_islands
        else:
            relevant_island_list = neutral_islands
    directions_list = [(game.distance(pir, i), i) for i in relevant_island_list]
    closest_island_data = reduce(compare_islands, directions_list)
    return closest_island_data[1]
