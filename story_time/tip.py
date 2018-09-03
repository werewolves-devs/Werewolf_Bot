import random as randium

def random():
    msg_table = []

    msg = "If you're the **Alcoholic**, Do not make it obvious that you can only talk in the tavern. "
    msg += "Such information is a good thing to share, but wait a short time before you share this. "
    msg += "In the beginning, the werewolves don't really know who to kill, so they'll go after anyone of whom they know the role."
    msg_table.append(msg)

    msg = "The **Assassin**'s main weakness is that they're alone. "
    msg += "Where the cult leader has their cult members to gather information, "
    msg += "the assassin has to do it all on themselves. "
    msg_table.append(msg)

    msg = "Roles like the Curse Caster, the Tanner and the Warlock prefer to remain anonymous and unseen in the beginning "
    msg += "of the game. If the **Aura Teller** receives a green aura from an active and attention-seeking player, "
    msg += "they are most likely to be trusted."
    msg_table.append(msg)

    msg = "Though the **Baker** role is one of the simplest roles, there are few who play this role well. "
    msg += "Because imitating the baker group is very risky and rarely happens, the Bakers are a safe haven "
    msg += "for crucial roles to find others.\n"
    msg += "The bakers aren't a primary target for the werewolves, so it isn't very risky to publicly share their roles."
    msg_table.append(msg)

    msg = "Immediately announincing the **Butcher** roles may seem beneficial for the town, but it's actually "
    msg += "a bad move if there's a **Tanner** in the town. They can easily disguise all butchers as bloody butchers.\n"
    msg += "This effectively hides the **Bloody Butcher** and frames the genuine **Butchers**."
    msg_table.append(msg)

    msg = "The **Aura Teller** is an easy way to find the **Bloody Butcher** among the group of **Butchers**. "
    msg += "The **Aura Teller**'s vision cannot be influenced by the **Flute Player** or the **Tanner**, "
    msg += "so the result will be definite and unambiguous."
    msg_table.append(msg)

    msg = "A good strategy for the **Crowd Seeker** is to ask for people's roles, and then confirm them during the night "
    msg += "- but subtlety is key. The **Crowd Seeker** is a big target due to the power of their role."
    msg_table.append(msg)

    msg = "The longer the **Cult Leader** survives, the more the game will be in the town's favour. "
    msg += "That is why it's better for the **Cult Leader** to stay down and to have the **Cult Members** "
    msg += "look around for targets to kill during the night."
    msg_table.append(msg)

    msg = "Though the cult doesn't depend on **Cult Members**, they are still very important. "
    msg += "The **Cult Members** need to provide the cult with information, so that the cult becomes "
    msg += "aware of the game's situation without having to risk the **Cult Leader**'s role."
    msg_table.append(msg)

    msg = "Though the Cursed Civilian isn't the most interesting role to play, it is one of the best "
    msg += "positions to be in. At the end of the game, the **Cursed Civilian** has the ability to win "
    msg += "with both the town and the werewolves; if the werewolves are about to ask, the **Cursed "
    msg += "Civilian** can simply ask nicely if they can get attacked by the wolves."
    msg_table.append(msg)

    msg = "Before the first night starts, there is still a full day that the **Dog** can use to talk to people, "
    msg += "investigate roles, situations and players to help make the decision which role they feel like playing."
    msg_table.append(msg)

    msg = "If a player pretends to be suspicious and seeks contact with the werewolves, it is most likely "
    msg += "that they will die by the lynch. This is the perfect strategy for the **Executioner**; "
    msg += "the **EXecutioner** seeks contact with the wolves. When they get lynched, they kill a wolf *and*"
    msg += "get revealed by the lynch and then can be trusted when giving away the list of werewolves."
    msg_table.append(msg)

    return msg_table[randium.randint(0,len(msg_table) - 1)]