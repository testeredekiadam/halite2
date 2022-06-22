
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging
from collections import OrderedDict

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("monkey_business")
# Then we print our start message to the logs
logging.info("Starting monkey business!")

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    """ We find the closest empty planets and closest enemy ships each turn
        and hold it into list ceplist for closest empty planets and ceslist for closest enemy ships.
        Then decide to attack a ship or occupying a planet.
        
        Further strategical options:
            1. Leave a planet free as bait
            2. attack the ships that go for that planet
            3. Order opponents according to the ship numbers/ planet numbers
            4. Go for bigger opponents
     """
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    # For every ship that I control
    for ship in game_map.get_me().all_ships():
        shipid = ship.id
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        # my team ships list
        tslist = game_map.get_me().all_ships()

        # get entities by distance
        ebdlist = game_map.nearby_entities_by_distance(ship)

        # sort entities according to the first element
        ebdlist = OrderedDict(sorted(ebdlist.items(), key=lambda t: t[0]))

        # list comprehension to find the closest empty planets sorted by distance
        ceplist = [ebdlist[distance][0] for distance in ebdlist if
                   isinstance(ebdlist[distance][0], hlt.entity.Planet)
                   and not ebdlist[distance][0].is_owned()]

        # list comprehension to find the closest enemy ships sorted by distance
        ceslist = [ebdlist[distance][0] for distance in ebdlist if
                   isinstance(ebdlist[distance][0], hlt.entity.Ship)
                   and ebdlist[distance][0] not in tslist]

        # occupy if there are unoccupied planets
        if len(ceplist) > 0:


    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
