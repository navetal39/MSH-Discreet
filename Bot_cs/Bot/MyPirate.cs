using System;
using System.Collections.Generic;
using System.Linq;
using Pirates;

namespace PirateBot
{
    class MyPirate
    {
        public const int EVETION_DISTANCE = 6;


        public Pirate pirate;
        public WorldIsland target;
        public int power;

        public MyPirate(Pirate pirate)
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
            pirate = Bot.game.GetMyPirate(this.pirate.Id);
            CalculatePower();
            if (this.pirate.IsLost)
                SetTarget(null);
           Bot.game.Debug("{0} power: {2}, target: {1}", this.pirate, target != null ? target.island.ToString() : "null", power);
        }

        public void SetTarget(WorldIsland target)
        {
            if (target == null)
            {
                if (this.target != null)
                    this.target.target = null;
                Bot.game.Debug("pirate: {0}. Given target is null. target is changed from {1} to null", this.pirate.Id, this.target != null ? this.target.island.Id.ToString() : "null");
                this.target = target;
            }
            else if (target.target == null)
            {
                if (this.target != null)
                    this.target.target = null;
                Bot.game.Debug("pirate: {0}. Given target is {2}. target is changed from {1} to {2}", this.pirate.Id, this.target != null ? this.target.island.Id.ToString() : "null", target.island.Id);
                this.target = target;
                this.target.target = this;
            }
        }

        void CalculatePower()
        {
            power = 0;
            if (!this.pirate.IsLost && !Bot.game.isCapturing(this.pirate))
            {
                Pirate[] pirates = Bot.game.MyPirates().ToArray();
                power = 1;
                for (int i = 0; i < pirates.Length; i++)
                {
                    if (Bot.game.InRange(this.pirate, pirates[i]) && !pirates[i].IsCloaked && !Bot.game.isCapturing(pirates[i])) power++;
                }
            }
        }
        //run.bat bots\csharp\Bot bots\demoBot8.pyc
        public void MoveTowardsTarget()
        {
                if (!this.pirate.IsLost)
                    Bot.game.SetSail(this.pirate, determineNextMove());
        }

        private Direction determineNextMove()
        {
            List<Pirate> closeEnemies = new List<Pirate>();

            for (int i = 0; i < Bot.enemyPirates.Length; i++)
            {
                if (Bot.game.Distance(this.pirate, Bot.enemyPirates[i].pirate) < MyPirate.EVETION_DISTANCE &&
                    Bot.enemyPirates[i].power >= this.power)
                    closeEnemies.Add(Bot.enemyPirates[i].pirate);
            }

            if (closeEnemies.Count > 0)
            {
                Location pivot = determinePivot(this.pirate, closeEnemies);
                Direction[] diractions = Bot.game.GetDirections(this.pirate, pivot).ToArray();
                return Utils.NegDirec(diractions[diractions.Length/2]);
            }

            if (this.target != null)
                return Bot.game.GetDirections(this.pirate, this.target.island)[0];

            return Direction.NOTHING;
        }

        private static Location determinePivot(Pirate targetEscapey,IEnumerable<Pirate> collection)
        {
            Pirate[] pirates = collection.ToArray();
            int[] weights = new int[pirates.Length];

            int weightTot = 0;

            for (int i = 0; i < pirates.Length; i++)
            {
                int temp = MyPirate.EVETION_DISTANCE - Bot.game.Distance(targetEscapey, pirates[i]);
                weightTot += temp;
                weights[i] = temp;
            }

            Location result = new Location(0, 0);

            for (int i = 0; i < pirates.Length; i++)
            {
                result.Col += pirates[i].Loc.Col * weights[i];
                result.Row += pirates[i].Loc.Row * weights[i];
            }

            result.Col = result.Col / weightTot;
            result.Row = result.Row / weightTot;

            return result;
        }
    }
}
