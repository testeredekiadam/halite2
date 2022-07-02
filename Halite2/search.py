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

    def defcap_planet_search(ship, game_map):
        defcap_list = {}
        for planet in game_map.all_planets():
            if planet.is_owned():
                continue
            dist = ship.calculate_distance_between(planet)
            docking_spot = planet.num_docking_spots
            index =  dist / (hlt.constants.MAX_SPEED * docking_spot)
            defcap_list.setdefault(index, []).append(planet)

        defcap_list = OrderedDict(sorted(defcap_list.items(), key=lambda t: t[0]))

        return defcap_list
