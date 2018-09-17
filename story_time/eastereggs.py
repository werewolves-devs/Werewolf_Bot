import random

def randiumlooks():
    msg_table = []

    msg1 = "Imagine a jumpsuit all covered on chocolate sprinkles, "
    msg1 += "that just got out of a dishwasher from the 1980s with a Samsung fridge next to it that isn't hooked up "
    msg1 += "to the WiFi network, but has three cables running through the dishwasher."
    msg2 = "He's the cable on the left."
    msg_table.append([msg1,msg2])

    msg1 = "Have you ever seen a green grizzly bear with a Christmas hat taking a bath in a pile of cow diarrea "
    msg1 += "whilst drinking a cocktail from pineapple juice and cockroach blood?"
    msg2 = "Well, he looks like a fucken potato."
    msg_table.append([msg1,msg2])

    msg1 = "Have you ever had that feeling that you really need to pie, but you can't because you're sitting in a giant room, "
    msg1 += "watching a presentation that you CANNOT interrupt?"
    msg2 = "Imagine that feeling upside-down, in green. That's him."
    msg_table.append([msg1,msg2])

    msg1 = "Ask Justin about it. He's seen a face reveal from him."
    msg_table.append([msg1])

    msg1 = "He looks like yo momma."
    msg2 = "Nah, I'm kidding. He ain't ugly."
    msg_table.append([msg1,msg2])

    msg1 = "Are you blind? 'cause if you're not, then I'm not surprised you don't know what he looks like!"
    msg_table.append([msg1])

    return msg_table[random.randint(0,len(msg_table)-1)]

def smite(user_id):
    msg_table = []

    msg = "You know that the people on this server only *tolerate* you, right, <@{}>?".format(user_id)
    msg_table.append(msg)

    msg = "<@{}>, you look like you've just taken a big dump in the cat litter!".format(user_id)
    msg_table.append(msg)

    msg = "My database is very good at remembering things, <@{}>, but I wished I could have it forget about you!".format(user_id)
    msg_table.append(msg)

    msg = "Really? You want me to smite <@{}>? ...can't we just perma-ban them?".format(user_id)
    msg_table.append(msg)

    msg = "You know, <@{}>, I appreciate your self confidence. You really have to not care about what others think if you wanna have a lifestyle like that.".format(user_id)
    msg_table.append(msg)

    msg = "Nah."
    msg_table.append(msg)

    msg = "Actually, I think they have a point."
    msg_table.append(msg)

    msg = "I never forget a user's profile. But yours make me wish I could, <@{}>.".format(user_id)
    msg_table.append(msg)

    msg = "In 200 years, no-one will remember you, <@{}>!".format(user_id)
    msg_table.append(msg)

    msg = "All right! If <@{}> signs up the next 5 games, they will be guaranteed to get the **Innocent** role!".format(user_id)
    msg_table.append(msg)

    msg = "Next game, I'm gonna make you a **Bloody Butcher**, but then *oops!* forget to add you until the first night!"
    msg_table.append(msg)

    msg = "<@{}> has been smitten.".format(user_id)
    msg_table.append(msg)

    msg = "***BOOM! <@{}> HAS BEEN SMITTEN!***".format(user_id)
    msg_table.append(msg)

    return msg_table[random.randint(0,len(msg_table)-1)]