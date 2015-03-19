def do_turn(game):
    from classes import *
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
                    game.debug("Attempting to assign pirate {} to island {}".format(pirate.pirate.id, island.island.id))
                    pirate.set_target(game, island)
    
    game.debug("Setting sails")
    for pirate in my_pirates:
        pirate.move_towards_target(game, enemy_pirates)
