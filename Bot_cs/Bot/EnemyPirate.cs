using System;
using System.Collections.Generic;
using System.Linq;
using Pirates;

namespace PirateBot
{
    class EnemyPirate
    {
        public Pirate pirate;
        public int power;

        public EnemyPirate(Pirate pirate)
        {
            this.pirate = pirate;
            CalculatePower();
        }

        public bool isCapturing()
        {
            return Bot.game.isCapturing(this.pirate);
        }

        public void UpdateData()
        {
            pirate = Bot.game.GetEnemyPirate(this.pirate.Id);
            CalculatePower();
            //Bot.game.Debug("{0}, target: {1}", this.pirate, target != null ? target.island.ToString() : "null");
        }

        void CalculatePower()
        {
            power = 0;
            if (!this.pirate.IsLost && !Bot.game.isCapturing(this.pirate))
            {
                Pirate[] pirates = Bot.game.EnemyPirates().ToArray();
                power = 1;
                for (int i = 0; i < pirates.Length; i++)
                {
                    if (Bot.game.InRange(this.pirate, pirates[i]) && !pirates[i].IsCloaked && !Bot.game.isCapturing(pirates[i])) power++;
                }
            }
        }
        
    }
}
