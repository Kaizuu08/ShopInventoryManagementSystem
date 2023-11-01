'''Shopping List Program'''

def read_inventory():
    '''Read inventory from a file, storing the inventory items in a list of dictionaries within a dictionary'''
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
    '''Customer buying function'''
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
    '''The checkout command and write to a new file'''
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


def main():
    '''The Main Program'''
    inventory = read_inventory()
    checkout = []

    #Asks the custoemr for a command
    while True:
        print('''Select from the following options:

            inventory - this will display what the shop has

            buy - this allows you to purchase items

            checkout - this will finish your purchases

            quit - this program will exit
            ''')
        customer = input("What would you like to do? ").lower()

        #inventory input - displays the current inventory
        if customer == "inventory":
            print("Current Inventory:")
            for item, details in inventory.items():
                print(f"Item: {item}")
                print(f"Price: {details['price']}")
                print(f"Aisle: {details['aisle']}")
                print(f"Inventory: {details['inventory']}")
                print("------------------------")

        #buy input - will buy the desired item in inventory
        elif customer == "buy":
            item = input("Enter the item you want to buy: \n").lower()
            aisle = input("Enter the aisle of the item: \n").lower()
            amount = int(input("Enter the quantity you want to buy: \n"))
            checkout_item = buy_inventory(item, aisle, amount, inventory)
            if checkout_item:
                checkout.append(checkout_item)

        #checkout input - will print receipt and finish
        elif customer == "checkout":
            write_checkout_to_file(checkout)
            break

        #breaks out of the program
        elif customer == "quit":
            print("Exiting the program.")
            break

main()