# nearby_empty_planets = [nearby_entities[distance][0] for distance in nearby_entities
#                                 if
#                                 isinstance(nearby_entities[distance][0], hlt.entity.Planet)
#                                 and not nearby_entities[distance][0].is_owned()]
#
# nearby_entities = OrderedDict(sorted(nearby_entities.items(), key=lambda t: t[0]))
import hlt
import logging
from collections import OrderedDict


class Search:

    @staticmethod
    def defcap_planet_search(ship, game_map):
        defcap_list = {}
        for planet in game_map.all_planets():
            if planet.is_owned():
                continue
            dist = ship.calculate_distance_between(planet)
            docking_spot = planet.num_docking_spots
            index = (dist * docking_spot) / hlt.constants.MAX_SPEED
            defcap_list.setdefault(index, []).append(planet)

        defcap_list = OrderedDict(sorted(defcap_list.items(), key=lambda t: t[0]))

        return defcap_list

    @staticmethod
    def attack_ship_search(ship, game_map):
        attack_list = {}
        for planet in game_map.all_planets():
            if planet.is_owned() and planet.owner != ship.owner:
                dist = ship.calculate_distance_between(planet)
                index = dist / (hlt.constants.MAX_SPEED * len(planet.all_docked_ships()))
                attack_list.setdefault(index, []).append(planet)

            else:
                continue

        attack_list = OrderedDict(sorted(attack_list.items(), key=lambda t: t[0]))

        return attack_list

    @staticmethod
    def minimax(ship, nearby_empty_planets):
        for planet in nearby_empty_planets:
            pass
