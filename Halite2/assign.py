class Assign:

    @staticmethod
    def assign_ship(ship, defcap_ships, attack_ships):
        saved_ships = defcap_ships + attack_ships
        if ship not in saved_ships:
            if len(defcap_ships)* 0.2 <= len(attack_ships):
                defcap_ships.append(ship)
            else:
                attack_ships.append(ship)




    @staticmethod
    def assign_planet(planet_array, target_planet):
        planet_array.append(target_planet)
