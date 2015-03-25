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

    idle = []
    game.debug("Assigning pirates to targets")
    for pirate in my_pirates:
        if not pirate.pirate.is_lost:
            if pirate.pirate.id > 0:
                if type(pirate.target) is World_Island and pirate.target.island.owner == game.ME:
                    pirate.set_target(game, None)
                for island in world_islands:
                    if (island.island.owner != game.ME or island.island.team_capturing != game.ME) and pirate.target is None:
                        pirate.set_target(game, island)
            elif pirate.pirate.id == 0: # Suecide bomber
                if not pirate.pirate.is_cloaked and game.can_cloak(): # Not ready
                    game.cloak(pirate.pirate)
                    continue
                else: # Ready
                    available_enemies = []
                    for enemy in enemy_pirates:
                        if not enemy.pirate.is_lost:
                            available_enemies.append((enemy, game.distance(pirate.pirate, enemy.pirate)))
                    if len(available_enemies): # There are enemies on the field
                        mini = available_enemies[0]; available_enemies.remove(mini)
                        for enemy in available_enemies:
                            if enemy[1] < mini[1]:
                                mini = enemy
                        pirate.set_target(game, mini[0])
                    else: # There are no enemies on the field
                        idle.append(pirate)
                    


                        
    game.debug("Setting sails")
    for pirate in my_pirates:
        moved = pirate.move_towards_target(game, enemy_pirates)
        if not moved:
            idle.append(pirate)
            
    game.debug("Assigning idle pirates to targets")
    for pirate in idle:
        if not pirate.pirate.is_lost:
            game.debug("pirate {} is idle for this turn".format(pirate.pirate.id))
