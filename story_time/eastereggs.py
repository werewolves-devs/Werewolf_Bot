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
