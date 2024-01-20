# Ashton Swanson
# Beauty Kabore
# Final Project
# PriceSmart comparison app
# DTSC 3020.501

# FUTURE FIXES

# ALLOW CARTS TO HAVE DIFFERENT ITEMS
# IMPORT INVENTORY AND COUPONS FROM INTERNET

def read_inventory(file_name):
    # CREATE DICTIONARY FOR INVENTORY
    inventory = {}
    # OPEN FILE
    with open(file_name, 'r') as file:
        # READ EACH LINE IN FILE
        for line in file:
            # SPLIT EACH LINE INTO ITEM AND PRICE STRING USING :
            item, price_str = map(str.strip, line.split(':'))
            # CONVERT PRICE STRING TO A FLOAT AND REMOVE $
            price = float(price_str.replace('$', ''))
            # SAVE PRICE IN INVENTORY DICTIONARY
            inventory[item.lower()] = price

    return inventory
def select_items(inventory):
    # CREATE AN EMPTY LIST
    selected_items = []
    # GET USER INPUT
    while True:
        item = input("Enter an item name to add it to your cart (or 'done' when complete): ").strip().lower()
        # BREAK IF USER ENTERS DONE
        if item == 'done':
            break
        # IF ITEM IS IN INVENTORY, ADD IT TO THE LIST
        elif item in inventory:
            selected_items.append(item)
            print(f"{item.capitalize()} added to your cart.")
        # IF ITEM IS NOT IN INVENTORY, DISPLAY ERROR MESSAGE
        else:
            print("Item not found. Please enter another item.")

    print("Selected items:", selected_items)  # Print selected items
    return selected_items


# FUNCTION TO SAVE SELECTED ITEMS ALONG WITH PRICES FROM INVENTORY
def save_selected_items(selected_items, inventory):
    # CREATE A DICTIONARY FOR SAVED ITEMS
    saved_items = {item.lower(): {'name': item, 'old_price': int(inventory.get(item.lower(), 0)), 'new_price': 999} for item in selected_items}
    return saved_items


def display_items(saved_items, nordstrom_list, macys_list, pennys_list):
    # CREATE AND PRINT HEADER
    print("\nItems in your cart:")
    #FORMAT THE HEADER FOR EASY READING
    header = "{:<20} {:<12} {:<12} {:<12}".format("Item", "Nordstrom", "Macy's", "JC Penny")
    print(header)

    # ITERATE THROUGH SAVED ITEMS LIST
    for item in saved_items:
        # TEST IF PRICE HAS CHANGED
        if nordstrom_list.get(item, {'new_price': 0})['new_price'] == 999:
            # PRINTS OLD PRICE IF PRICE IS UNCHANGED
            nordstrom_price = nordstrom_list.get(item, {'old_price': 0})['old_price']
        else:
            # PRINTS NEW PRICE IF PRICE IS CHANGED
            nordstrom_price = nordstrom_list.get(item, {'new_price': 0})['new_price']

        # TEST IF PRICE HAS CHANGED
        if macys_list.get(item, {'new_price': 0})['new_price'] == 999:
              # PRINTS OLD PRICE IF PRICE IS UNCHANGED
             macys_price = macys_list.get(item, {'old_price': 0})['old_price']
        else:
                # PRINTS NEW PRICE IF PRICE IS CHANGED
            macys_price = macys_list.get(item, {'new_price': 0})['new_price']

        # TEST IF PRICE HAS CHANGED
        if pennys_list.get(item, {'new_price': 0})['new_price'] == 999:
            # PRINTS OLD PRICE IF PRICE IS UNCHANGED
            pennys_price = pennys_list.get(item, {'old_price': 0})['old_price']
        else:
            # PRINTS NEW PRICE IF PRICE IS CHANGED
            pennys_price = pennys_list.get(item, {'new_price': 0})['new_price']

        # FORMAT EACH ROW FOR EASY READING
        row = "{:<20} ${:<11.2f} ${:<11.2f} ${:<11.2f}".format(item.capitalize(), nordstrom_price, macys_price, pennys_price)
        print(row)


def calculate_total_cost(saved_items):
    # ADDS UP THE TOTALS OF THE SELECTED ITEMS USING PRICE FROM EACH SAVED ITEMS LIST
    total_cost = 0
    for item in saved_items:
        # IF STATEMENT TO CHECK IF PRICE HAS CHANGED
        if saved_items.get(item, {'new_price': 0})['new_price'] == 999:
            # ADD OLD PRICE IF PRICE HASN'T CHANGED
            total_cost += saved_items.get(item, {'old_price': 0})['old_price']
        # ADD NEW PRICE IF IT HAS CHANGED
        else:
            total_cost += saved_items.get(item, {'new_price': 0})['new_price']
    return total_cost

