import zmq
import json

#read the json file
def load_beverages():
    with open("data.json", "r") as file:
        return json.load(file)
    
#store everything
def show_beverages(beverage_list):
    result = ["\n-- All Beverages -- "]
    result.append("\nBeverages with '*' are marked as Favorites")

    for beverage in beverage_list:
        name = beverage["name"]
        fav = "[*]" if beverage.get("favorite") == "*" else ""
        category = beverage["category"]
        description = beverage["description"]

        result.append("\n-----------------------------\n"
                        f"Name: {name} {fav}\n"
                        f"Category: {category}\n"
                        f"Description: {description}")    
        
    return "\n".join(result)
    
def beverage_main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5551") 

    print("View All Beverages Server is running and listening...")

    while True:
        message = socket.recv_string()
        print(f"Received request: {message}, printing all beverages... ")

        beverage_list = load_beverages()
        response = show_beverages(beverage_list)

        socket.send_string(response) #send the beverage list back to main

beverage_main()
