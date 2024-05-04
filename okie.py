import random

# things in fridge:


vegetables = ["lettuce", "tomatoes", "red onions", "cucumber", "peppers", "pickels"]
cheese = ["cheddar", "marble", "blue cheese", "fetta"]
meat = ["ham", "bologna", "turkey", "bacon", "chicken", "egg"]
bread = ["white bread", "brown bread", "sourdough bread", "whole wheat bread", "rye", "baugette"]

rand_veg = random.randrange(len(vegetables))
rand_cheese = random.randrange(len(cheese))
rand_meat = random.randrange(len(meat))
rand_bread = random.randrange(len(bread))

toggle_fancy = False

print(f"""Your sandwich:
    {bread[rand_bread]}
    {vegetables[rand_veg]}
    {cheese[rand_cheese]}
    {meat[rand_meat]}
    {bread[rand_bread]}\n""")

print("Your imaginary sandwich:")
# flipside 
import cohere
co = cohere.Client('pS5EODFdSJ8qm02qMvV0YWSGiNBNzYoN4z04pkLD')

# response = co.chat(
#     chat_history=[
#         {"role": "USER", "message": "Generate an imaginary meat, like 'celestial mutton' or 'fillet junglefish"},
#         {
#             "role": "CHATBOT",
#             "message": "Angry ham",
#         },
#         {"role": "USER", "message": "Generate an imaginary meat, like 'celestial mutton' or 'fillet junglefish"},
#         {
#             "role": "CHATBOT",
#             "message": "Recyclable beef",
#         },
#     ],
#     message="Generate an imaginary meat, only give its name",
#     # perform web search before answering the question. You can also use your own custom connector.
#     connectors=[{"id": "web-search"}],
# )


from wonderwords import RandomWord

r = RandomWord()

ibread = f"{r.word(include_parts_of_speech=['adjectives'])} {bread[rand_bread]}"
iveg = f"{r.word(include_parts_of_speech=['adjectives'])} {vegetables[rand_veg]}"
icheese = f"{r.word(include_parts_of_speech=['adjectives'])} {cheese[rand_cheese]}"
imeat = f"{r.word(include_parts_of_speech=['adjectives'])} {meat[rand_meat]}"

print(f"""
    {ibread}
    {iveg}
    {icheese}
    {imeat}
    {ibread}\n""")

if toggle_fancy == True:
    response = co.chat(
        
        message=f"Generate an explanation of the taste and origins of a sandwich containing: {ibread}, {iveg}, {icheese}, and {imeat}. Talk in an extremely fancy and exquisite way, and give the sandwich a fancy name",
        # perform web search before answering the question. You can also use your own custom connector.
        connectors=[{"id": "web-search"}],
    )
else:
    response = co.chat(
        
        message=f"Generate an explanation of the taste and origins of a sandwich containing: {ibread}, {iveg}, {icheese}, and {imeat}. Use humour in your explanation, create wild explanations of its origins, make it understanble for kids",
        # perform web search before answering the question. You can also use your own custom connector.
        connectors=[{"id": "web-search"}],
    )

# funky vs fancy description

print(response.text)
