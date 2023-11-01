import unittest
import os
import program


class Test(unittest.TestCase):

    def test_read_inventory(self):
        expected_result = {}
        with open("inventory.txt", "r") as file:
            for line in file:
                item_name, price, aisle, inventory = line.split(",")
                expected_result[item_name] = {
                    'price': float(price),
                    'aisle': str(aisle.strip()),
                    'inventory': int(inventory)
                }

        result = program.read_inventory()

        #checks for whitespaces in aisle
        for item_name, item in result.items():
            self.assertFalse(' ' in item['aisle'], f"Whitespace found in aisle for item '{item_name}': {item['aisle']}")

        #checks if the read_inventory() is equal to the inventory
        self.assertEqual(result, expected_result, msg = "Inventory does not match the text file")

    def test_buy_inventory(self):
        inventory = program.read_inventory()  # Read inventory from file

        item = 'apples'
        aisle = 'produce'
        amount = 10

        checkout = []

        # Test buying an available item
        checkout_item = program.buy_inventory(item, aisle, amount, inventory)
        self.assertIsInstance(checkout_item, dict)
        self.assertEqual(checkout_item['item'], item, msg= "Incorrect Item in checkout ")
        self.assertEqual(checkout_item['aisle'], aisle, msg="Incorrect aisle in checkout")
        self.assertEqual(checkout_item['amount'], amount, msg="Incorrect amount in checkout")
        self.assertEqual(inventory[item]['inventory'], 40, msg="Inventory was not updated correctly")
        checkout.append(checkout_item)

        # Test buying an item with insufficient inventory
        amount = 100
        checkout_item = program.buy_inventory(item, aisle, amount, inventory)
        self.assertIsNone(checkout_item, msg="checkout_item is not None even with insufficient inventory")

        # Test buying an item not in the inventory
        item = 'banana'
        checkout_item = program.buy_inventory(item, aisle, amount, inventory)
        self.assertIsNone(checkout_item, msg="checkout_item is not None even with item not in inventory")

        # Check if inventory and checkout are updated correctly
        self.assertEqual(inventory['apples']['inventory'], 40, msg="Inventory was not updated correctly")
        self.assertEqual(len(checkout), 1, msg="Incorrect number of items in checkout")
        self.assertEqual(checkout[0]['item'], 'apples', msg="Incorrect item in checkout")

    def test_write_checkout_to_file(self):
        checkout = [
            {'item': 'apples', 'price': 0.99, 'aisle': 'produce', 'amount': 10, 'subtotal': 9.9},
            {'item': 'bananas', 'price': 0.49, 'aisle': 'produce', 'amount': 5, 'subtotal': 2.45}
        ]

        expected_contents = """Item: apples
        Price: 0.99
        Aisle: produce
        Amount: 10
        Subtotal: 9.90
        -------------------------
        Item: bananas
        Price: 0.49
        Aisle: produce
        Amount: 5
        Subtotal: 2.45
        -------------------------
        Total Owing: $12.35"""

        # Test writing checkout information to file
        program.write_checkout_to_file(checkout)

        # Assert that the receipt.txt file exists
        self.assertTrue(os.path.exists('receipt.txt'))

        # Read the contents of the receipt.txt file
        with open('receipt.txt', 'r') as file:
            contents = file.readlines()

        # Split the expected contents into lines
        expected_lines = expected_contents.strip().split('\n')

        # Remove leading and trailing whitespace from each line
        expected_lines = [line.strip() for line in expected_lines]

        # Compare the contents line by line
        for i, line in enumerate(expected_lines):
            self.assertEqual(line, contents[i].strip())


        


if __name__ == '__main__':
    unittest.main()
