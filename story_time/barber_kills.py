import random

def barber_kill_story(barber_id,victim_id):
    story_table = []

    msg = "What the town did not realize was that there was someone amongst them who hated <@{}> so much,".format(victim_id)
    msg += " that they thought they had to be cut up in pieces!"
    msg += " It wasn't long after the body of <@{}> was found when people realised it must've been the barber".format(victim_id)
    msg += " who performed this assassination!\n"
    msg += "*<@{}>, the barber, has killed <@{}> and has now turned into a regular **Innocent**.".format(barber_id,victim_id)

    story_table.append(msg)

    msg = '*"Down with the wolves! Down with the wolves!"* ' + "That's what people chanted all day."
    msg += " 'Easier said than done,' was <@{}> response to that. They never believed in words, only actions would achieve something!\n".format(barber_id)
    msg += " Though that may sound innocent or even *cute*, this was what finally led to the assassination of <@{}> on this day.".format(victim_id)
    msg += " They were found dead, lying in a dumpster behind the barbershop.\n"
    msg += "*<@{}>, originally a barber, has assassinated a victim and has now turned into a regular **Innocent**.".format(barber_id)
    msg += " Meanwhile, unfortunately, <@{}> has deceased.*"

    story_table.append(msg)

    msg = "The Wild West used to have some strange rules if one was to compare them."
    msg += " Stealing a horse deserved a sentence of death, while killing in a duel was completely fine!"
    msg += " However, as <@{}> was to found out on this day, those rules were not strange at all, compared to this town's.\n".format(barber_id)
    msg += "<@{}>, a happy barber, had a pretty good conversation with one of their clients, <@{}>.".format(barber_id,victim_id)
    msg += " However, their client appeared to lose a lot of hair, hair which strangely resembled that of the hair found on the town's dead bodies..."
    msg += " The barber immediately knew what to do, and *accidentally* slit their knife in the wrong direction,"
    msg += " effectively beheading their client.\n"
    msg += "<@{}>, realising what the consequences would be, prepared themselves for a long time in jail, or even getting lynched that day,".format(barber_id)
    msg += " but found out nothing would happen!\n"
    msg += "Apparently, this town had a weird rule that going to the barber made the barber responsible of your life. Not their fault if you die.\n"
    msg += "After this day, however, no-one visited <@{}>'s barbershop anymore, forcing them to close for good.\n".format(barber_id)
    msg += "*<@{}>, a barber, has assassinated <@{}> and has become an **Innocent**!*"

    story_table.append(msg)

    msg = "Later that day, another body was found! Were they too careless, and did they miss that one body?\n"
    msg += "No, it seems like this one was new. The flesh was still warm, and the cuts in <@{}>'s neck did not have much blood yet;".format(victim_id)
    msg += "The murder must've been done a few minutes ago.\n"
    msg += "In other parts of the town, people noticed that <@{}>, the town's favourite barber, had a lot of blood stains on their hands and clothes...\n".format(barber_id)
    msg += "*<@{}>, a barber, has killed <@{}> and turned into an **Innocent**!*"

    story_table.append(msg)

    return story_table[random.randint(0,len(story_table)-1)]
