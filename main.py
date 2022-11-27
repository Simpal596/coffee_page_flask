from data import MENU, resources


def check_requirement(coffee_new, water_new, milk_new, type, money):
    if  MENU[type]["ingredients"]["water"] <= water_new and MENU[type]["ingredients"]["milk"] <= milk_new and MENU[type]["ingredients"]["coffee"] <= coffee_new and money >= MENU[type]["cost"] :
        return True
    else :
        return False


def calculate_money(quarter_no, dime_no, nickle_no, pennie_no):
    money = (quarter_no * 0.25) + (dime_no * 0.10) + (nickle_no * 0.05) + (pennie_no * 0.01)
    return money

def calculate_change(money_inserted, money_needed):
    return round((money_inserted - money_needed), 2)


def track_resource(coffee_new, water_new, milk_new) :
    resources["coffee"] = resources["coffee"] - coffee_new
    resources["milk"] = resources["milk"] - milk_new
    resources["water"] = resources["water"] - water_new


def coffee_machine():
    print("WELCOME TO COFFEE WORLD ☕")
    desire = input("What would you like ? (espresso/latte/cappuccino)").lower()
    if desire == "espresso" or desire == "latte" or desire == "cappuccino" :
        print("Please insert coins")
        quarters = float(input("How many quarters : "))
        dimes = float(input("How many dimes : "))
        nickles = float(input("How many nickles :"))
        pennies = float(input("How many pennies :"))
        money = calculate_money(quarters, dimes, nickles, pennies)
        check = check_requirement(resources["coffee"], resources["water"], resources["milk"], desire, money)
        if check is True :
            change = calculate_change(money, MENU[desire]["cost"])
            print(f"here is ${change} in change")
            print(f"here is your {desire} ☕. Enjoy 🙂")
            track_resource(MENU[desire]["ingredients"]["coffee"], MENU[desire]["ingredients"]["water"], MENU[desire]["ingredients"]["milk"])
        else :
            print("Sorry ! requirement can't be fulfilled ! money refunded.")
    elif desire == "report" :
        for item in resources:
            print(f"{item} : {resources[item]}")
    elif desire == "off" :
        return

coffee_machine()


