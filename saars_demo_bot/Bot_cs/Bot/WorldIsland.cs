using System;
using System.Collections.Generic;
using System.Linq;
using Pirates;

namespace PirateBot
{
    class WorldIsland
    {
        public Island island;
        public MyPirate target;

        public WorldIsland(Island island)
        {
            this.island = island;
        }

        public void UpdateData(IPirateGame game)
        {
            island = game.GetIsland(this.island.Id);
            game.Debug("Island {0}, targeted by pirate: {1}", island.Id, target != null ? target.pirate.Id.ToString() : "null");
        }
    }
}

