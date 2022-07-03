# Firat Erkol – 219204648
# Finn Doose-Bruns - 220200432
# Fiona Stürzekarn – 220200224
# Iana Mazur - 219204806
# Tobias Edrich - 218201941

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