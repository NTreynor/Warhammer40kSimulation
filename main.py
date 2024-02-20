import random

class Model:
    def __init__(self, name, movement, toughness, save_characteristic, wounds, leadership, objective_control, ranged_weapons=None, close_combat_weapons=None):
        self.name = name
        self.movement = movement
        self.toughness = toughness
        self.save_characteristic = save_characteristic
        self.wounds = wounds
        self.leadership = leadership
        self.objective_control = objective_control
        self.ranged_weapons = ranged_weapons or []
        self.close_combat_weapons = close_combat_weapons or []

    def add_ranged_weapon(self, weapon):
        self.ranged_weapons.append(weapon)

    def add_close_combat_weapon(self, weapon):
        self.close_combat_weapons.append(weapon)

    def simulate_ranged_attack(self, weapon, target_model):
        if weapon not in self.ranged_weapons:
            return f"{self.name} does not have the {weapon.name}."

        hits = 0
        wounds = 0
        failed_saves = 0
        total_damage = 0

        for _ in range(weapon.num_attacks):
            # Hit Roll
            if weapon.hit_roll():
                hits += 1

                # Wound Roll
                if weapon.wound_roll(target_model.toughness):
                    wounds += 1

                    # Save Roll modified by armor penetration
                    modified_save_characteristic = max(target_model.save_characteristic + weapon.armor_penetration, 2)
                    if not weapon.save_roll(modified_save_characteristic):
                        failed_saves += 1
                        total_damage += weapon.damage

        result = f"{weapon.num_attacks} {weapon.name} attacks: {hits} hits, {wounds} wounds, {failed_saves} failed saves, {total_damage} damage inflicted"
        return result

class Weapon:
    def __init__(self, name, ballistic_skill, num_attacks, strength, armor_penetration, damage):
        self.name = name
        self.ballistic_skill = ballistic_skill
        self.num_attacks = num_attacks
        self.strength = strength
        self.armor_penetration = armor_penetration
        self.damage = damage

    def hit_roll(self):
        return random.randint(1, 6) >= self.ballistic_skill

    def wound_roll(self, toughness):
        ratio = toughness / self.strength

        if ratio > 2:
            required_roll = 6
        elif 2 >= ratio > 1:
            required_roll = 5
        elif ratio == 1:
            required_roll = 4
        elif 1 > ratio > 0.5:
            required_roll = 3
        else:
            required_roll = 2

        return random.randint(1, 6) >= required_roll

    def save_roll(self, save_characteristic):
        return random.randint(1, 6) >= save_characteristic

# Create a Bolter weapon instance
bolter = Weapon(name="Bolter", ballistic_skill=3, num_attacks=2, strength=4, armor_penetration=0, damage=1)

# Create a Tactical Marine model instance
tactical_marine = Model(name="Tactical Marine", movement=6, toughness=4, save_characteristic=3, wounds=2, leadership=6, objective_control=2)
tactical_marine.add_ranged_weapon(bolter)

# Example Usage
result = tactical_marine.simulate_ranged_attack(weapon=bolter, target_model=tactical_marine)
print(result)