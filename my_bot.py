def do_turn(game):
    from bot_utils import *
    global fleet1_target
    global fleet2_target
    fleet1 = []
    fleet2 = []
    # Fleet creation:
    for n in xrange(5):
        pirate_n = game.get_my_pirate(n)
        if n <= 2:
            fleet1.append(pirate_n)
        else:
            fleet2.append(pirate_n)
    # Leader election:
    leader1 = fleet1[0]
    leader2 = fleet2[0]
    for pir in fleet1:
        if pir.is_lost:
            continue
        else:
            leader1 = pir
    
    for pir in fleet2:
        if pir.is_lost:
            continue
        else:
            leader2 = pir

    #Target selection:
    target1 = closest_island(game, leader1, fleet1, 'neutralize')
    target2 = closest_island(game, leader2, fleet2, 'capture')

    #Seting sail...etion?
    for pir in fleet1:
        try:
            direction = game.get_directions(pir, target1)
            game.set_sail(pir, direction[0])
        except Exception, e:
            game.debug(e)
    for pir in fleet2:
        try:
            direction = game.get_directions(pir, target2)
            game.set_sail(pir, direction[0])
        except Exception, e:
            game.debug(e)
