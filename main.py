import zmq

def display_main_menu():
    print("\n--------------------------------------------------------------------")
    print("Menu Options")
    print("1) View All Beverages")
    print("2) View Favorites")
    print("3) Search Recipes")
    print("4) Manage Recipes")
    print("5) Exit my PourFolio")


def option_1(context): #view all beverages
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5551")
    socket.send_string("1")  #send request first
    response = socket.recv_string()
    print(response)


def option_2(context): #view favorites
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5552")

    while True:
        print("\n--------------------------------------------------------------------")
        print("| Favorites |")
        print("- A place to manage your favorite beverages, add beverage to favorite feature can be found in 'Manage Recipes' -")
        print("\nWhat would you like to do?")
        print("1) View Favorite Beverages")
        print("2) View Favorite Recipes")
        print("3) Remove Beverage from Favorites")
        print("4) Go Back to Main Menu")
        
        sub_choice = input("\nEnter a choice from 1 to 4: ")

        if sub_choice == "4":
            print("\nReturning to Main Menu...")
            break

        if sub_choice == "3":
            beverage_name = input("Enter the recipe name you wish to remove: ").strip()
            socket.send_string(f"check:{beverage_name}")
            response = socket.recv_string()

            if response == "not found":
                print(f"\nERROR: Failed to remove '{beverage_name}' because it does not exist! Try again.")
                continue  #go back to menu

            print("\nWARNING: If you removed this beverage from Favorites, then you would have to re-add it from 'Manage Recipe'!!! \n")
            confirm = input(f"Do you wish to remove '{beverage_name}'? (Yes/No): ").strip().lower()

            if confirm == "yes":
                socket.send_string(f"3:{beverage_name}")  #send remove request with name
                response = socket.recv_string()
                print(response)
            else:
                print("\nOperation canceled.")
        else:
            socket.send_string(sub_choice)  #send user choice
            response = socket.recv_string()
            print(response)


def option_3(context): #search recipe
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5553")

    while True:
        print("\n--------------------------------------------------------------------")
        print("| Search and Filter |")
        print("- A place to search speicific recipe and filter beverages -")
        print("\nWhat would you like to do?")
        print("1) Search Recipe by Name")
        print("2) Filter Beverages by Type")
        print("3) Filter Beverages by Ingredient")
        
        print("4) Go Back to Main Menu")
        
        sub_choice = input("\nEnter a choice from 1 to 4: ")

        if sub_choice == "4":
            print("\nReturning to Main Menu...")
            break
        
        if sub_choice == "1":
            #ask user for name, then send req to check if name exist
            #receive res, if not found, then err
            #if found, keep processing
            recipe_name = input("Enter the recipe name you are looking for: ").strip()
            socket.send_string(f"check:{recipe_name}")
            response = socket.recv_string()

            if response == "not found":
                print(f"\nERROR: Failed to look up '{recipe_name}' because it does not exist! Try again.")
                continue  #go back to menu

            socket.send_string(f"1:{recipe_name}")  #send remove request with name
            response = socket.recv_string()
            print(response) #recived and print response

        elif sub_choice == "2":
            beverage_type = input("Enter the type of beverages you are looking for: ").strip()
            socket.send_string(f"check:{beverage_type}")
            response = socket.recv_string()

            if response == "not found":
                print(f"\nERROR: Cannot find beverages with the cateogry of {beverage_type}! Try again.")
                continue  #go back to menu
            
            socket.send_string(f"2:{beverage_type}")  #send remove request with type
            response = socket.recv_string()
            print(response) #recived and print response

        elif sub_choice == "3":
            beverage_ingr = input("Enter an ingredient you are looking for in beverages: ").strip()
            socket.send_string(f"check:{beverage_ingr}")
            response = socket.recv_string()

            if response == "not found":
                print(f"\nERROR: Cannot find beverages with the ingredient of {beverage_type}! Try again.")
                continue  #go back to menu
            
            socket.send_string(f"3:{beverage_ingr}")  #send remove request with type
            response = socket.recv_string()
            print(response) #recived and print response


