import math
import random

class DeepSeaMegalodon:
    def __init__(self, name, length_m, mass_kg):
        self.name = name
        self.length = length_m
        self.mass = mass_kg
        
        # --- FIX: REALISTIC LIVER ENERGY RESERVES ---
        # Liver is approx 25% of body mass
        liver_mass = mass_kg * 0.25
        # 9000 kcal per kg of lipid. Assume 50% of liver is usable oil.
        self.max_energy = liver_mass * 0.5 * 9000
        
        # Start with 50% reserves (hungry but healthy)
        self.current_energy_kcal = self.max_energy * 0.5 
        
        self.is_alive = True
        
        # Deep Sea Physics Constants
        self.water_density = 1027 
        self.drag_coefficient = 0.04 
        self.frontal_area = math.pi * ((length_m / 6) ** 2)

    def calculate_bmr(self):
        """
        Calculates Basal Metabolic Rate (BMR) - Energy burned just existing.
        Using modified Kleiber's Law for Ectothermic (cold-blooded) Gigantotherms.
        """
        k = 0.5 
        # The "Sleeper Adaptation": Deep sea animals have VERY slow metabolisms.
        # We assume it burns 80% less energy than a surface Great White.
        sleeper_factor = 0.2 
        
        # Kleiber's Law: BMR proportional to Mass^0.75
        hourly_burn_kcal = k * (self.mass ** 0.75) * sleeper_factor
        return hourly_burn_kcal

    def swim(self, hours, speed_mps):
        """
        Calculates energy lost due to swimming (Hydrodynamic Drag).
        Force = 0.5 * density * velocity^2 * drag_coeff * area
        Energy (Joules) = Force * Distance
        """
        distance_m = speed_mps * (hours * 3600)
        
        # Drag Force Equation
        drag_force = 0.5 * self.water_density * (speed_mps ** 2) * self.drag_coefficient * self.frontal_area
        
        # Work Done (Joules)
        energy_joules = drag_force * distance_m
        
        # Convert Joules to kcal (1 kcal = 4184 Joules)
        energy_kcal = energy_joules / 4184
        
        return energy_kcal

    def scavenge(self):
        """
        Simulates the chance of finding a 'Whale Fall' (Dead whale on sea floor).
        Point Nemo is sparse. We assume a 1% chance (0.01) per day of finding a major food source.
        """
        # 1% chance to find food per day
        if random.random() < 0.01: 
            # JACKPOT! A small whale carcass.
            # 100 kg of blubber * 7000 kcal/kg = 700,000 kcal
            calories_gained = 700000 
            self.current_energy_kcal += calories_gained
            return f"*** JACKPOT! FOUND A WHALE FALL! (+{calories_gained} kcal) ***"
        else:
            return "Scanned sector... nothing found."

    def live_one_day(self, swim_speed_mps=1.0):
        """
        Simulates 24 hours of life.
        INCLUDES ADAPTIVE BEHAVIOR (Low Power Mode)
        """
        if not self.is_alive:
            return f"{self.name} is dead."

        # --- BEHAVIOR UPDATE: LOW POWER MODE ---
        # If energy drops below 10%, slow down to drift speed to survive
        actual_speed = swim_speed_mps
        if self.current_energy_kcal < (self.max_energy * 0.1):
            actual_speed = 0.2 # Drift mode (barely moving)
            mode = "LOW POWER MODE"
        else:
            mode = "Patrolling"

        # 1. Burn BMR
        bmr_cost = self.calculate_bmr() * 24
        
        # 2. Burn Swim Energy
        swim_cost = self.swim(24, actual_speed)
        
        total_loss = bmr_cost + swim_cost
        self.current_energy_kcal -= total_loss
        
        # Format numbers for readability (Divide by 1000 to show 'k')
        status = f"[{mode}] Burned {int(total_loss)} kcal. Reserves: {int(self.current_energy_kcal/1000)}k / {int(self.max_energy/1000)}k"
        
        if self.current_energy_kcal <= 0:
            self.is_alive = False
            status += " -> STARVED TO DEATH."
            
        return status

# --- RUN THE 1-YEAR SURVIVAL TEST ---

meg = DeepSeaMegalodon("Subject Zero", length_m=12, mass_kg=15000)
days_survived = 0

print(f"--- STARTING 365 DAY SURVIVAL TEST FOR {meg.name} ---")
print(f"Stats: {meg.length}m | {meg.mass}kg | Start Energy: {meg.current_energy_kcal} kcal")
print("-" * 50)

for day in range(1, 366):
    if not meg.is_alive:
        break
    
    # 1. Try to find food (The Lottery)
    hunt_result = meg.scavenge()
    
    # 2. Burn energy to live
    # Swimming at 1.0 m/s (approx 3.6 km/h) to cover ground
    status_log = meg.live_one_day(swim_speed_mps=1.0) 
    
    # Only print critical events (Food found or Death) to keep console readable
    if "JACKPOT" in hunt_result or not meg.is_alive:
        print(f"Day {day}: {hunt_result}")
        print(f"       {status_log}")
    
    days_survived += 1

print("-" * 50)
if meg.is_alive:
    print(f"RESULT: SUCCESS. Creature survived the year with {int(meg.current_energy_kcal)} kcal remaining.")
else:
    print(f"RESULT: FAILED. Creature starved after {days_survived} days.")