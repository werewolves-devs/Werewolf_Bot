def exclamate(text):
    msg = "**======================\n                {}\n======================\n**".format(text.upper())
    return msg

def power(role,user_id=0):
    if role == 'Assassin':
        msg = exclamate('Assassin')
        msg += 'The time has arrived to free this town from the evil beings that roam around! '
        msg += 'Whom shall you assassinate to free this town from a potential threat?'
    elif role == 'Aura Teller':
        msg = exclamate('Aura Teller')
        msg += 'Your visions have come back and they show you the aura of... whose aura do they show exactly?'
    elif role == 'Crowd Seeker':
        msg = exclamate('Crowd Seeker')
        msg += 'You have once again decided to look through the crowd, searching for that one role you need. '
        msg += 'Whom shall you inspect tonight?'
    elif role == 'Cupid':
        msg = exclamate('Cupid')
        msg += 'Your arrows have gone loose, and you accidentally shot yourself! You know what\'s about to happen...\n'
        msg += 'It\'s time to choose your least unattractive buddy in town, so that the two of you can fall in love!'
    elif role == 'Dog':
        msg = exclamate('ARROOOO')
        msg += 'Dear Dog, it is time to see where your true loyalty lies; with your friends from town or where nature calls you!\n'
        msg += 'Time to make a choice! What will you be? An **Innocent**, a **Cursed Civilian** or a **Werewolf**?'
    elif role == 'Exorcist':
        msg = exclamate('Exorcist')
        msg += 'Every night you are haunted by the memory of your first exorcism. That poor girl... Tonight is no different.'
        msg += 'Who do you choose to undoom tonight?'
    elif role == 'Fortune Teller':
        msg = exclamate('Fortune Teller')
        msg += 'You stare into your crystal ball, finally able to focus on the mystic smoke after a long day of work in the field.'
        msg += 'Who\'s role will you check tonight?'
    elif role == 'Grandma':
        msg = exclamate('Oh Wise One,')
        msg += 'Which children have been naughty today?'
        msg += 'Who will you prevent from voting tomorrow?'
    elif role == 'Hooker':
        msg = exclamate('Hooker')
        msg += 'After a long day of work, most people get to rest. But for you, work is just beginning.'
        msg += 'Who will you pay a special visit to tonight?'
    elif role == 'Innkeeper':
        msg = exclamate('Inkeeper')
        msg += 'You have polished the bar for the 20th time today and the last patron has retired to their room.'
        msg += 'Who do you wish to unfreeze tonight?'
    elif role == 'Look-Alike':
        msg = exclamate('Master of Illusion')
        msg += 'You have spent all day studying the townspeople, and are ready to make your choice.'
        msg += 'Who\'s role will you take on going forward?'
    elif role == 'Priest':
        msg = exclamate('Holy One')
        msg += 'The holy water is prepared. You are purified and sanctified. The task is at hand.'
        msg += 'Is someone worthy of being sanctified? Who will recieve the blessing of the holy water?'
    elif role == 'Priestess':
        msg = exclamate('Priestess')
        msg += 'The gods are kind! You have completed your daily rituals and the purification ceremony is upon us.'
        msg += 'Who will you purify tonight?'
    elif role == 'Raven':
        msg = exclamate('Cacaww!')
        msg += 'Men are punny! They should fear our cries!'
        msg += 'Who shall you threaten tonight?'
    elif role == 'Witch': #this role does't exist yet, but still, it's in the book.
        msg = exclamate('Witch')
        msg += 'Your cauldron is bubbling. Your potions gurggle.'
        msg += 'Will you use the Potion of Life? Or perhaps the Potion of Death?'
    elif role == 'Barber':
        msg = exclamate('Barber')
        msg += 'Cutomers come and go, but once in a while, an accident could happen. Decisions, decisions...'
        msg += 'Do you wish to kill someone today? Who will bleed out in your chair? Do you wish to reveal yourself?'
    elif role == 'Royal Knight':
        msg = exclamate('Royal Knight')
        msg += 'The royal proclamation you carry, for forgiving any lynchee-to-be, weighs heavily in your satchel every day.'
        msg += 'Do you wish to forgive the lynchee-to-be today?'
    elif role == 'Curse Caster':
        msg = exclamate('Curse Caster')
        msg += 'Mankind is evil! You should turn everyone into a werewolf for ultimate revenge.'
        msg += 'Who shall you curse tonight?'
    elif role == 'Infected Wolf':
        msg = exclamate('Infected Wolf')
        msg += 'Your fangs drip poison, ready to turn someone to your team at any moment.'
        msg += 'Do you wish to infect someone? Who will fall to your fangs and join the Wolf team?'
    elif role == 'Lone Wolf':
        msg = exclamate('AROOOOO')
        msg += 'The moon rises and you feel the call of the pack. But it is not time to join them yet.'
        msg += 'Who will you consume tonight?'
    elif role == 'Warlock':
        msg = exclamate('Warlock')
        msg += 'Your blackened and warped crystal ball still functions as well as ever. It is ready to obey the power of the Warlock.'
        msg += 'Who\'s role will you check tonight?'
    elif role == 'Tanner':
        msg = exclamate('Tanner')
        msg += 'The disguises you made last night are prepared. You will fool the fortune teller!'
        msg += 'Who do you wish to disguise today?'
    elif role == 'White Wolf':
        msg = exclamate('White Werewolf')
        msg += 'Your pack mates are just as tasty as the townspeople.'
        msg += 'Which werewolf will you snack on tonight?'
    elif role == 'Devil':
        msg = exclamate('Devil')
        msg += 'The fires of hell are ever hungry, never satisfied.'
        msg += 'Who will you give the wager to tonight?'
    elif role == 'Flute Player':
        msg = exclamate('Flute Player')
        msg += 'All rats follow the piper. All townspeople will one day be enchanted.'
        msg += 'Who shall you enchant tonight?'
    elif role == 'Ice King':
        msg = exclamate('Ice King')
        msg += 'The seeping cold slowly freezes all. The world will be frozen, soon enough.'
        msg += 'Who\'s roles will you guess tonight, and what will they be?'
    elif role == 'Pyromancer':
        msg = exclamate('Burn Baby, Burn!')
        msg += 'Your powder is ready, and of course your lighter is too. You are ready to light a *fiyah*.'
        msg += 'Who will you powder tonight? ...Or perhaps you wish to ignite and watch the world burn?'
    elif role == 'The Thing': #apparently this is a night user too?
        msg = exclamate('Monster!')
        msg += ''
        msg += 'Who will you do the thing to tonight?'
    elif role == 'Vampire':
        msg = exclamate('Vampire')
        msg += 'The army of the dead will rise!'
        msg += 'Who shall you demonize tonight?'
    elif role == 'Zombie':
        msg = exclamate('BRAINZZZZZ')
        msg += 'Tasty, tasty brains. Must eat more.'
        msg += 'Who will you bite tonight?'
    else:
        msg = "Hey bud! Time to do something!"
    # TODO

    return msg