def option_4(context): #manage recipes
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5554")
    
    while True:
        print("\n--------------------------------------------------------------------")
        print("| Mangage Recipes |")
        print("- A place to add and delete recipes -")
        print("\nWhat would you like to do?")
        print("1) Add New Recipe")
        print("2) Delete Existing Recipe")
        print("3) Add Existing Recipe to Favorites")
        print("4) Go Back to Main Menu")
        
        sub_choice = input("\nEnter a choice from 1 to 4: ")

        if sub_choice == "4":
            print("\nReturning to Main Menu...")
            break
        
        if sub_choice == "1":
            #first check if name already exist
            new_name = input("Enter the name of the new beverage: ").strip()
            socket.send_string(f"check:{new_name}")
            response = socket.recv_string()

            if response == "exists":
                print(f"\nERROR: The recipe of '{new_name}' already exists! Try adding a different recipe.")
                continue  #go back to menu

            category = input("Enter the cateogry in which the new beverage belongs to (Coffee, Tea, etc.): ").strip()
            description = input("Enter a description for the new beverage: ").strip()
            ingredients = input("Enter ingredients (separate using comma): ").strip().split(",")

            instructions = []
            print("Enter instructions step by step, type 'done' when finished.")
            while True:
                step = input(f"Step {len(instructions) + 1}: ").strip() #so step 1, step 2, ... inc based on instruction
                if step.lower() == "done": #if done is entered
                    break
                instructions.append(step) #otherwise keep appending steps
            
            add_to_fav = input(f"Do you want to add this new recipe '{new_name}' to favorite? (Yes/No): ").strip().lower()
            if add_to_fav == "yes":
                favorite = "*"
            else:
                favorite = ""
            socket.send_string(f"1:{new_name};{category};{description};{','.join(ingredients)};{'.'.join(instructions)};{favorite}")
            
            response = socket.recv_string()
            print(response) #recived and print response

        elif sub_choice == "2":
            beverage_name = input("Enter the recipe name you wish to delete: ").strip()
            socket.send_string(f"check:{beverage_name}")
            response = socket.recv_string()

            if response == "not found":
                print(f"\ERROR: Failed to delete '{beverage_name}' because it does not exist! Try again.")
                continue  #go back to menu

            print("\nWARNING: If you DELETE this recipe, then it will be GONE from the catalog!!! \n")
            confirm = input(f"Do you wish to DELETE '{beverage_name}'? (Yes/No): ").strip().lower()

            if confirm == "yes":
                socket.send_string(f"2:{beverage_name}")  #send remove request with name
                response = socket.recv_string()
                print(response)
            else:
                print("\nOperation canceled.")

        elif sub_choice == "3":
            beverage_name = input("Enter the beverage name you wish to add to Favorites: ").strip()
            socket.send_string(f"check:{beverage_name}")
            response = socket.recv_string()

            if response == "not found":
                print(f"\nERROR: Failed to add '{beverage_name}' to Favorites because it does not exist! Try again.")
                continue  #go back to menu
            
            socket.send_string(f"3:{beverage_name}")  #send remove request with type
            response = socket.recv_string()
            print(response) #recived and print response


def main():
    context = zmq.Context()
    print("\n********************************************************************")
    print("|| PourFolio ||")
    print("\n-- 'A comprehensive beverage management tool designed to explore, manage, and share recipes' --")

    while True:
        display_main_menu()
        user_choice = input("\nEnter a choice from 1 to 5: ")
        
        if user_choice == "1":
            option_1(context)

        elif user_choice == "2":
            option_2(context)

        elif user_choice == "3":
            option_3(context)

        elif user_choice == "4":
            option_4(context)

        elif user_choice == "5":
            print("Exiting PourFolio. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
            continue

main()
