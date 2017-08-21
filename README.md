NpGameWorld
=============
NpGameWorld is very simple game engine in pure python, created for embedding. It is designed for games such as top-down shooters (Crimsonlands, etc.) where the player controls the hero, sending commands (like lists of dictionaries) to the world. World contains a hero, enemies and bullets. Enemies move to the hero and attack the hero in a collision. The hero needs to shoot at enemies and/or run away.

# About the world
* (0, 0) - point in the upper left corner of the world.
* All objects are circles.
* Coordinates of objects == coordinates of the centers of objects.
* Each object has the attributes `x` and `y` with the coordinates of its center.
* Each object also has the attributes `pad_x` and `pad_y`. They are the coordinates of the rectangle inscribed in a circle.
* The distance between objects is the distance between their centers.
* A collision occurs when the distance between the centers of objects A and B <= the radius of the object A + the radius of the object B.
* The world has a method called `world_gen`. It returns a generator object used to process the in-game cycle from starting a new game to the end of the game. So, the world has iterations, each object can do its actions at every iteration of the world, the enemies move to the hero, the bullets fly, the hero executes the player's command.
* At the end of each world iteration, the attribute of the world `world_stat`, which contains information about heroes, enemies, bullets, the status of the game, killed enemies, the number of iterations passed, etc., is updated.
* Bullets are destroyed in collisions.
* NpGameWorld doesn't have any graphics but you can draw some primitives on the client side. See `play_world.py` for the pygame example.

# How to start
* Create a world object  - `npgameworld.world.World`
* Setup a hero - `init_hero` world's method
* Setup new enemy type - `add_enemy_type` world's method
* Create generator for the game loop in the world - `world_gen` world's method
* Iterate generator and send commands to the hero while he is alive - the `send` method of the generator, commands are a list with dictionaries

See script `test_world.py` for example.

# Setup world
Create a world object from `npgameworld.world.World`. The constructor takes values

* `screen_width` - world's map width
* `screen_height` - - world's map height
* `start_enemies` - maximum number of enemies at the beginning of the game
* `enemies_max_iter_step` - frequency (in world iterations) of maximum number of enemies increase
* `spawn_dst` - minimal distance between the hero and the place where the enemy appears

# Setup hero
Use `init_hero` world's method

* `hp`
* `radius`
* `spd - speed`
* `bullet_radius`
* `bullet_spd` - bullet's speed
* `bullet_power` - how much damage will the enemies get in a collision with a bullet
* `reload_iters` - how many iterations the hero reload his weapon after one shot

# Setup new enemy type
You can add new enemies type into game with `add_enemy_type` world's method

* `unlock_iter` - with what iteration in the world will appear enemies. If `unlock_iter == 0` then enemies are unlocked on world start.
* `radius`
* `spd` - speed
* `power` - how much damage will the hero get in a collision with enemies
* `hp`

# Hero commands
* `'cmd' : 'move'`, sends with `xd` (x direction) and `yd` (y direction), can be 0 - stay, 1 - increase value (for example for x axis `'xd': 1` means moving right)
* `'cmd': 'shoot'`, sends with `x` and `y` - coordinates of shooting target.

Commands must be sent as a list with dictionaries like `[{'cmd': 'shoot', 'x': 114, 'y': 286}, {'cmd': 'move', 'xd': 1, 'yd': -1}]`.
