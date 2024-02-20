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
        self.is_damaged = False

    def add_ranged_weapon(self, weapon):
        self.ranged_weapons.append(weapon)

    def add_close_combat_weapon(self, weapon):
        self.close_combat_weapons.append(weapon)

    def simulate_ranged_attack(self, weapon, target_model):
        if weapon not in self.ranged_weapons:
            return f"{self.name} does not have the {weapon.name}."

        hits = 0
        successful_wounds = 0
        wound_details = []

        for _ in range(weapon.num_attacks):
            # Hit Roll
            if weapon.hit_roll():
                hits += 1

                # Wound Roll
                if weapon.wound_roll(target_model.toughness):
                    successful_wounds += 1
                    wound_details.append({"damage": weapon.damage, "armor_penetration": weapon.armor_penetration})

        result = {
            "hits": hits,
            "successful_wounds": successful_wounds,
            "wound_details": wound_details
        }
        return result

    def save_roll(self, save_characteristic):
        return random.randint(1, 6) >= save_characteristic

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

class Unit:
    def __init__(self, name, models=None):
        self.name = name
        self.models = models or []

    def add_model(self, model):
        self.models.append(model)

    def squad_engagement(self, enemy_unit):
        results = []

        for attacker in self.models:
            for weapon in attacker.ranged_weapons:
                for target in enemy_unit.models:
                    result = attacker.simulate_ranged_attack(weapon, target)
                    results.append(result)

        return results

    def allocate_saves(self, damage_info):
        damaged_models = [model for model in self.models if model.is_damaged]

        if damaged_models:
            target_model = random.choice(damaged_models)
        else:
            #target_model = random.choice(self.models)
            target_model = self.models.pop()

        for wound_detail in damage_info["wound_details"]:
            modified_save_characteristic = max(target_model.save_characteristic + wound_detail["armor_penetration"], 2)
            if not target_model.save_roll(modified_save_characteristic):
                target_model.wounds -= wound_detail["damage"]

                if target_model.wounds <= 0:
                    self.models.remove(target_model)

# Create a Bolter weapon instance
bolter = Weapon(name="Bolter", ballistic_skill=3, num_attacks=2, strength=4, armor_penetration=0, damage=1)

# Create Tactical Marine model instance
tactical_marine = Model(name="Tactical Marine", movement=6, toughness=4, save_characteristic=3, wounds=2, leadership=6, objective_control=2)
tactical_marine.add_ranged_weapon(bolter)

# Create Tactical Marine Squad unit consisting of 10 Tactical Marines
tactical_marine_squad = Unit(name="Tactical Marine Squad")
for _ in range(10):
    tactical_marine_squad.add_model(tactical_marine)

# Create another Tactical Marine Squad unit consisting of 10 Tactical Marines
enemy_tactical_marine_squad = Unit(name="Enemy Tactical Marine Squad")
for _ in range(10):
    enemy_tactical_marine_squad.add_model(tactical_marine)

# Example Usage
results = tactical_marine_squad.squad_engagement(enemy_tactical_marine_squad)

for result in results:
    tactical_marine_squad.allocate_saves(result)