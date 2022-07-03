#
# Firat Erkol – 219204648
# Finn Doose-Bruns - 220200432
# Fiona Stürzekarn – 220200224
# Iana Mazur - 219204806
# Tobias Edrich - 218201941
#

import hlt

import logging
from collections import OrderedDict
import search
import assign

# GAME START


game = hlt.Game("monkey_business")
logging.info("Starting monkey business!")

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()


    # arrays to hold some informations
    # captured planets
    captured_planets = []
    # planets captured by me
    my_planets = []
    # non captured planets, planned to capture next
    non_captured_planned_planet = []

    # my attack ships
    attack_ships = []

    # defence&capture ships - no use at the moment, only to track the ship population. maybe I use it later.
    defcap_ships = []

    # keep the track of the ship assignment
    # saved_ships = attack_ships + defcap_ships

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []

    # my ships for for-loop
    my_ships = game_map.get_me().all_ships()

    # list comprehension to find enemy ships
    enemy_ships = [ship for ship in game_map._all_ships()
                   if ship not in my_ships]

    # For every ship that I control
    for ship in my_ships:

        # ship assignment
        assign.Assign.assign_ship(ship, defcap_ships, attack_ships)

        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        # planets for defcap ships
        defcap_empty_planets = search.Search.defcap_planet_search(ship, game_map)
        defcap_empty_planets_list = [defcap_empty_planets[distance][0] for distance in defcap_empty_planets]

        # ships for attack ships
        attack_ships_target_planets = search.Search.attack_ship_search(ship, game_map)
        attack_ships_target_planets_list = [attack_ships_target_planets[distance][0] for distance in
                                            attack_ships_target_planets]

        # get entities by distance
        nearby_entities = game_map.nearby_entities_by_distance(ship)
        # sort entities according to the first element
        nearby_entities = OrderedDict(sorted(nearby_entities.items(), key=lambda t: t[0]))

        # list comprehension to find the closest empty planets sorted by distance
        nearby_empty_planets = [nearby_entities[distance][0] for distance in nearby_entities
                                if
                                isinstance(nearby_entities[distance][0], hlt.entity.Planet)
                                and not nearby_entities[distance][0].is_owned()]

        # list comprehension to find the closest enemy ships sorted by distance
        nearby_enemy_ships = [nearby_entities[distance][0] for distance in nearby_entities
                              if
                              isinstance(nearby_entities[distance][0], hlt.entity.Ship)
                              and nearby_entities[distance][0] not in my_ships]

        # list comprehension to find my planets which have free docking place
        my_planet_nearby_not_full = [nearby_entities[distance][0] for distance in nearby_entities if
                                     isinstance(nearby_entities[distance][0], hlt.entity.Planet) and
                                     nearby_entities[distance][0].is_owned() and
                                     nearby_entities[distance][0].owner == ship.owner and not
                                     nearby_entities[distance][0].is_full() and
                                     nearby_entities[distance][0] not in captured_planets and
                                     nearby_entities[distance][0] not in non_captured_planned_planet]

        # list comprehension to find my closest ship to prevent friendly collision
        nearby_friendly_ships = [nearby_entities[distance][0] for distance in nearby_entities
                                 if isinstance(nearby_entities[distance][0], hlt.entity.Ship)
                                 and nearby_entities[distance][0] in my_ships]

        # mine if there is free docking place

        # find closest empty planets and capture them

        if len(my_planet_nearby_not_full) > 0:
            target_planet = my_planet_nearby_not_full[0]
            # decide to attack if ship is attack ship
            if ship in attack_ships:
                target_ship = nearby_enemy_ships[0]
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_ship),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)

            # check whether ship can dock
            elif ship.can_dock(target_planet):
                command_queue.append(ship.dock(target_planet))

            # travel to the planet
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)
                    captured_planets.append(target_planet)

        elif len(defcap_empty_planets_list) > 0:
            target_planet = defcap_empty_planets_list[0]
            if ship in attack_ships:
                target_ship = nearby_enemy_ships[0]
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_ship),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)

            elif ship.can_dock(target_planet):
                command_queue.append(ship.dock(target_planet))
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)

                if navigate_command:
                    command_queue.append(navigate_command)
                    non_captured_planned_planet.append(target_planet)

        # find ships to attack if they are close
        elif len(nearby_enemy_ships) > 0:
            target_ship = nearby_enemy_ships[0]
            navigate_command = ship.navigate(
                ship.closest_point_to(target_ship),
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                ignore_ships=False)

            if navigate_command:
                command_queue.append(navigate_command)

        elif len(attack_ships_target_planets_list) > 0:
            target_ship = attack_ships_target_planets_list[0]
            navigate_command = ship.navigate(
                ship.closest_point_to(target_ship),
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                ignore_ships=False)

            if navigate_command:
                command_queue.append(navigate_command)

    # Send our set of commands to the Halite engine for this turn
    logging.info("All ships %d" % len(game_map.get_me().all_ships()))
    logging.info("Attack ships %d" % len(attack_ships))
    logging.info("Enemy ships %d" % len(enemy_ships))
    logging.info("defcap empty list")
    if len(defcap_empty_planets_list) > 0:
        logging.info(defcap_empty_planets_list[0])
    # logging.info("nearby entity")
    # logging.info(nearby_entities)
    logging.info("nearby empty planets")
    logging.info(len(nearby_empty_planets))
    if len(nearby_empty_planets) > 0:
        logging.info(nearby_empty_planets[0])

    game.send_command_queue(command_queue)
    # TURN END
# GAME END
