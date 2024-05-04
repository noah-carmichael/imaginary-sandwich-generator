import random

vegetables = ["lettuce", "tomatoes", "red onions", "cucumber", "peppers", "pickels"]
cheese = ["cheddar", "marble", "blue cheese", "fetta"]
meat = ["ham", "bologna", "turkey", "bacon", "chicken", "egg"]
bread = ["white","brown","sourdough", "whole wheat", "rye", "baugette"]

rand_veg = random.randrange(len(vegetables))
rand_cheese = random.randrange(len(cheese))
rand_meat = random.randrange(len(meat))
rand_bread = random.randrange(len(bread))

print(f"""Your sandwich:
    {bread[rand_bread]}
    {vegetables[rand_veg]}
    {cheese[rand_cheese]}
    {meat[rand_meat]}
    {bread[rand_bread]}""")

    