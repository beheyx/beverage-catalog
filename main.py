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
            drink_name = input("Enter the beverage name you wish to remove: ")
            confirm = input(f"Do you wish to remove '{drink_name}'? (Yes/No): ").lower()

            if confirm == "yes":
                socket.send_string(f"3:{drink_name}")  # Send remove request
                response = socket.recv_string()
                print(response)
            else:
                print("\nOperation canceled.")
        else:
            socket.send_string(sub_choice)  # Send user choice
            response = socket.recv_string()
            print(response)


def option_3(context): #search recipe
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5553")

    #socket.send_string("3")
    #insert the sub menu option

    response = socket.recv_string()
    print(response)

def option_4(context): #manage recipes
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5554")
    
    #socket.send_string("4") 
    #insert the sub menu option

    response = socket.recv_string()
    print(response)

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
