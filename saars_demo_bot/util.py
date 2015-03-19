def reverse_direction(game, direction):
    changes = {'n':'s', 's':'n', 'e':'w', 'w':'e', '-':'-'}
    try:
        return changes[direction]
    except Exception, e:
        game.debug('An error occured: '+e)
        return '-' # Default value
