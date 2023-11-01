import tkinter as tk

def read_inventory():
    items = {}
    with open("inventory.txt", "r") as file:
        for line in file:
            item_name, price, aisle, inventory = line.split(",")
            items[item_name] = {
                'price': float(price),
                'aisle': str(aisle.strip()),
                'inventory': int(inventory)
            }
    return items

def buy_inventory(item, aisle, amount, inventory):
    checkout = {}
    if item in inventory:
        if inventory[item]['aisle'] == aisle and inventory[item]['inventory'] >= amount:
            checkout = {
                'item': item,
                'price': float(inventory[item]['price']),
                'aisle': aisle,
                'amount': amount,
                'subtotal': float(inventory[item]['price'] * amount)
            }
            inventory[item]['inventory'] -= amount
            print(f"Successfully placed an order for {amount} {item} costing {checkout['subtotal']}")
            return checkout
        elif inventory[item]['inventory'] < amount:
            print(f"We only have {inventory[item]['inventory']} {item} available. You can't purchase {amount}.")
        else:
            print(f"Item {item} is currently out of stock.")
    else:
        print("Item does not exist in the inventory.")

def write_checkout_to_file(checkout):
    totalling = 0
    with open("receipt.txt", "w") as file:
        for item in checkout:
            file.write(f"Item: {item['item']}\n")
            file.write(f"Price: {item['price']}\n")
            file.write(f"Aisle: {item['aisle']}\n")
            file.write(f"Amount: {item['amount']}\n")
            file.write(f"Subtotal: {item['subtotal']:.2f}\n") 
            file.write("-------------------------\n")
            totalling += item['subtotal']
        file.write(f"Total Owing: ${totalling:.2f}") 
    print("Checkout information written to receipt.txt.")

def handle_inventory():
    inventory = read_inventory()
    print("Current Inventory:")
    for item, details in inventory.items():
        print(f"Item: {item}")
        print(f"Price: {details['price']}")
        print(f"Aisle: {details['aisle']}")
        print(f"Inventory: {details['inventory']}")
        print("------------------------")

def handle_buy():
    item = input("Enter the item you want to buy: \n").lower()
    aisle = input("Enter the aisle of the item: \n").lower()
    amount = int(input("Enter the quantity you want to buy: \n"))
    checkout_item = buy_inventory(item, aisle, amount, inventory)
    if checkout_item:
        checkout.append(checkout_item)

def handle_checkout():
    write_checkout_to_file(checkout)
    window.destroy()

def handle_quit():
    print("Exiting the program.")
    window.destroy()

# Create the main window
window = tk.Tk()

# Load the inventory
inventory = read_inventory()

# Create the buttons
inventory_button = tk.Button(window, text="Inventory", command=handle_inventory)
buy_button = tk.Button(window, text="Buy", command=handle_buy)
checkout_button = tk.Button(window, text="Checkout", command=handle_checkout)
quit_button = tk.Button(window, text="Quit", command=handle_quit)

# Add the buttons to the window
inventory_button.pack()
buy_button.pack()
checkout_button.pack()
quit_button.pack()

# Create the checkout list
checkout = []

# Start the main loop
window.mainloop()