def calculate_discount(old_total):
    # ASK USER IF THEY ARE CURRENTLY A REWARDS MEMBER
    member = input("Are you currently a member of the PriceSmart rewards program (Enter yes or no)?: ")
    # IF USER ANSWERS YES ADD 10% DISCOUNT
    if member.lower() == 'yes' or member.lower() == 'y':
        # ADD CURRENT MEMBER DISCOUNT OF 10%
        print("\nThank you for being a member!\nPriceSmart members are entitled to a 10% discount off of any purchase.\n")
        # CALCULATE DISCOUNT
        discount = old_total * 0.1
        # CALCULATE NEW TOTAL
        new_total = old_total - discount
        print(f"Your new total is ${new_total:.2f}.\nYou saved an additional ${discount:.2f} by being a PriceSmart member!\n")
    # IF USER ANSWERS NO GIVE THEM 20% DISCOUNT
    elif member.lower() == 'no' or member.lower() == 'n':
        # ADD NEW MEMBER DISCOUNT OF 20%
        print("Thank you for signing up for PriceSmart!\nNew members receive a 20% discount!\n")
        # CALCULATE DISCOUNT
        discount = old_total * 0.2
        # CALCULATE NEW TOTAL
        new_total = old_total - discount
        print(f"Your new total is ${new_total:.2f}.\nYou saved an additional ${discount:.2f} by signing up to be a PriceSmart member!\n")

def add_coupon(items_dict):
    # GET USER INPUT FOR COUPON
    coupon_type = input("Enter coupon type ('percentage', 'bogo', 'bogo50'): ").strip().lower()

    # IF STATEMENT DEPENDING ON COUPON TYPE
    if coupon_type == 'percentage':
        # GET PRECENTAGE OFF FROM USER
        percentage = int(input("Enter the percentage off (e.g., 10 for 10%): "))
        # ITERATE THROUGH DICTIONARY
        for item_name, item_details in items_dict.items():
            # SAVE NEW PRICE TO DICTIONARY
            item_details['new_price'] = item_details['old_price'] * (1 - percentage / 100)
            # CONFIRM ON SCREEN
            print(f"Coupon applied to {item_name}. New price: ${item_details['new_price']:.2f}")
    # BUY ONE GET ONE FREE
    elif coupon_type == 'bogo':
        # FIND LOWEST COST ITEM IN STORE DICTIONARY
        lowest_cost_item_name = min(items_dict, key=lambda x: items_dict[x]['old_price'])
        # ASSIGN NEW PRICE TO FREE
        items_dict[lowest_cost_item_name]['new_price'] = 0
        # CONFIRM ON SCREEN
        print(f"Coupon applied to {lowest_cost_item_name}. New price: ${items_dict[lowest_cost_item_name]['new_price']:.2f}")
    # BUY ONE GET OF 50% OFF
    elif coupon_type == 'bogo50':
        # FIND LOWEST COST ITEM IN STORE DICTIONARY
        lowest_cost_item_name = min(items_dict, key=lambda x: items_dict[x]['old_price'])
        # ASSIGN NEW PRICE TO HALF OFF
        items_dict[lowest_cost_item_name]['new_price'] = items_dict[lowest_cost_item_name]['old_price'] / 2
        # CONFIRM ON SCREEN
        print(f"Coupon applied to {lowest_cost_item_name}. New price: ${items_dict[lowest_cost_item_name]['new_price']:.2f}")
    else:
        print("Invalid coupon type. No coupon applied.")



