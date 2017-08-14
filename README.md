NpGameWorld
===========
NpGameWorld is very simple pure python game engine created for embedding. It designed for games like top-down shooters (crimsonlands, etc). World contains hero and enemies. Hero controlled by player, player need to send dictionaries with commands about hero's actions to world. Enemies just moves to hero and hit hero on collisions. 

# About world
* 0, 0 - point in left upper corner of world.
* All objects are circles.
* Coordinates of objects == coordinates of objects's centers .
 * Every object has `x` and `y` attributes with coordinates of his center.
 * But also every object has `pad_x` and `pad_y` attributes. They are coordinates of rectangle for incircle.
 * Distance between objects is distance between them centers.
* Collision becames when distance between object A and object B centers <= object A radius + object B radius.
* World have `world_gen` method. It returns a generator object used for processing in-game loop from new game start up to gameover. So world has iterations, every object can do his actions on every world's iteration, enemy moves to hero, bullets flyes, hero does player's command.
* In the end of every world iteration updates world's attribute `world_stat` which contains information about hero, enemies, bullets, game status, killed enemies, count of passed iterations, etc.
* Bullets destroys on collisions.
* NpGameWorld doesn't have any graphics but you can draw any primitives on client side. See `play_world.py` for pygame example. 

# How to start
* Create world object  - `npgameworld.world.World`
* Setup hero - `init_hero` world's method
* Setup new enemy type - `add_enemy_type` world's method
* Create generator for world's game loop - `world_gen` world's method
* Iterate generator and send commands to hero while he is alive - `send` generator's method, commands are list with dictionaries

See script `test_world.py` for example.

# Setup world
Create world object from `npgameworld.world.World`. Constructor got

* `screen_width` - world's map width
* `screen_height` - - world's map height
* `start_enemies` - max enemies count on game start
* `enemies_max_iter_step` - how often (in world iterations) max enemies count will increase
* `spawn_dst` - minimal distance beween hero and enemy on enemy spawn

# Setup hero
Use `init_hero` world's method

* `hp`
* `radius`
* `spd - speed`
* `bullet_radius`
* `bullet_spd` - bullet's speed
* `bullet_power` - how much damage will got enemy on collision with bullet
* `reload_iters` - how much iteration hero reload his gun after one shot

# Setup new enemy type
You can add new enemy type into game with `add_enemy_type` world's method

* `unlock_iter` - from which world's iteration enemy can spawns. If `unlock_iter == 0` then enemy unlocked with world start. 
* `radius`
* `spd` - speed
* `power` - how much damage will get hero on collision with enemy
* `hp`

# Hero commands
* `'cmd' : 'move'`, sends with `xd` (x direction) and `yd` (y direction), can be 0 - stay, 1 - increase value (for example for x axis `'xd': 1` means moving right)
* `'cmd': 'shoot'`, sends with `x` and `y` - coordinates of shooting target.

Commands neet to be send as list with dictionaries like `[{'cmd': 'shoot', 'x': 114, 'y': 286}, {'cmd': 'move', 'xd': 1, 'yd': -1}]`.


