using System;
using System.Collections.Generic;
using System.Linq;
using Pirates;

namespace PirateBot
{
    class Bot : Pirates.IPirateBot
    {
        public static IPirateGame game;

        MyPirate[] myPirates;
        public static EnemyPirate[] enemyPirates;
        WorldIsland[] worldIslands;

        public void DoTurn(IPirateGame game)
        {
            Bot.game = game;

            Pirate[] MPirates = game.MyPirates().ToArray();
            Pirate[] EPirates = game.EnemyPirates().ToArray();
            Island[] islands = game.NotMyIslands().ToArray();

            //For now: if there are no pirates avaliable do nothing.
            if (MPirates.Length == 0 )
                return;

            //Updating the data about the pirates.
            if (game.GetTurn() == 1)
            {
                game.Debug("Setting lists");
                myPirates = new MyPirate[MPirates.Length];
                Bot.enemyPirates = new EnemyPirate[EPirates.Length];
                worldIslands = new WorldIsland[islands.Length];
                for (int i = 0; i < myPirates.Length; i++)
                {
                    myPirates[i] = new MyPirate(MPirates[i]);
                }
                game.Debug("myPirates list is set");
                for (int i = 0; i < enemyPirates.Length; i++)
                {
                    Bot.enemyPirates[i] = new EnemyPirate(EPirates[i]);
                }
                game.Debug("enemyPirates list is set");
                for (int i = 0; i < worldIslands.Length; i++)
                {
                    worldIslands[i] = new WorldIsland(islands[i]);
                }
                game.Debug("worldIslands list is set");
            }
            else
            {
                game.Debug("Updating list");
                for (int i = 0; i < myPirates.Length; i++)
                {
                    myPirates[i].UpdateData();
                }
                for (int i = 0; i < enemyPirates.Length; i++)
                {
                    Bot.enemyPirates[i].UpdateData();
                }
                for (int i = 0; i < worldIslands.Length; i++)
                {
                    worldIslands[i].UpdateData(game);
                }
            }

            //assign pirates for islands.
            game.Debug("assining pirates to islands");
            for (int i = 0; i < myPirates.Length; i++)
            {
                if (!myPirates[i].pirate.IsLost)
                {
                    if (myPirates[i].target != null && myPirates[i].target.island.Owner == Consts.ME)
                    {
                        myPirates[i].SetTarget(null);
                    }
                    for (int j = 0; j < worldIslands.Length; j++)
                    {
                        if ((worldIslands[j].island.Owner != Consts.ME || worldIslands[j].island.TeamCapturing != Consts.ME) &&
                            myPirates[i].target == null)
                        {
                            game.Debug("atempting to assain pirate {0} to island {1}", myPirates[i].pirate.Id, worldIslands[j].island.Id);
                            myPirates[i].SetTarget(worldIslands[j]);
                        }
                    }
                }
            }

            //move pirates.
            for (int i = 0; i < myPirates.Length; i++)
            {
                myPirates[i].MoveTowardsTarget();
            }
        }
    }
}