def main():
    # READ AND SAVE EACH INVENTORY
    nordstrom_inventory = read_inventory('nordstrom.txt')
    macys_inventory = read_inventory('macys.txt')
    pennys_inventory = read_inventory('pennys.txt')

    # HAVE USER SELECT ITEMS
    print("Welcome to PriceSmart!")
    print("Your #1 discount finding app!")
    items = select_items(nordstrom_inventory)

    # SAVE ITEMS AND PRICES TO LIST
    nordstrom_list = save_selected_items(items, nordstrom_inventory)
    macys_list = save_selected_items(items, macys_inventory)
    pennys_list = save_selected_items(items, pennys_inventory)

    # PRINT ITEMS IN CART FOR EACH STORE
    display_items(items, nordstrom_list, macys_list, pennys_list)

    # CALCULATE TOTAL COST FROM EACH STORE
    nordstrom_total = calculate_total_cost(nordstrom_list)
    macys_total = calculate_total_cost(macys_list)
    pennys_total = calculate_total_cost(pennys_list)


    # DISPLAY TOTAL COSTS
    print("\nTotal cost from each store:")
    print("{:<12} {:<12} {:<12}".format("Nordstrom", "Macy's", "JC Penny"))
    print("${:<11.2f} ${:<11.2f} ${:<11.2f}".format(nordstrom_total, macys_total, pennys_total))

    # FIND LARGEST AND SMALLEST TOTAL
    largest = max(nordstrom_total, macys_total, pennys_total)
    smallest = min(nordstrom_total, macys_total, pennys_total)
    difference = largest - smallest

    # FIGURE OUT WHICH STORE HAS THE BEST DEAL
    best_deal = None
    if smallest == nordstrom_total:
        best_deal = "Nordstrom"
    elif smallest == macys_total:
        best_deal = "Macy's"
    elif smallest == pennys_total:
        best_deal = "JC Penny"

    # DISPLAY BEST DEAL
    print(f"The store with the best deal currently is: {best_deal}")

    # DISPLAY SAVINGS FROM USING APP
    print(
        f"\nThank you for allowing us to compare your totals!\nYou potentially saved up to ${difference:.2f} by putting your cart into PriceSmart!\n")

    # ASK USER IF THEY HAVE A COUPON
    have_coupon = input("Do you have any coupons? (enter yes or no):").strip().lower()

    if have_coupon.lower() == 'yes' or have_coupon.lower() == 'y':
        # WHILE LOOP TO PROMPT USER UNTIL THEY ENTER NO
        while have_coupon.lower() == 'yes' or have_coupon.lower() == 'y':
            # GET STORE NAME AND APPLY COUPON
            store = input("Which store do you have a coupon for?:").strip().lower()
            if store == 'nordstrom':
                add_coupon(nordstrom_list)
            elif store == 'macys' or store == "macy's":
                add_coupon(macys_list)
            elif store == 'jc penny' or store == 'jc pennys' or store == "jc penny's" or store == 'pennys' or store == "penny's":
                add_coupon(pennys_list)
            have_coupon = input("Do you have another coupon? (enter yes or no):").strip().lower()
            # PRINT AFTER COUPON TOTALS
        print("\n Here are your new store totals: ")
        display_items(items, nordstrom_list, macys_list, pennys_list)

        # CALCULATE NEW TOTALS
        new_nordstrom_total = calculate_total_cost(nordstrom_list)
        new_macys_total = calculate_total_cost(macys_list)
        new_pennys_total = calculate_total_cost(pennys_list)

        # DISPLAY NEW TOTAL COSTS
        print("\nNew total cost from each store:")
        print("{:<12} {:<12} {:<12}".format("Nordstrom", "Macy's", "JC Penny"))
        print("${:<11.2f} ${:<11.2f} ${:<11.2f}".format(new_nordstrom_total, new_macys_total, new_pennys_total))

        # CALCULATE COUPON SAVINGS
        nordstrom_savings = nordstrom_total - new_nordstrom_total
        macys_savings = macys_total - new_macys_total
        pennys_savings = pennys_total - new_pennys_total

        # PRINT COUPON SAVINGS
        print("Counpon savings by store:")
        print("${:<11.2f} ${:<11.2f} ${:<11.2f}".format(nordstrom_savings,macys_savings,pennys_savings))

        # FIGURE OUT WHICH STORE HAS THE BEST DEAL
        old_smallest = smallest
        smallest = min(new_nordstrom_total, new_macys_total, new_pennys_total)
        # CALCULATE COUPON SAVINGS
        difference = old_smallest - smallest

        best_deal = None
        if smallest == new_nordstrom_total:
           best_deal = "Nordstrom"
        elif smallest == new_macys_total:
            best_deal = "Macy's"
        elif smallest == new_pennys_total:
            best_deal = "JC Penny"

        # DISPLAY BEST DEAL
        print(f"The store with the best deal after applying coupons is: {best_deal}")
        print(f"You have potentially saved an additional ${difference:.2f} by appling coupons with PriceSmart.")

    # ASK USER IF THEY WOULD LIKE TO SIGN UP FOR OUR REWARDS PROGRAM
    loyalty = input("\nWould you like to save more by logging in or signing up for PriceSmart rewards? (enter yes or no):").strip().lower()

    # IF USER ANSWERS YES, RUN LOYALTY FUNCTION
    if loyalty.lower() == 'yes' or loyalty.lower() == 'y':
        # CALCULATE DISCOUNTS WITH PRICE SMART
        calculate_discount(smallest)
    # IF USER ANSWERS NO, TELL THEM HOW MUCH ADDITIONAL MONEY THEY COULD BE SAVING
    elif loyalty.lower() == 'no' or loyalty.lower() == 'n':
        # CALCULATE POTENTIAL SAVINGS
        savings = smallest * 0.2
        print(f"\nWhat a shame. PriceSmart users save 20% off their first purchase, so you could have saved an additional ${savings:.2f}.\n")

if __name__ == "__main__":
    main()

