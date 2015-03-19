using System;
using System.Collections.Generic;
using System.Linq;
using Pirates;

namespace PirateBot
{
    class Utils
    {
        public static Direction NegDirec(Direction direction)
        {
            switch (direction)
            {
                case Direction.CLOAK:
                    return Direction.REVEAL;
                case Direction.EAST:
                    return Direction.WEST;
                case Direction.NORTH:
                    return Direction.SOUTH;
                case Direction.NOTHING:
                    return Direction.NOTHING;
                case Direction.REVEAL:
                    return Direction.CLOAK;
                case Direction.SOUTH:
                    return Direction.NORTH;
                case Direction.WEST:
                    return Direction.EAST;
                default:
                    return Direction.NOTHING;
            }
        }
    }
}
