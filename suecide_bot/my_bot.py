def do_turn(game):
    mpl = game.my_pirates()
    epl = game.enemy_pirates()
    tis = game.not_my_islands()
    for mp in mpl:
        ep = game.get_enemy_pirate(mp.id)
        if not ep.is_lost:
            dirs = game.get_directions(mp, ep)
        else:
            ti = tis[0]; tis.remove(ti)
            dirs = game.get_directions(mp, ti)
        game.set_sail(mp, dirs[0])
