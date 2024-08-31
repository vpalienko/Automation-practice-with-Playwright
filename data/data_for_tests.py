from random import choice

coffee_list = [("Espresso", "$10.00"),
               ("Espresso Macchiato", "$12.00"),
               ("Cappuccino", "$19.00"),
               ("Mocha", "$8.00"),
               ("Flat White", "$18.00"),
               ("Americano", "$7.00"),
               ("Cafe Latte", "$16.00"),
               ("Espresso Con Panna", "$14.00"),
               ("Cafe Breve", "$15.00")]

coffee_translations = [("Espresso", "特浓咖啡"),
                       ("Espresso Macchiato", "浓缩玛奇朵"),
                       ("Cappuccino", "卡布奇诺"),
                       ("Mocha", "摩卡"),
                       ("Flat White", "平白咖啡"),
                       ("Americano", "美式咖啡"),
                       ("Cafe Latte", "拿铁"),
                       ("Espresso Con Panna", "浓缩康宝蓝"),
                       ("Cafe Breve", "半拿铁")]

coffee_names = ["Espresso",
                "Espresso Macchiato",
                "Cappuccino",
                "Mocha",
                "Flat White",
                "Americano",
                "Cafe Latte",
                "Espresso Con Panna",
                "Cafe Breve"]

number_of_available_coffee = len(coffee_names)


def get_random_coffee_type():
    return choice(coffee_names)