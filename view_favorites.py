import zmq
import json

def load_beverages():
    with open("data.json", "r") as file:
        return json.load(file)

#save updated beverage data to json
def save_beverages(beverages):
    with open("data.json", "w") as file:
        json.dump(beverages, file, indent=4)

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
        beverages = load_beverages()

        if message == "1":  #view favorite beverage
            response = show_fav_beverage(beverages)
            print(f"Received request: {message}, printing favorite beverages... ")

        elif message == "2":  #view favorite recipes
            response = show_fav_recipes(beverages)
            print(f"Received request: {message}, printing beverage recipes... ")

        elif message.startswith("3:"):  #remove from Favorites
            name = message[2:]
            response = remove_favorite(beverages, name)  #passing the correct name
            print(f"Received request: {message}, trying to remove beverage name: '{name}'... ")

        else:
            response = "Invalid option."

        socket.send_string(response)

fav_main()