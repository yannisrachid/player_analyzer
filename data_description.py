table_data = """
| Variable     | Data Type    | Description    | Stats Type    |
|------|-----|-----|-----|
| `Gls`    | float64    | **Goals**. Goals scored or allowed     | Standard Stats     |
| `Ast`    | float64    | **Assists**     | Standard Stats     |
| `G-PK`    | float64    | **Non-Penalty Goals**     | Standard Stats     |
| `PK`    | float64    | **Penalty Kicks Made**    | Standard Stats     |
| `PKatt`    | float64    | **Penalty Kicks Attempted**    | Standard Stats     |
| `CrdY`    | float64    | **Yellow Cards**    | Standard Stats     |
| `CrdR`    | float64    | **Red Cards**    | Standard Stats     |
| `G+A`    | float64    | **Goals Scored per 90 minutes**. Minimum 30 minutes played per squad game to qualify as a leader    | Standard Stats     |
| `G+A-PK`    | float64    | **Goals plus Assists minus Penalty Kicks made per 90 minutes**. Minimum 30 minutes played per squad game to qualify as a leader    | Standard Stats     |
| `xG`    | float64    | **Expected Goals**. xG totals include penalty kicks, but do not include penalty shootouts.     | Standard Stats     |
| `npxG`    | float64    | **Non-Penalty Expected Goals per 90 minutes**. Minimum 30 minutes played per squad game to qualify as a leader     | Standard Stats     |
| `xA`    | float64    | **xG Assisted**. xG which follows a pass that assists a shot.     | Standard Stats     |
| `npxG+xA`    | float64    | **Non-Penalty Expected Goals plus xG Assisted per 90 minutes**. Minimum 30 minutes played per squad game to qualify as a leader    | Standard Stats     |
| `xG+xA`    | float64    | **Expected Goals plus Assist per 90 minutes**. xG totals include penalty kicks, but do not include penalty shootouts (unless otherwise noted). Minimum 30 minutes played per squad game to qualify as a leader    | Standard Stats     |
| `Sh`    | float64    | **Shots Total**. Does not include penalty kicks.    | Shooting Stats     |
| `SoT`    | float64    | **Shots on target**. Note: Shots on target do not include penalty kicks.     | Shooting Stats     |
| `SoT%`    | float64    | **Shots on target percentage**. Percentage of shots that are on target. Minimum .395 shots per squad game to qualify as a leader. Note: Shots on target do not include penalty kicks    | Shooting Stats     |
| `Sh/90`    | float64    | **Shots total per 90 minutes**. Minimum 30 minutes played per squad game to qualify as a leader    | Shooting Stats     |
| `SoT/90`    | float64    | **Shots on target per 90 minutes**. Minimum 30 minutes played per squad game to qualify as a leader. Note: Shots on target do not include penalty kicks    | Shooting Stats     |
| `G/Sh`    | float64    | **Goals per shot**. Minimum .395 shots per squad game to qualify as a leader.    | Shooting Stats     |
| `G/SoT`    | float64    | **Goals per shot on target**. Minimum .111 shots on target per squad game to qualify as a leader. Note: Shots on target do not include penalty kicks.    | Shooting Stats     |
| `Dist`    | float64    | **Average distance, in yards, from goal of all shots taken**. Minimum .395 shots per squad game to qualify as a leader. Does not include penalty kicks.    | Shooting Stats     |
| `FK`    | float64    | **Shots from free kicks**.     | Shooting Stats     |
| `npxG/Sh`    | float64    | **Non-Penalty Expected Goals per shot**. Minimum .395 shots per squad game to qualify as a leader.    | Shooting Stats     |
| `G-xG`    | float64    | **Goals minus Expected Goals**. xG totals include penalty kicks, but do not include penalty shootouts (unless otherwise noted).     | Shooting Stats     |
| `np:G-xG`    | float64    | **Non-Penalty Goals minus Non-Penalty Expected Goals**. xG totals include penalty kicks, but do not include penalty shootouts (unless otherwise noted).     | Shooting Stats     |
| `Cmp`    | float64    | **Passes Completed**.    | Passing Stats     |
| `Att`    | float64    | **Passes Attempted**.    | Passing Stats     |
| `Cmp%`    | float64    | **Pass Completion Percentage**. Minimum 30 minutes played per squad game to qualify as a leader    | Passing Stats     |
| `TotDist`    | float64    | **Total distance, in yards, that completed passes have traveled in any direction**.    | Passing Stats     |
| `PrgDist`    | float64    | **Progressive Distance**. Total distance, in yards, that completed passes have traveled towards the opponent's goal. Note: Passes away from opponent's goal are counted as zero progressive yards.    | Passing Stats     |
| `A-xA`    | float64    | **Assists minus xG Assisted**.     | Passing Stats     |
| `KP`    | float64    | **Passes that directly lead to a shot (assisted shots)**.    | Passing Stats     |
| `1/3`    | float64    | **Completed passes that enter the 1/3 of the pitch closest to the goal**. Not including set pieces.    | Passing Stats     |
| `PPA`    | float64    | **Completed passes into the 18-yard box**. Not including set pieces.    | Passing Stats     |
| `CrsPA`    | float64    | **Completed crosses into the 18-yard box**. Not including set pieces.    | Passing Stats     |
| `Prod`    | float64    | **Progressive Passes**. Completed passes that move the ball towards the opponent's goal at least 10 yards from its furthest point in the last six passes, or any completed pass into the penalty area. Excludes passes from the defending 40% of the pitch     | Passing Stats     |
| `Live`    | float64    | **Live-ball passes**.    | Pass Type Stats     |
| `Dead`    | float64    | **Dead-ball passes**. Includes free kicks, corner kicks, kick offs, throw-ins and goal kicks.    | Pass Type Stats     |
| `TB`    | float64    | **Completed pass sent between back defenders into open space**.    | Pass Type Stats     |
| `Press`    | float64    | **Passes made while under pressure from opponent**.    | Pass Type Stats     |
| `Sw`    | float64    | **Passes that travel more than 40 yards of the width of the pitch**.    | Pass Type Stats     |
| `Crs`    | float64    | **Crosses**.    | Pass Type Stats     |
| `CK`    | float64    | **Corner Kicks**.    | Pass Type Stats     |
| `In`    | float64    | **Inswinging Corner Kicks**.    | Pass Type Stats     |
| `Out`    | float64    | **Outswinging Corner Kicks**.    | Pass Type Stats     |
| `Str`    | float64    | **Straight Corner Kicks**.    | Pass Type Stats     |
| `Groud`    | float64    | **Ground passes**.    | Pass Type Stats     |
| `Low`    | float64    | **Passes that leave the ground, but stay below shoulder-level**.    | Pass Type Stats     |
| `High`    | float64    | **Passes that are above shoulder-level at the peak height**.    | Pass Type Stats     |
| `Left`    | float64    | **Passes attempted using left foot**.    | Pass Type Stats     |
| `Right`    | float64    | **Passes attempted using right foot**.    | Pass Type Stats     |
| `Head`    | float64    | **Passes attempted using head**.    | Pass Type Stats     |
| `TI`    | float64    | **Throw-Ins taken**.    | Pass Type Stats     |
| `Other`    | float64    | **Passes attempted using body parts other than the player's head or feet.**    | Passing Stats     |
| `Off`    | float64    | **Offsides**.    | Passing Stats     |
| `Int`    | float64    | **Intercepted**.    | Passing Stats     |
| `Blocks`    | float64    | **Blocked by the opponent who was standing it the path**.    | Passing Stats     |
| `SCA`    | float64    | **Shot-Creating Actions**. The two offensive actions directly leading to a shot, such as passes, dribbles and drawing fouls. Note: A single player can receive credit for multiple actions and the shot-taker can also receive credit.    | Goal and Shot Creation Stats     |
| `SCA90`    | float64    | **Shot-Creating Actions per 90 minutes**. Minimum 30 minutes played per squad game to qualify as a leader    | Goal and Shot Creation Stats     |
| `PassLive`    | float64    | **Completed live-ball passes that lead to a shot attempt**.    | Goal and Shot Creation Stats     |
| `PassDead`    | float64    | **Completed dead-ball passes that lead to a shot attempt**. Includes free kicks, corner kicks, kick offs, throw-ins and goal kicks.    | Goal and Shot Creation Stats     |
| `Drib`    | float64    | **Successful dribbles that lead to a shot attempt**.    | Goal and Shot Creation Stats     |
| `Fld`    | float64    | **Fouls drawn that lead to a shot attempt**.    | Goal and Shot Creation Stats     |
| `Def`    | float64    | **Defensive actions that lead to a shot attempt**.    | Goal and Shot Creation Stats     |
| `GCA`    | float64    | **Goal-Creating Actions**. The two offensive actions directly leading to a goal, such as passes, dribbles and drawing fouls. Note: A single player can receive credit for multiple actions and the shot-taker can also receive credit.    | Goal and Shot Creation Stats     |
| `GCA90`    | float64    | **Goal-Creating Actions per 90 minutes**. Minimum 30 minutes played per squad game to qualify as a leader.    | Goal and Shot Creation Stats     |
| `Tkl`    | float64    | **Number of players tackled**.    | Defensive Action Stats     |
| `TklW`    | float64    | **Tackles in which the tackler's team won possession of the ball**.    | Defensive Action Stats     |
| `Def 3rd`    | float64    | **Tackles in defensive 1/3**.    | Defensive Action Stats     |
| `Mid 3rd`    | float64    | **Tackles in middle 1/3**.    | Defensive Action Stats     |
| `Att 3rd`    | float64    | **Tackles in attacking 1/3**.    | Defensive Action Stats     |
| `Tkl%`    | float64    | **Percentage of dribblers tackled**. Dribblers tackled divided by dribblers tackled plus times dribbled past. Minimum .625 dribblers contested per squad game to qualify as a leader.    | Defensive Action Stats     |
| `Past`    | float64    | **Number of times dribbled past by an opposing player**.    | Defensive Action Stats     |
| `Succ`    | float64    | **Number of times the squad gained possession withing five seconds of applying pressure**.    | Defensive Action Stats     |
| `%`    | float64    | **Successful Pressure Percentage**. Percentage of time the squad gained possession withing five seconds of applying pressure. Minimum 6.44 pressures per squad game to qualify as a leader    | Defensive Action Stats     |
| `ShSv`    | float64    | **Number of times blocking a shot that was on target, by standing in its path**.    | Defensive Action Stats     |
| `Pass`    | float64    | **Number of times blocking a pass by standing in its path**.    | Defensive Action Stats     |
| `Tkl+Int`    | float64    | **Number of players tackled plus number of interceptions**.    | Defensive Action Stats     |
| `Clr`    | float64    | **Clearances**.    | Defensive Action Stats     |
| `Err`    | float64    | **Mistakes leading to an opponent's shot**.    | Defensive Action Stats     |
| `Touches`    | float64    | **Number of times a player touched the ball**. Note: Receiving a pass, then dribbling, then sending a pass counts as one touch.    | Possession Stats     |
| `Def Pen`    | float64    | **Touches in defensive penalty area**.    | Possession Stats     |
| `Att Pen`    | float64    | **Touches in attacking penalty area**.    | Possession Stats     |
| `Succ%`    | float64    | **Percentage of Dribbles Completed Successfully**. Minimum .5 dribbles per squad game to qualify as a leader    | Possession Stats     |
| `#Pl`    | float64    | **Number of Players Dribbled Past**.    | Possession Stats     |
| `Megs`    | float64    | **Number of times a player dribbled the ball through an opposing player's legs**.    | Possession Stats     |
| `Carries`    | float64    | **Total number of times a player controls the ball with their feet**.    | Possession Stats     |
| `TotDist`    | float64    | **Total distance, in yards, a player moved the ball while carrying.**. Minimum 30 minutes played per squad game to qualify as a leader.    | Possession Stats     |
| `PrgDist`    | float64    | **Progressive distance**. Total distance, in yards, a player moved the ball forward while carrying.    | Possession Stats     |
| `Miscon`    | float64    | **Miscontrols**.    | Possession Stats     |
| `Dispos`    | float64    | **Dispossessed**.    | Possession Stats     |
| `Targ`    | float64    | **Targets. The number of passes received**.    | Possession Stats     |
| `Rec`    | float64    | **Receptions**.    | Possession Stats     |
| `Rec%`    | float64    | **Reception Percentage**.    | Possession Stats     |
| `Prog`    | float64    | **Progressive Passes**. Passes that move the ball towards the opponent's goal at least 10 yards from its furthest point in the last six passes, or any completed pass into the penalty area. Excludes passes from the defending 40% of the pitch     | Possession Stats     |
"""