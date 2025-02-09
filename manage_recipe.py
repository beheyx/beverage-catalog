import zmq
import json

def load_beverages():
    with open("data.json", "r") as file:
        return json.load(file)

def save_beverages(beverage_list):
    with open("data.json", "w") as file:
        json.dump(beverage_list, file, indent=4)

def check_exist(beverage_list, name):
    for beverage in beverage_list:
        if beverage["name"].lower() == name.lower():
            return True 
    return False

#add a new recipe
def add_new_recipe(beverage_list, name, category, description, ingredients, instructions, favorite):
    #create new recipe and insert
    new_recipe = {
        "name": name,
        "category": category,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "favorite": favorite
    }

    beverage_list.append(new_recipe)
    save_beverages(beverage_list)
    return f"Recipe '{name}' has been successfully added!"

#delete a recipe
def delete_recipe(beverage_list, name):
    for beverage in beverage_list:
        if beverage["name"].lower() == name.lower():
            beverage_list.remove(beverage)
            save_beverages(beverage_list)
            return f"Recipe '{name}' has been deleted."

#add a recipe to favorites
def add_to_favorites(beverage_list, name):
    for beverage in beverage_list:
        if beverage["name"].lower() == name.lower():
            beverage["favorite"] = "*"  #mark as fav
            save_beverages(beverage_list)
            return f"Recipe '{name}' has been added to favorites!"

def recipe_main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5554")

    print("Manage Recipes Server running on port 5554...")

    while True:
        message = socket.recv_string()
        beverage_list = load_beverages()

        if message.startswith("check:"):  #exist if found or not found
            print(f"Received request: {message}, checking if beverage exists in catalog... ")
            name = message.split("check:", 1)[1].strip()
            response = "exists" if check_exist(beverage_list, name) else "not found"

        elif message.startswith("1:"):  #add new recipe
            try:
                recipe_data = message.split("1:", 1)[1] #discard the 1:
                name, category, decription, ingredients, instructions, favorite = recipe_data.split(";")
                ingredients = [i.strip() for i in ingredients.split(",")]
                instructions = [step.strip() for step in instructions.split(".")]

                response = add_new_recipe(beverage_list, name, category, decription, ingredients, instructions, favorite)
                print(f"Received request: {message}, adding new recipe... ")

            except ValueError:
                response = "Error: Invalid recipe format."

        elif message.startswith("2:"):  #delete recipe
            recipe_name = message[2:].strip()
            response = delete_recipe(beverage_list, recipe_name)
            print(f"Received request: {message}, deleting existing recipe.. ")


        elif message.startswith("3:"):  #add to favorites
            recipe_name = message[2:].strip()
            response = add_to_favorites(beverage_list, recipe_name)
            print(f"Received request: {message}, adding beverage into favorites... ")


        else:
            response = "Invalid option."

        socket.send_string(response)


recipe_main()