import zmq
import json

def load_beverages():
    with open("data.json", "r") as file:
        return json.load(file)

#save updated beverage data to json
def save_beverages(beverage_list):
    with open("data.json", "w") as file:
        json.dump(beverage_list, file, indent=4)

#check if beverage exists
def check_exist(beverage_list, name):
    for beverage in beverage_list:
        if beverage["name"].lower() == name.lower():
            return True 
    return False

#display fav beverage
def show_fav_beverage(beverage_list):
    favorite_beverage = [beverage for beverage in beverage_list if beverage.get("favorite") == "*"]

    result = ["\n-- View Favorite Beverages --"]

    if not favorite_beverage:
        return "No favorite beverages found."

    for beverage in favorite_beverage:
        result.append("\n-----------------------------\n"
                        f"Name: {beverage['name']} [*]\n"
                        f"Category: {beverage['category']}\n"
                        f"Description: {beverage['description']}")
    return "\n".join(result)

#display fav recipe
def show_fav_recipes(beverage_list):
    favorite_recipes = [beverage for beverage in beverage_list if beverage.get("favorite") == "*"]

    result = ["\n-- View Favorite Recipes --"]

    if not favorite_recipes:
        return "No favorite recipes found."

    for beverage in favorite_recipes:
        result.append("\n-----------------------------\n"
                        f"Name: {beverage['name']} [*]\n"
                        f"Ingredients: {", ".join(beverage["ingredients"])} \n"
                        f"Instructions:\n" + "\n".join([f"{i+1}. {step}" for i, step in enumerate(beverage.get("instructions", []))]))
    return "\n".join(result)

#remove a beverage from Favorites
def remove_favorite(beverage_list, name):
    for beverage in beverage_list:
        if beverage["name"].lower() == name.lower() and beverage.get("favorite") == "*":
            beverage["favorite"] = ""  #removed from favorites
            save_beverages(beverage_list)
            return f"\nRemoved {beverage['name']} from Favorites."
    
    return f"\nBeverage '{name}' is not found in favorites."


def fav_main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5552")

    print("Favorites Management Server running on port 5552...")

    while True:
        message = socket.recv_string()
        beverage_list = load_beverages()

        if message.startswith("check:"):  #exist if found or not found
            print(f"Received request: {message}, checking if beverage exists in catalog... ")
            name = message.split("check:", 1)[1].strip()
            response = "exists" if check_exist(beverage_list, name) else "not found"

        elif message == "1":  #view favorite beverage
            response = show_fav_beverage(beverage_list)
            print(f"Received request: {message}, printing favorite beverages... ")

        elif message == "2":  #view favorite recipes
            response = show_fav_recipes(beverage_list)
            print(f"Received request: {message}, printing beverage recipes... ")

        elif message.startswith("3:"):  #remove from Favorites
            name = message[2:] #remove the 3: 
            response = remove_favorite(beverage_list, name)  #passing the correct name
            print(f"Received request: {message}, trying to remove beverage name: '{name}'... ")

        else:
            response = "Invalid option."

        socket.send_string(response)

fav_main()