def creation(role,user_id=0):
    msg = 'That is strange! Your role doesn\'t exist in my logs.... or not yet, at least.\n'
    msg += 'But don\'t worry! At this stage, this message\'s perfectly normal. :hugging:'

    if role == 'Amulet Holder':
        msg = exclamate('AMULET HOLDER,')
        msg = "Has it been forged? Has it been made? Crafted by hands, or created by magic? Who knows. "
        msg += "It doesn't really matter. All that matters, is that you feel comfortable bringing it around, "
        msg += "and it's a great artifact to hang above your bed!\nAlso, you noticed that everyone keeps complaining "
        msg += "about attacks during the night, but you haven\'t noticed anything lately.\n"
        msg += "Does the amulet protect you...? Naah, that's superstition. But it's a beautiful amulet anyway.\n"
        msg += "**You are currently wearing the amulet. You cannot be killed during the night. "
        msg += "Except for the first Amulet Holder, to whom this amulet will return if the new owner dies.**"

    if role == 'Assassin':
        msg = exclamate('Dear Assassin,')
        msg += "This town\'s spirit has been corrupted, evil has spread across the streets, "
        msg += "and the smell of death roams around every corner! Luckily, you will put it out of its misery soon, "
        msg += "for you shall effectively get rid of all evil that roams around the city.\n"
        msg += "Though.... you will need to make sure. On the first night, you shall not kill anyone yet. "
        msg += "Sacrifices may be necessary in the near future, but one shall not end a fight before it has begun.\n"
        msg += "**You are the Assassin. Kill all wolves and solo players in town! Good luck.**"

    if role == 'Aura Teller':
        msg = exclamate('Dear Aura Teller,')
        msg += 'The spirits have been talking to you lately, and they kept showing you weird shapes of other civilians... '
        msg += 'The shapes became brighter and brighter, and as time had progressed, you started to see... '
        msg += 'thoughts. Emotions. Intentions. Some were good, some were not so good, those dreams were beautiful!\n'
        msg += 'The least pleasant one was when you visited your neighbours and found out where the constant \"oohs\" '
        msg += 'and \"aahs\" were coming from, but you started to be able to control this power. '
        msg += 'You would find out later that this was a very effective way to spot the evil ones in your town!'
        msg += '**You are the Aura Teller. Inspect players\' auras to investigate if they\'re part of the wolf pack.**'

    if role == 'Baker':
        msg = exclamate('Hello, bakers')
        msg += 'The trusted guild of bakers is something that you all hold in high regard. With benefits, as you '
        msg += 'have so much trust in each other, that you dare to assume the others won\'t turn into hungry wolves '
        msg += 'at night. After all, you gotta wake up at four in the morning to start baking bread together!\n'
        msg += 'Yes, as long as no-one amongst you gets corrupted, you know you can fully trust each other, '
        msg += 'and take the journey of trust *together*.\n'
        msg += '**You are the bakers. All other members of this channel are bakers too. Work together to eliminate '
        msg += 'all threats, and secure the town from wolves, solo players and other enemies.**'

    if role == 'Butcher':
        msg = exclamate('BLOOD.')
        msg += "That's your trademark. No meat has too much blood for you to not sell it. Anything the customer wants!\n"
        msg += "You butchers love your job, and your healthy work environment makes the job even greater! "
        msg += "With the strange events happening in town, you wish to trust each other, but it seems that "
        msg += "one of you has enjoyed the presence *(the taste!)* of blood a little too much. "
        msg += "You better be careful, before something wrong starts to happen!\n"
        msg += "**You are the Butchers! All the other players in this channel are Butchers too, except for ONE. "
        msg += "That one is the Bloody Butcher. Eliminate the Bloody Butcher before they can eat YOU!**"
    
    if role == 'Barber':
        msg = exclamate('Clip Clip Clip')
        msg += "The authorities say they have everything under control, but your daily chats with the citizens tells you "
        msg += "something different. No, they have no idea what they're doing, and you know **EXACTLY** who's the fault "
        msg += "of all this!\n You know where and how you are gonna kill them, you just need to wait for the right moment. "
        msg += "This elimination should not only kill that monster, but should also become a statement; no longer does this "
        msg += "town accept to be tortured!"
        msg += "**You are the Barber! You can kill a player at any time during the day. Choose wisely, however! "
        msg += "You can only use this power once.**"

    if role == 'Crowd Seeker':
        msg = exclamate('Seek and thou shall find')
        msg += "Your powers do not allow you to sense specific players too well, but you are capable of following your "
        msg += "senses and finding specific roles among the crowd! This is why you've given yourself the task to find "
        msg += "and kill the evil geings in your town!\n"
        msg += "**You are the Crowd Seeker! Use your powers to confirm or debunk people who claim their roles. "
        msg += "Make sure to kill everything that does not belong here!**"

    return msg
