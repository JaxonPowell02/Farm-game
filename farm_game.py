import json
import os

# Define plant types with growth time and harvest value
plant_types = {
    "apple": {"growth_time": 3, "value": 10},
    "banana": {"growth_time": 2, "value": 8}
}

# Initial game state
game_state = {
    "money": 100,
    "seeds": {"apple": 5, "banana": 5},  # Corrected to include apple and banana seeds
    "crops": [],
    "day": 1
}

# Function to save the game state to a file
def save_game(state, filename="savegame.json"):
    with open(filename, "w") as file:
        json.dump(state, file)
    print("Game saved.")

# Function to load the game state from a file
def load_game(filename="savegame.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    else:
        print("No saved game found.")
        return None

# Function to plant a crop
def plant_crop(crop_type):
    print(f"Attempting to plant {crop_type}...")
    if game_state["seeds"].get(crop_type, 0) > 0:
        game_state["seeds"][crop_type] -= 1
        game_state["crops"].append({"type": crop_type, "planted_day": game_state["day"]})
        print(f"Planted a {crop_type}.")
    else:
        print(f"No {crop_type} seeds available.")

# Function to harvest crops
def harvest_crops():
    harvested = []
    for crop in game_state["crops"]:
        growth_time = plant_types[crop["type"]]["growth_time"]
        if game_state["day"] - crop["planted_day"] >= growth_time:
            value = plant_types[crop["type"]]["value"]
            game_state["money"] += value
            harvested.append(crop)
            print(f"Harvested {crop['type']} for ${value}.")
    # Remove harvested crops from the list
    game_state["crops"] = [crop for crop in game_state["crops"] if crop not in harvested]

# Main game loop
def game_loop():
    global game_state
    while True:
        print(f"Day {game_state['day']}")
        print(f"Money: ${game_state['money']}")
        print(f"Seeds: {game_state['seeds']}")
        print(f"Crops: {game_state['crops']}")
        action = input("What would you like to do? (plant/harvest/sell/save/quit): ").lower()

        if action == "plant":
            crop_type = input("Which crop would you like to plant? (apple/banana): ").lower()
            if crop_type in plant_types:
                plant_crop(crop_type)
            else:
                print("Invalid crop type.")
        elif action == "harvest":
            harvest_crops()
        elif action == "save":
            save_game(game_state)
        elif action == "quit":
            break
        else:
            print("Invalid action.")
        
        game_state["day"] += 1

if __name__ == "__main__":
    # Load game if exists
    loaded_game = load_game()
    if loaded_game:
        game_state = loaded_game
    
    game_loop()
