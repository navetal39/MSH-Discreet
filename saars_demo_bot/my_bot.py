def do_turn(game):
    from classes import *
    if len(game.my_pirates()) == 0:
        return
    if game.get_turn() == 1:
        game.debug("Setting lists")
        global my_pirates
        global enemy_pirates
        global world_islands
        my_pirates = []
        enemy_pirates = []
        world_islands = []

        for pirate in game.my_pirates():
            my_pirates.append(My_Pirate(game, pirate))
            game.debug("+my")
        game.debug("my_pirates list is set")
        for pirate in game.enemy_pirates():
            enemy_pirates.append(Enemy_Pirate(game, pirate))
            game.debug("+enemy")
        game.debug("enemy_pirates list is set")
        for island in game.not_my_islands():
            world_islands.append(World_Island(island))
            game.debug("+island")
        game.debug("world_islands list is set")

    else:
        game.debug("Updating lists")
        for pirate in my_pirates:
            pirate.update_data(game)
            game.debug("^my")
        game.debug("my_pirates list updated")
        for pirate in enemy_pirates:
            pirate.update_data(game)
            game.debug("^enemy")
        game.debug("enemy_pirates list updated")
        for island in world_islands:
            island.update_data(game)
            game.debug("^island")
        game.debug("world_islands list updated")

    game.debug("Assigning pirates to islands")
    for pirate in my_pirates:
        if not pirate.pirate.is_lost:
            if not pirate.target is None and pirate.target.island.owner == game.ME:
                pirate.set_target(game, None)
            for island in world_islands:
                if (island.island.owner != game.ME or island.island.team_capturing != game.ME) and pirate.target is None:
                    pirate.set_target(game, island)
    
    game.debug("Setting sails")
    calls_for_help = {}
    idle_pirates = []
    for pirate in my_pirates:
        has_mission, new_location, help_ammount = pirate.move_towards_target(game, enemy_pirates)
        if not has_mission:
            game.debug(has_mission)
            idle_pirates.append(pirate)
        if help_ammount:
            calls_for_help[new_location] = help_ammount
    
    calls = sort_calls(calls_for_help)
    game.debug("giving missions to idle pirates")
    for mission in calls:
        help_ammount = calls_for_help[mission]
        if len(idle_pirates) >= help_ammount: # Enough pirates for the mission
            pirates_by_distance = get_pirates_for_mission(game, idle_pirates, mission)
            for i in xrange(help_ammount):
                pirates_by_distance[i].go_help(game, mission)
                idle_pirates.remove(pirates_by_distance[i])
        else: # No more piraets for this and any of the following missions
            break

def sort_calls(calls_dict):
    # Not efficient, but for such low numbers I don't care...
    sorted_list = []
    for i in xrange(5):
        for call in calls_dict.keys():
            if calls_dict[call] == i:
                sorted_list.append(call)
    return sorted_list

def get_pirates_for_mission(game, pirates, mission):
    pirates_and_distances = [(pirate, game.distance(pirate.pirate, mission)) for pirate in pirates]
    sorted_list = []
    while len(pirates_and_distances) > 0:
        min_dis = 256
        min_pir = None
        for pnd in pirates_and_distances:
            if pnd[1] <= min_dis:
                min_dis = pnd[1]
                min_pir = pnd[0]
        if not min_pir is None:
            sorted_list.append(min_pir)
            pirates_and_distances.remove((min_pir, min_dis))
    return sorted_list
