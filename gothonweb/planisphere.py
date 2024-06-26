# The provided code defines a text-based adventure game with multiple rooms and paths
# between them. Each room has a description, and players can navigate through the game by
# choosing actions in each room. The game engine is implemented using Flask, a Python web
# framework. It uses sessions to keep track of the player's progress and renders HTML
# templates to display the game interface. Players can interact with the game by selecting
# actions from a list of options presented in the web interface.

from random import randint
# from textwrap import dedent


class Room(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.paths = {}  # {"Option": Room}
        self.pathnames = self.paths.keys()

    def go(self, direction):
        """It is up to the engine to communicate the self.from"""
        return self.paths.get(direction, None)

    def add_paths(self, paths):
        self.paths.update(paths)


# Possible Actions:
"""
* Map
    − next_scene
    − opening_scene
* Engine
    − play
* Scene
    − enter  # will have to be overridden by child classes
    * Death
    * Central Corridor
    * Laser Weapon Armory
    * The Bridge
    * Escape Pod
"""


prompt = "> "


central_corridor = Room("Central Corridor",
"""
The Gothons of Planet Percal # 25 have invaded your ship and destroyed your entire crew.
You are the last surviving member and your last mission is to get the neutron destruct 
bomb from the Weapons Armory, put it in the bridge, and blow the ship up after getting
into an escape pod.\n\n

You're running down the central corridor to the Weapons Armory when a Gothon jumps out,
red scaly skin, dark grimy teeth, and evil clown costume flowing around his hate filled
body. He's blocking the door to the Armory and about to pull a weapon to blast you.
""")


laser_weapon_armory = Room("Lazer Weapon Armory",
"""
Lucky for you they made you learn Gothon insults in the academy. You tell the one Gothon
joke you know: Lbhe zbgure vf fb sng, jura fur fvgf nebhaq gur ubhfr, fur fvgf nebhaq gur
ubhfr. The Gothon stops, tries not to laugh, then busts out laughing and can't move.
While he's laughing you run up and shoot him square in the head putting him down, then
jump through the Weapon Armory door.\n\n

You do a dive roll into the Weapon Armory, crouch and scan the room for more Gothons that
might be hiding. It's dead quiet, too quiet. You stand up and run to the far side of the
room and find the neutron bomb in its container. There's a keypad lock on the box and you
need the code to get the bomb out. If you get the code wrong 10 times then the lock closes
forever and you can't get the bomb. The code is 3 digits.
""")


the_bridge = Room("The Bridge",
"""
The container clicks open and the seal breaks, letting gas out. You grab the neutron bomb
and run as fast as you can to the bridge where you must place it in the right spot.\n\n

You burst onto the Bridge with the neutron destruct bomb under your arm and surprise 5
Gothons who are trying to take control of the ship. Each of them has an even uglier
clown costume than the last. They haven't pulled their weapons out yet, as they see the
active bomb under your arm and don't want to set it off.
""")


escape_pod = Room("Escape Pod",
"""
You point your blaster at the bomb under your arm and the Gothons put their hands up and
start to sweat. You inch backward to the door, open it, and then carefully place the bomb
on the floor, pointing your blaster at it.  You then jump back through the door, punch the
close button and blast the lock so the Gothons can't get out. Now that the bomb is placed
you run to the escape pod to get off this tin can.\n\n

You rush through the ship desperately trying to make it to the escape pod before the whole
ship explodes. It seems like hardly any Gothons are on the ship, so your run is clear of
interference. You get to the chamber with the escape pods, and now need to pick one to
take. Some of them could be damaged but you don't have time to look. There's 5 pods,
which one do you take?
""")


the_end_winner = Room("The End Winner",
"""
You jump into pod {guess} and hit the eject button. The pod easily slides out
into space heading to the planet below. As it flies to the planet, you look 
back and see your ship implode then explode like a bright star, taking out the 
Gothon ship at the same time. You won!
""")


the_end_loser = Room("The End",
"""
You jump into a random pod and hit the eject button. \
The pod escapes out into the void of space, then implodes as the hull \
ruptures, crushing your body into jam jelly.
""")


player_death = Room("Death", "You died.")


central_corridor.add_paths({
    'shoot!': player_death,
    'dodge!': player_death,
    'tell a joke': laser_weapon_armory
})

laser_weapon_armory.add_paths({
    '0312': the_bridge,
    '*': player_death
})

the_bridge.add_paths({
    'slowly place the bomb': escape_pod,
    'throw the bomb': player_death
})

escape_pod.add_paths({
    '2': the_end_winner,
    '*': the_end_loser
})


START = 'Central Corridor'

rooms_list = [  # List of Room Objects
    central_corridor,
    escape_pod,
    the_bridge,
    laser_weapon_armory,
    player_death,
    the_end_winner,
    the_end_loser,
]

rooms = {}
terminating_rooms = {}

for room in rooms_list:  # Sets up Rooms dict object
    rooms.update({room.name: room})


def load_room(name):
    if name in rooms.keys():
        return rooms[name]


def name_room(room):
    for key, value in rooms.items():
        if value == room:
            return key
