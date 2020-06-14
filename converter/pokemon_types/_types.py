class BaseType:
	"""This is type that will be used for all pokemon_types, everything defaults to 1
	with the different pokemon_types changing type properties as needed."""
	normal = 1.0
	fire = 1.0
	water = 1.0
	electric = 1.0
	grass = 1.0
	ice = 1.0
	fighting = 1.0
	poison = 1.0
	ground = 1.0
	flying = 1.0
	psychic = 1.0
	bug = 1.0
	rock = 1.0
	ghost = 1.0
	dragon = 1.0
	dark = 1.0
	steel = 1.0
	fairy = 1.0


Normal = BaseType()
Normal.fighting = 2.0
Normal.ghost = 0.0

Fire = BaseType()
Fire.fire = 0.5
Fire.water = 2.0
Fire.grass = 0.5
Fire.ice = 0.5
Fire.ground = 2.0
Fire.bug = 0.5
Fire.rock = 2.0
Fire.steel = 0.5
Fire.fairy = 0.5

Water = BaseType()
Water.fire = 0.5
Water.water = 0.5
Water.electric = 2.0
Water.grass = 2.0
Water.ice = 0.5
Water.steel = 0.5

Electric = BaseType()
Electric.electric = 0.5
Electric.ground = 2.0
Electric.flying = 0.5
Electric.steel = 0.5

Grass = BaseType()
Grass.fire = 2.0
Grass.water = 0.5
Grass.electric = 0.5
Grass.grass = 0.5
Grass.ice = 2.0
Grass.poison = 2.0
Grass.ground = 0.5
Grass.flying = 2.0
Grass.bug = 2.0

Ice = BaseType()
Ice.fire = 2.0
Ice.ice = 0.5
Ice.fighting = 2.0
Ice.rock = 2.0
Ice.steel = 2.0

Fighting = BaseType()
Fighting.flying = 2.0
Fighting.psychic = 2.0
Fighting.bug = 0.5
Fighting.rock = 0.5
Fighting.dark = 0.5
Fighting.fairy = 2.0

Poison = BaseType()
Poison.grass = 0.5
Poison.fighting = 0.5
Poison.poison = 0.5
Poison.ground = 2.0
Poison.psychic = 2.0
Poison.bug = 0.5
Poison.fairy = 0.5

Ground = BaseType()
Ground.water = 2.0
Ground.electric = 0.0
Ground.grass = 2.0
Ground.ice = 2.0
Ground.poison = 0.5
Ground.rock = 0.5

Flying = BaseType()
Flying.electric = 2.0
Flying.grass = 0.5
Flying.ice = 2.0
Flying.fighting = 0.5
Flying.ground = 0.0
Flying.bug = 0.5
Flying.rock = 2.0

Psychic = BaseType()
Psychic.fighting = 0.5
Psychic.psychic = 0.5
Psychic.bug = 2.0
Psychic.ghost = 2.0
Psychic.dark = 2.0


Bug = BaseType()
Bug.fire = 2.0
Bug.grass = 0.5
Bug.fighting = 0.5
Bug.ground = 0.5
Bug.flying = 2.0
Bug.rock = 2.0


Rock = BaseType()
Rock.normal = 0.5
Rock.fire = 0.5
Rock.water = 2.0
Rock.grass = 2.0
Rock.fighting = 2.0
Rock.poison = 0.5
Rock.ground = 2.0
Rock.flying = 0.5
Rock.steel = 2.0

Ghost = BaseType()
Ghost.normal = 0.0
Ghost.fighting = 0.0
Ghost.poison = 0.5
Ghost.bug = 0.5
Ghost.ghost = 2.0
Ghost.dark = 2.0

Dragon = BaseType()
Dragon.fire = 0.5
Dragon.water = 0.5
Dragon.electric = 0.5
Dragon.grass = 0.5
Dragon.ice = 2.0
Dragon.dragon = 2.0
Dragon.fairy = 2.0

Dark = BaseType()
Dark.fighting = 2.0
Dark.psychic = 0.0
Dark.bug = 2.0
Dark.ghost = 0.5
Dark.dark = 0.5
Dark.fairy = 2.0

Steel = BaseType()
Steel.normal = 0.5
Steel.fire = 2.0
Steel.grass = 0.5
Steel.ice = 0.5
Steel.fighting = 2.0
Steel.poison = 0.0
Steel.ground = 2.0
Steel.flying = 0.5
Steel.psychic = 0.5
Steel.bug = 0.5
Steel.rock = 0.5
Steel.dragon = 0.5
Steel.steel = 0.5
Steel.fairy = 0.5

Fairy = BaseType()
Fairy.fighting = 0.5
Fairy.poison = 2.0
Fairy.bug = 0.5
Fairy.dragon = 0.0
Fairy.dark = 0.5
Fairy.steel = 2.0
