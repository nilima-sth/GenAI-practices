import json
import datetime

INVENTORY_FILE = 'D:\GenAI\Day1-project\database.json'
# Load inventory data
with open(INVENTORY_FILE, 'r') as f:
    database = json.load(f)

def show_items():
    """Show available categories and items inside selected category."""
    print("\nCategories are:")
    for category in database:
        print(f"- {category}")

    # check for valid category
    while True:
        category = input("Select a Category: ").strip()
        if category not in database:
            print(f"Error: Category '{category}' not found. Please try again.")
            continue
        break

    print(f"\nAvailable items in {category}:")
    for item, details in database[category].items():
        print(f"{item} - Quantity: {details['quantity']}, Price: ${details['price']}")
    return category

def select_items(category):
    """Select item and purchase quantity from the chosen category."""
    while True:
        item = input("\nEnter the item you want to select: ").strip()
        if item not in database[category]:
            print(f"Error: Item '{item}' not found in category '{category}'.")
            continue
        break

    while True:
        try:
            qty = int(input("How many do you want to purchase? : "))
            if qty <= 0:
                print("Quantity must be greater than zero.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    return item, qty

def purchase_item(user, category, item, qty):
    """Purchase item if available and log the purchase."""
    if database[category][item]['quantity'] < qty:
        print(f"Error: Only {database[category][item]['quantity']} {item} left in stock.")
        return False

    database[category][item]['quantity'] -= qty
    print(f"\n✅ Purchased {qty} {item}(s) from {category}. Remaining stock: {database[category][item]['quantity']}")

    # save updated database
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(database, f, indent=4)

    # log purchase
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('log.txt', 'a') as log_file:
        log_file.write(f"User: {user} purchased {qty} {item}(s) from {category} at {time}\n")

    return True

def main():
    print("-----------------INVENTORY MANAGEMENT SYSTEM------------------")
    user = input("Enter your name: ")
    print(f"Hi {user}! Welcome to Inventory Management System.")

    category = show_items()
    item, qty = select_items(category)

    if purchase_item(user, category, item, qty):
        print(f"\nThank you for your purchase, {user}!")

if __name__ == "__main__":
    main()