# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging
from collections import OrderedDict
import search

# GAME START


game = hlt.Game("monkey_business2")
logging.info("Starting monkey business!")

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    """ We find the closest empty planets and closest enemy ships each turn
        and hold it into list nearby empty planets for closest empty planets and nearby enemy ships for closest enemy ships.
        Then decide to attack a ship or occupying a planet.
        
        Further strategical options:
            1. Leave a planet free as bait
            2. attack the ships that go for that planet
            3. Order opponents according to the ship numbers/ planet numbers
            4. Go for bigger opponents
            5. Separate ships to attack and to occupy (Done)
            7. Avoid collisions
            8. first attack center - then cover the opponent's planets
            9. more than 2 players -> go for the outer planet and capture planets while
            others fight with each other
            10. defcap attack if a ship is docked on planet, then capture
            11. defcap search planets. cost = distance, profit = dockable_port
            12. attack search. cost = distance, profit = docked_ship_number
     """
    game_map = game.update_map()

    mapX = game_map.width
    mapY = game_map.height

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
    saved_ships = attack_ships + defcap_ships

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
        if ship not in saved_ships:
            if len(defcap_ships) * 0.2 <= len(attack_ships):
                defcap_ships.append(ship)
            else:
                attack_ships.append(ship)

        # to assign ships to attack / defence&capture
        ship_id = ship.id

        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue




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

        planets_inside_out = []

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

        elif len(nearby_empty_planets) > 0:
            target_planet = nearby_empty_planets[0]
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

    # Send our set of commands to the Halite engine for this turn
    logging.info("All ships %d" % len(game_map.get_me().all_ships()))
    logging.info("Attack ships %d" % len(attack_ships))
    logging.info("Enemy ships %d" % len(enemy_ships))
    game.send_command_queue(command_queue)
    # TURN END
# GAME END



