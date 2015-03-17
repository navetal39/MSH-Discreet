def do_turn(game):
    from bot_utils import *
    global fleet1_target
    global fleet2_target
    fleet1 = []
    fleet2 = []
    # Fleet creation:
    for n in xrange(5):
        pirate_n = game.get_my_pirate(n)
        if not pirate_n.is_lost:
            if n <= 2:
                fleet1.append(pirate_n)
            else:
                fleet2.append(pirate_n)

    # Leader election:
    try:
        leader1 = fleet1[0]
    except IndexError: # All the fleet is out!
        leader1 = None
    try:
        leader2 = fleet2[0]
    except IndexError: # All the fleet is out!
        leader2 = None

    # Target selection:
    target1, mission1 = closest_island(game, leader1, fleet1, 'capture')
    target2, mission2 = closest_island(game, leader2, fleet2, 'neutralize')

    # Complete wipe-out prevention:
    if len(fleet1) == 1: #Fleet in danger
        target1 = leader1.initial_loc
    elif len(fleet2) == 1: # Fleet indanger!
        target2 = leader2.initial_loc
        
    # Collition prevention:
    if target1 == target2:
        target = target1
        mission = mission1 # Just so there won't be any confusion
        if mission != 'N/A':
            closer_fleet = compare_distances(game, leader1, leader2, target)
            if closer_fleet == 1:
                target2, new_mission = closest_island(game, leader2, fleet2, mission, target)
            else:
                target1, new_mission = closest_island(game, leader1, fleet1, mission, target)

    # Seting sail...etion?
    for pir in fleet1:
        try:
            direction = game.get_directions(pir, target1)
            game.debug(1)
            game.set_sail(pir, direction[0])
            game.debug(2)
        except Exception, e:
            game.debug(e)
    for pir in fleet2:
        try:
            direction = game.get_directions(pir, target2)
            game.debug(3)
            game.set_sail(pir, direction[0])
            game.debug(4)
        except Exception, e:
            game.debug(e)
