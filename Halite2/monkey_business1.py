# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging
from collections import OrderedDict

# GAME START
game = hlt.Game("monkey_business1")
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
            5. Separate ships to attack and to occupy 
     """
    game_map = game.update_map()

    # number to separate the ships: 0 to n*.5 attack ships for n ships
    attack_ships_number = int(len(game_map.get_me().all_ships()) * .5)
    # arrays to hold some informations
    # captured planets
    captured_planets = []
    # planets captured by me
    my_planets = []
    # non captured planets, planned to capture next
    non_captured_planned_planet = []
    # my attack ships
    attack_ships = game_map.get_me().all_ships()[0:attack_ships_number]

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    # For every ship that I control
    for ship in game_map.get_me().all_ships():
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        # get entities by distance
        entities_by_distance_list = game_map.nearby_entities_by_distance(ship)
        # sort entities according to the first element
        entities_by_distance_list = OrderedDict(sorted(entities_by_distance_list.items(), key=lambda t: t[0]))

        # list comprehension to find the closest empty planets sorted by distance
        closest_empty_planets_list = [entities_by_distance_list[distance][0] for distance in entities_by_distance_list
                                      if
                                      isinstance(entities_by_distance_list[distance][0], hlt.entity.Planet)
                                      and not entities_by_distance_list[distance][0].is_owned()]

        # get my team ships list
        my_ships = game_map.get_me().all_ships()

        # list comprehension to find the closest enemy ships sorted by distance
        closest_enemy_ships_list = [entities_by_distance_list[distance][0] for distance in entities_by_distance_list
                                      if
                                      isinstance(entities_by_distance_list[distance][0], hlt.entity.Ship)
                                      and entities_by_distance_list[distance][0] not in my_ships]

        # list comprehension to find my planets which have free docking place
        closest_my_planet_notFull = [entities_by_distance_list[distance][0] for distance in entities_by_distance_list if
                                     isinstance(entities_by_distance_list[distance][0], hlt.entity.Planet) and
                                     entities_by_distance_list[distance][0].is_owned() and
                                     entities_by_distance_list[distance][0].owner == ship.owner and not
                                     entities_by_distance_list[distance][0].is_full() and
                                     entities_by_distance_list[distance][0] not in captured_planets and
                                     entities_by_distance_list[distance][0] not in non_captured_planned_planet]



        # try to mine if there are uncaptured planets
        if len(closest_empty_planets_list) > 0:
            target_planet = closest_empty_planets_list[0]
            if ship.can_dock(target_planet):
                command_queue.append(ship.dock(target_planet))

            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

        # find ships to attack if they are close
        elif len(closest_enemy_ships_list) > 0:
            target_ship = closest_enemy_ships_list[0]
            navigate_command = ship.navigate(
                ship.closest_point_to(target_ship),
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                ignore_ships=False)

            if navigate_command:
                command_queue.append(navigate_command)

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
