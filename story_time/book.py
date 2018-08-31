# From the rule book


def find_role_rules(role):
    if role == "Innocent":
        msg = '''
    The innocents are normal players. They only know their own role. The innocents can vote during the day on whomever they suspect to be an enemy, and hope during the night that they won't get killed. The Curse Caster can turn innocents into Cursed Civilians.

    Innocent players do not gain a personal Secret Channel. Other than the Public Channels and the voting booth, they have access to no other channels.

    The infected wolf can turn the innocent into a werewolf.

    '''
    if role == "Alcoholic":
        msg = '''
    The alcoholic cannot talk on the town square, but is only allowed to talk in the tavern. The alcoholic can talk in the conspiracy channels.

    The curse caster cannot curse the alcoholic.

    The infected wolf can turn the alcoholic into a werewolf.

    If the Alcoholic becomes undead, they will be able to talk on the town square again.

    '''
    if role == "Amulet Holder":
        msg = '''
    At the start of the game, the amulet holder will gain the item called the *Amulet of Protection*. They who hold the *Amulet of Protection*, can neither die nor turn undead during the night. If the holder of the amulet dies, the amulet will be returned to the Amulet Holder.

    If the player who holds the *Amulet of Protection* dies in any other way, the amulet will be lost forever, and the amulet holder will turn into a regular innocent.

    The amulet can be given away during the day. Giving the amulet is anonymous, the receiver will not know from whom they got the amulet. Once the night starts, the amulet is bound to the user, and the amulet can no longer be switched.

    The Amulet doesn't work for the Amulet Holder; they will not be protected during the night. The same goes for the town elder.

    If the player who holds the amulet dies, it will only be revealed to the Amulet Holder.

    '''
    if role == "Assassin":
        msg = '''
    The assassin may choose a player to kill. This happens every night, except for the first one.

    The assassin's kill is an end effect; the player will die at the end of the night.

    If the look-alike copies the assassin, then the assassins won't join. The look-alike will know the assassin's role, of course, but the original assassin won't know the look-alike's.

    The curse caster cannot curse the assassin.

    The infected wolf can turn the assassin into a werewolf.

    If the assassin turns undead, they will lose their powers.

    '''
    if role == "Aura Teller":
        msg = '''
    The aura teller cannot see a player's role, but they can check whether a player is in the wolf pack. This means that they can recognize the aura of the werewolf, sacred werewolf, white werewolf, etc, but not the roles like the lone wolf, tanner warlock or curse caster. The aura teller gains less information, but isn\'t influenced by the powers of the tanner.

    The Aura Teller's inspection is an immediate effect; they will know the aura of their victim immediately after inspecting.

    If the look-alike copies the aura teller, then the aura tellers won't join. The look-alike will know the aura teller's role, of course, but the original aura teller won't know the look-alike's.

    The curse caster cannot curse the aura teller.

    The infected wolf can turn the aura teller into a werewolf.

    If the aura teller turns undead, they will lose their powers.

    '''
    if role == "Baker":
        msg = '''
    Bakers are a special type of innocents; they know all other players who gained the baker role. They can fully trust and rely on each other.

    Bakers share a private channel, where they can communicate with each other. If a baker loses their role in any way, they will still keep access to the channel. This means that at some point, a baker may betray the group.

    If the look-alike copies a baker, then they will be added to the same group as the other bakers.

    The curse caster cannot curse the baker.

    The infected wolf can turn the baker into a werewolf.

    If the baker turns undead, they will keep contact with the other bakers.

    '''
    if role == "Butcher":
        msg = '''
    The Butcher is like the baker group, a group of trusted players; except for that exactly one butcher is a werewolf! This player is called the Bloody Butcher.

    If the look-alike copies a butcher, they will be added to the group. However, their role nor whom they copied is revealed, for they could as well have copied the bloody butcher.

    The curse caster cannot curse the butcher.

    The infected wolf can turn the butcher into a werewolf.

    If the baker turns undead, they will keep contact with the other butchers.

    '''
    if role == "Barber":
        msg = '''
    At any time during the day, the barber may once kill another player. The barber also receives the choice whether they want to be revealed or not.

    The barber's kill is an immediate effect; the player will die immediately after

    The barber cannot kill anyone on the first day or during the night.

    If the look-alike copies the barber, then the barbers won't join. The look-alike will know the barber's role, of course, but the original barber won't know the look-alike's.

    The Idiot's powers do not trigger when attacked and killed by the barber. The Idiot will die immediately.

    The town elder cannot die during the day. Hence, the town elder cannot be killed by the barber. The barber will fail to assassinate the player. The barber will turn innocent without killing anyone.

    The curse caster cannot curse the barber.

    The infected wolf can turn the barber into a werewolf.

    If the barber turns undead, they will lose their powers.

    '''
    if role == "Crowd Seeker":
        msg = '''
    The crowd seeker can select three different players each night, and guess for each of them what their role could be. Any correct guesses made will be confirmed.

    The crowd seeker's seeking is an immediate effect; they will gain an answer to their question immediately.

    If the look-alike copies the crowd seeker, then the crowd seekers won't join. The look-alike will know the crowd seeker's role, of course, but the original crowd seeker won't know the look-alike's.

    The crowd seeker's powers can be influenced by the flute player's and the tanner's.

    A seeking is an immediate effect; the player will gain their requested info directly after having made the guesses.

    The curse caster cannot curse the crowd seeker.

    The infected wolf can turn the crowd seeker into a werewolf.

    The crowd seeker's powers are influenced by the tanner's disguises.

    The crowd seeker's powers are influenced by the flute player; if they're enchanted, and there's still a flute player alive, seeking a player has a 60\% chance of confirming them as a flute player, and a 40\% chance of confirming them as their actual role (or at least the role that the tanner gave them).

    If the crowd seeker turns undead, they will lose their powers.

    '''
    if role == "Cult Leader":
        msg = '''
    The Cult Leader is the owner of a group called the cult. The cult can kill one player each night, except for on the first night. When the Cult Leader dies, the cult gets disbanded. The players can no longer kill, and all Cult Members will turn into regular innocents.

    The cult's kill is an end effect; the chosen victim will die at the end of the night.

    The runner's effect will not trigger when they are being attacked by the cult, which means they'll die immediately.

    The cult only gets disbanded when the player who originally was a cult leader, dies. This is referring to rare situations like the ones where the Cult Leaders turns into a werewolf. In such cases, the cult would continue to exist.

    If the Look-Alike copies the Cult Leader, then the cult has multiple leaders, and the cult will be disbanded when all the Cult Leaders have died.

    The curse caster cannot curse the cult leader.

    The infected wolf can turn the cult leader into a werewolf.

    If the cult leader turns undead, they will remain part of the cult. The cult will lose their powers if all members are undead.

    '''
    if role == "Cult Member":
        msg = '''
    The Cult Member is part of the cult. The cult can kill one player each night, except for the first night. When the Cult Leader dies, the cult gets disbanded, and the Cult Member will turn into a regular Innocent.

    The cult decides their victims by voting on whom they suspect most. The cult's kill is an end effect; the chosen victim will die at the end of the night.

    If the look-alike copies a cult member, they will join the cult.

    The curse caster cannot curse the cult member.

    The infected wolf can turn the cult member into a werewolf.

    If the cult member turns undead, they will remain part of the cult. The cult will lose their powers if all members are undead.

    '''
    if role == "Cupid":
        msg = '''
    During the first night, the cupid can choose a player. They can no longer vote to kill each other, and they will die if the other player dies. After the player has chosen their lover, they will turn NOT turn into an innocent.

    Choosing a lover is an immediate effect; the couple will immediately fall in love with each other.

    If the two players are on different teams, they will only win when both win conditions are fulfilled.

    For example, if the couple is Cupid and a Werewolf, everyone must die.

    Another example is when the couple is Undead and a Vampire, then the normal Vampire win condition must be reached.

    Or, if they're both Townspeople, they belong to the Townspeople team and can win together with them.

    If the look-alike copies the cupid before they have chosen a lover, then the look-alike gets to choose a lover as well. If the cupid has already chosen a lover, then they will form a threesome, and all become lovers of each other.
    The same goes for when the cupid copies the cupid's lover.

    The Infected Wolf can turn the Cupid into a werewolf. If this happens before the Cupid has chosen a target, then they won't need to choose one.

    The curse caster cannot curse the cupid.

    The infected wolf can turn the cupid into a werewolf. The cupid will still keep their lover.

    If the cupid turns undead, they will keep their lover. If they haven't chosen one yet, then they won't.

    '''
    if role == "Cursed Civilian":
        msg = '''
    The cursed civilian is part of the townspeople team. However, if they get attacked by the werewolves, they will turn into a werewolf, instead of dying.

    If the look-alike copies the cursed civilian, then the cursed civilians won't join. The look-alike will know the cursed civilian's role, of course, but the original cursed civilian won't know the look-alike's.

    The Cursed Civilian can be purified by the Priestess. The cursed civilian will then turn into a regular innocent.

    The Infected Wolf can turn a cursed civilian into a werewolf, though this is not recommended. Attacking the player instead is often a wiser decision.

    If the cursed civilian turns undead, they will no longer turn into a werewolf when they get attacked.

    '''
    if role == "Dog":
        msg = '''
    During the first night, the Dog will be able to choose their role; they can play the game as an innocent, aa a cursed civilian or as a werewolf. They will continue to play the game as their chosen role.

    Changing the dog's role is an immediate effect; their role will change immediately after they have chosen their new role.

    If the dog hasn't chosen a role before the night ends, the dog will be given the role of the innocent.

    If the look-alike copies the Dog before the dog has chosen a role, then the look-alike gets to choose a role of his own as well.

    The curse caster cannot curse the dog.

    The infected wolf can turn the dog into a werewolf.

    If the dog turns undead, they will no longer be able to choose a role.

    '''
    if role == "Executioner":
        msg = '''
    Whenever the Executioner is chosen to be lynched, it will be prevented, and the Executioner will be able to choose another player. That player will die in their place. After the failed lynch, the Executioner will turn into a regular innocent.

    The Executioner may also choose to not let anyone die in their place.

    If the look-alike copies the executioner, then the executioners won't join. The look-alike will know the executioner's role, of course, but the original executioner won't know the look-alike's.

    The curse caster cannot curse the executioner.

    The infected wolf can turn the executioner into a werewolf.

    If the executioner turns undead, they will lose their powers.

    '''
    if role == "Exorcist":
        msg = '''
    Every night, the Exorcist may choose a player to undoom. An undoomed player will lose the demonized effect, and if the player was a Vampire, Undead, Demon, The Devil or The Thing, then they will die.

    Undooming a player is an immediate effect; the effects, including dying, will happen immediately.

    If the look-alike copies the exorcist, then the exorcists won't join. The look-alike will know the exorcist's role, of course, but the original exorcist won't know the look-alike's.

    This is one of the few immediate effects that can kill a player instantly.

    The curse caster cannot curse the exorcist.

    The infected wolf can turn the exorcist into a werewolf.

    The Exorcist can be demonized by the Vampire, but the Exorcist will never turn undead. If they are supposed to turn undead, they will die immediately.

    '''
    if role == "Fortune Teller":
        msg = '''
    Each night, the fortune teller can inspect a player. The fortune teller will be told what their role is.

    Inspecting a player is an immediate effect; the role will be revealed immediately.

    Each fortune teller can have at most one fortune apprentice. In case of multiple fortune tellers in-game (and a smaller amount of apprentices), the fortune teller will be told whether they have an apprentice or not, but they will not be told who it is.

    If the look-alike copies the fortune teller, then the fortune tellers won't join. The look-alike will know the fortune teller's role, of course, but the original fortune teller won't know the look-alike's.

    The curse caster cannot curse the fortune teller.

    The infected wolf can turn the fortune teller into a werewolf.

    The fortune teller's powers are influenced by the tanner's disguises.

    The fortune teller's powers are influenced by the flute player; if they're enchanted, and there's still a flute player alive, inspecting a player has a 60\% chance of displaying them as a flute player, and a 40\% chance of displaying them as their actual role (or at least the role that the tanner gave them).

    The fortune teller's powers are influenced by the tanner's disguises.

    If the fortune teller turns undead, they will lose their powers.

    '''
    if role == "Fortune Apprentice":
        msg = '''
    The fortune apprentice is being given a fortune teller. When the fortune teller dies, the apprentice becomes the new fortune teller. This will happen anytime in the game, even if the fortune apprentice's role has changed.

    The apprentice will turn into a fortune teller whenever the given fortune teller dies, not when they lose their role. This applies to rare scenarios where the fortune teller dies after having turned into, for example, a werewolf.

    If the look-alike copies a fortune apprentice, then they are in the same class, and they WILL know each other.

    The curse caster cannot curse the fortune apprentice.

    The infected wolf can turn the fortune apprentice into a werewolf. However, they should remember that the fortune apprentice may become a fortune teller again when their fortune teller dies, even if the fortune teller no longer had their original role.

    Becoming an undead is an exception, and the fortune apprentice will no longer turn into a fortune teller after they have turned undead.

    '''
    if role == "Grandma":
        msg = '''
    Each night, Grandma can choose three players. The next day, those three players aren't allowed to vote. Grandma can choose herself as one of them.

    Making three players unable to vote is an immediate effect; the players will be assigned immediately that they are no longer allowed to vote. This is relevant in scenarios where Grandma changes her role during the night.

    If the look-alike copies Grandma, then Grandma and the look-alike won't join. The look-alike will know Grandma's role, of course, but Grandma won't know the look-alike's.

    The curse caster cannot curse Grandma.

    The infected wolf can turn Grandma into a werewolf. You don't wanna see that happen.

    If Grandma turns undead, Grandma will lose her powers.

    '''
    if role == "Hooker":
        msg = '''
    Each night, the hooker sleeps with another player. Since the hooker is at the other player's house and not at home, any attacks in the night will fail; however, if the person they're sleeping over at is being attacked, then so are they.

    Choosing a player to sleep with is an immediate effect. From that point on, they will stay with that player for the rest of the night.

    Not the result, but the action is copied; if the Hooker chooses a Cursed Civilian and the Cursed Civilian gets attacked, then the Cursed Civilian turns, but the Hooker dies. Same with protected players; the Hooker won't survive a cult attack if the other is a Sacred Wolf.

    The Hooker can also choose not to sleep with anybody.

    The curse caster cannot curse the hooker.

    The infected wolf can turn the hooker into a werewolf.

    If the hooker turns undead, they will lose their powers.

    '''
    if role == "Huntress":
        msg = '''
    Whenever the huntress dies, she can choose a player to die along with her. The role will be revealed to all, and the other player is killed immediately. Special effects like the town elder, huntress, sacred wolf and turning undead still apply.

    If the look-alike copies the huntress, then the huntresses won't join. The look-alike will know the huntress' role, of course, but the original huntress won't know the look-alike's.

    The curse caster cannot curse the huntress.

    The infected wolf can turn the huntress into a werewolf.

    If the huntress turns undead, they will lose their powers.

    '''
    if role == "Idiot":
        msg = '''
    If the idiot dies during the death poll or during the night, the first attack will be prevented. However, the idiot loses the right to vote.

    It is not publicly announced that the idiot dies, and the idiot will keep access to the voting booth. His vote will simply no longer count. When the idiot turns into an Undead, they will be able to vote again.

    The Idiot's powers do not trigger when attacked and killed by the barber. The Idiot will die immediately.

    If the look-alike copies the idiot, then the idiots won't join. The look-alike will know the idiot's role, of course, but the original idiot won't know the look-alike's.

    The infected wolf can turn the idiot into a werewolf.

    '''
    if role == "Innkeeper":
        msg = '''
    Each night, the innkeeper may choose a frozen player to unfreeze. The unfrozen player will be able to speak again.

    If the look-alike copies the innkeeper, then the innkeepers won't join. The look-alike will know the innkeeper's role, of course, but the original innkeeper won't know the look-alike's.

    The curse caster cannot curse the innkeeper.

    The innkeeper cannot unfreeze themselves.

    If the innkeeper turns undead, they will lose their powers.


    '''
    if role == "Jack Robinson":
        msg = '''
    Your goal is the same as any other innocent, except for one extra goal; when the innocents win, Robin Jackson has to be dead. If Robin Jackson is still alive when the innocents win, then you will lose the game.

    If the look-alike copies Jack Robinson, then they will not join, but they both do need to kill Robin Jackson before the end of the game.

    The curse caster cannot curse Jack Robinson.

    The infected wolf can turn Jack Robinson into a werewolf.

    If Robin Jackson loses their roles in any other way (e.g. turning undead, becoming a werewolf, etc.), then that counts as well, and allows Jack Robinson to win the game with the other innocents.

    '''
    if role == "Look-Alike":
        msg = '''
    During the first night, the look-alike chooses a player. All data, including whether they are enchanted or not, demonized, in love, etc, is copied.

    Choosing a player to copy is an immediate effect.

    The target is not being told they have been copied by the look-alike, unless if it says so in their description. This means that if the look-alike copies a werewolf, he will join the wolf ranks, but the werewolves will not be told who has been copied; it could be that they copied the white werewolf, after all.

    If the Look-Alike chooses a player who turns out to be a look-alike as well, they will get to choose again.

    If the Look-Alike doesn't choose a player before the end of the first night, they will turn into a regular innocent.

    The curse caster cannot curse the look-alike.

    The infected wolf can turn the look-alike into a werewolf.

    If the look-alike turns undead, they will lose their ability to choose a player.

    '''
    if role == "Macho":
        msg = '''
    If the macho is killed during the night, they will survive until the next day. The macho will know who killed them, and it is up to him to decide whether he wants to share this information or not. At the end of the day, the macho dies.

    If it's a group that killed the macho, like the cult or the werewolves, then a random member who voted for the macho is selected.

    If the look-alike copies the macho, then the machos won't join. The look-alike will know the macho's role, of course, but the original macho won't know the look-alike's.

    The curse caster cannot curse the macho.

    The infected wolf can turn the macho into a werewolf. If they were in the dying state, this will save them as well.

    The Macho cannot be demonized, but they will never turn undead. The macho will always die at the end of the day, so it is impossible to turn undead.

    '''
    if role == "Mad Scientist":
        msg = '''
    At the start of the game, the Mad Scientist gets two players assigned. If the mad scientist dies, then so will the two other players. Special effects like the town elder, huntress, sacred wolf and turning undead still apply.

    Killing the two other players is an immediate effect.

    If the Look-Alike copies the Mad Scientist, the look-alike will have the same assigned victims as the real mad scientist.

    The curse caster cannot curse the mad scientist.

    The infected wolf can turn the mad scientist into a werewolf.

    If the mad scientist turns undead, they will lose their victims. The two players will no longer die if the original mad scientist dies.

    '''
    if role == "Priest":
        msg = '''
    Each night, the Priest can use his holy water on a player. If that player is on the Werewolf team, that player will die. If they are not, then the Priest will die.

    Using holy water upon a player is an end effect.

    If the look-alike copies the priest, then the priests won't join. The look-alike will know the priest's role, of course, but the original priest won't know the look-alike's.

    The curse caster cannot curse the priest.

    The infected wolf can turn the priest into a werewolf.

    If the priest turns undead, they will lose their powers.

    '''
    if role == "Priestess":
        msg = '''
    Each night, the priestess may choose one player. If that player is a cursed civilian, they will turn into a regular innocent. If the player is a sacred werewolf, they will turn into a regular werewolf.

    Purifying a player is an immediate effect.

    When the priestess purifies a player, the result will be positive, neutral or negative.

    If the result is positive, then the target was a cursed civilian or a sacred werewolf, and turned into an innocent or werewolf, respectively.

    If the result is neutral, then the target was already an innocent or a werewolf, so they cannot be purified.

    If the result is negative, then they had another role besides the innocent, cursed civilian, werewolf or sacred werewolf.

    If the look-alike copies the priestess, then the priestesses won't join. The look-alike will know the priestess' role, of course, but the original priestess won't know the look-alike's.

    The curse caster cannot curse the priestess.

    The infected wolf can turn the priestess into a werewolf.

    If the priestess turns undead, they will lose their powers.

    '''
    if role == "Raven":
        msg = '''
    Each night, the raven can threaten a player. The morning after, that player has 2 more votes against them on the daily death poll. However, only the Raven and the threatened player know about it.

    Threatening a player is an immediate effect.

    If the look-alike copies the raven, then the ravens won't join. The look-alike will know the raven's role, of course, but the original raven won't know the look-alike's.

    The curse caster cannot curse the raven.

    The infected wolf can turn the raven into a werewolf.

    If the raven turns undead, they will lose their powers.

    '''
    if role == "Robin Jackson":
        msg = '''
    Your goal is the same as any other innocent, except for one extra goal; when the innocents win, Jack Robinson has to be dead. If Jack Robinson is still alive when the innocents win, then you will lose the game.

    If the look-alike copies Robin Jackson, then they will not join, but they both do need to kill Jack Robinson before the end of the game.

    The curse caster cannot curse Robin Jackson.

    The infected wolf can turn Robin Jackson into a werewolf.

    If Jack Robinson loses their roles in any other way (e.g. turning undead, becoming a werewolf, etc.), then that counts as well, and allows Robin Jackson to win the game with the other innocents.

    '''
    if role == "Royal Knight":
        msg = '''
    The royal knight may forgive a player once, and prevent that player from being lynched that day. The Royal Knight is allowed to forgive themselves. When forgiving a player and cancelling a lynch, the royal knight will not be revealed.

    Forgiving a player is an end effect. The fact that the lynch has been canceled will only be revealed at the end of the day, when the player is about to be lynched.

    If the look-alike copies the royal knight, then the royal knights won't join. The look-alike will know the royal knight's role, of course, but the original royal knight won't know the look-alike's.

    The curse caster cannot curse the royal knight.

    The infected wolf can turn the royal knight into a werewolf.

    If the royal knight turns undead, they will lose their powers.


    '''
    if role == "Runner":
        msg = '''
    The runner can escape a werewolf attack once. They won't die, but they will lose the runner role, and turn into an innocent.

    If the look-alike copies the runner, then the runners won't join. The look-alike will know the runner's role, of course, but the original runner won't know the look-alike's.

    The curse caster cannot curse the runner.

    The infected wolf can turn the runner into a werewolf.

    If the runner turns undead, they will lose their powers.

    '''
    if role == "Town Elder":
        msg = '''
    The town elder cannot die during the daily death poll. If they're about to get lynched, their role will be revealed, and they will no longer be able to be hung up. After the third failed attempt to lynch the Town Elder, they will die to aging.

    If the look-alike copies the town elder, then the town elders won't join. The look-alike will know the town elder's role, of course, but the original town elder won't know the look-alike's.

    The curse caster cannot curse the town elder.

    The infected wolf can turn the town elder into a werewolf.

    If the town elder turns undead, they will lose their powers.

    '''
    if role == "Witch":
        msg = '''
    The Witch has two potions; a potion of life and a potion of death. Each night, they can choose whether they want to use either of those potions. If they use the potion of life, then no-one dies during that night. If they use the pot ion of death, they can choose one player to kill.

    Each potion can be used only once. They can also be used simultaneously in one night. The potion of life can also protect the witch herself. Do note that the potion of life only protects players from end effect kills; immediate kills, like the exorcist's, still apply.

    If the look-alike copies the witch, then the witches won't join. The look-alike will know the witch's role, of course, but the original witch won't know the look-alike's.

    The infected wolf can turn the witch into a werewolf.

    If the witch turns undead, they will lose their powers.

    '''

     # Werewolf Team

    if role == "Werewolf":
        msg = '''
    The Werewolf is a player who acts like a regular player during the day, but secretly kills players during the night, together with all the other werewolves.

    The Werewolf appears as a threat to the Aura Teller.

    If the look - alike copies a werewolf, they will be added to the wolf pack, but their role will not be revealed
    after all, they might as well have copied the white werewolf...

    The infected wolf can turn the werewolf into a werewolf. This may seem pointless, but it happens, when the infected wolf suspects a wolf of being the white werewolf.

    If the werewolf turns undead, they will still keep access to the wolf pack. The werewolves will still be able to kill a player every night, until all the werewolves are either dead or undead.

    '''
    if role == "Bloody Butcher":
        msg = '''
    The Bloody Butcher is a werewolf who is also part of the Butcher group. He is the traitor among the group, who tries to gain information.

    The Bloody Butcher appears as a threat to the Aura Teller.

    If the look - alike copies a werewolf, they will be added to the wolf pack and the butcher group, but their role will not be revealed
    after all, to the butchers, they might be the bloody butcher, and to the werewolves, they could be a second white werewolf...

    The infected wolf can turn the bloody butcher into a werewolf. This may seem pointless, for the bloody butcher won't lose access to the butcher group, but this may happen when the infected wolf suspects a bloody butcher of being the white werewolf.

    If the bloody butcher turns undead, they will still keep access to the butcher group and the wolf pack. The werewolves will still be able to kill a player every night, until all the werewolves are either dead or undead.

    '''
    if role == "Curse Caster":
        msg = '''
    Each night, the curse caster can curse a player. If that player is a regular innocent, they will turn into a cursed civilian. The Curse Caster cannot curse players with extra roles, like the runner, the cupid or the fortune teller. The curse caster does not know the werewolves, and it is their task to seek contact.

    Cursing a player is an immediate effect.

    The curse caster does not appear as a threat to the aura teller.

    If the look - alike copies the curse caster, then the curse casters won't join. The look-alike will know the curse caster's role, of course, but the original curse caster won't know the look-alike's.

    The infected wolf can turn the curse caster into a werewolf.

    If the curse caster turns undead, they will lose all their powers.

    '''
    if role == "Hell Hound":
        msg = '''

    Hell Hounds are the bakers of hell - quite literally. These werewolves know from each other that they are hell hounds, and they can use and share this information in their battle against the white werewolf.

    '''
    if role == "Infected Wolf":
        msg = '''
    At any time during any night throughout the game, the infected wolf may once choose a player to turn into a werewolf. They will lose their original role, and continue to play as a werewolf.

    Infecting a player is an immediate effect.

    The infected wolf appears as a threat to the aura teller.

    If the look - alike copies an infected wolf, they will be added to the wolf pack, but their role will not be revealed
    after all, they might as well have copied the white werewolf...

    The infected wolf can infect most players, but there are some exceptions, like the undead or the vampire, who will merely pretend to have become a werewolf, while in reality, they aren't. For those roles, it is mentioned in their description that they will not turn into a werewolf.

    Players you shouldn\'t infect are the Undead and the Vampire, while infecting the Fortune Apprentice isn\'t recommended either.

    If there are multiple infected wolves, the infected wolf can be turned into a werewolf by another infected wolf. This may seem pointless, but it happens when the other infected wolf suspects them of being the white werewolf.

    If the infected wolf turns undead, they will lose the power to infect a player, but they will keep access to the wolf pack. The werewolves will still be able to kill a player every night, until all the werewolves are either dead or undead.

    '''
    if role == "Lone Wolf":
        msg = '''
    The Lone Wolf doesn't know the other wolves, and starts off all alone. Each night, they can kill one player on their own. When another werewolf dies, the Lone Wolf loses their powers, join the wolf pack and turn into a regular werewolf.

    The exception is the white werewolf
    if a werewolf dies because they had been killed by the white werewolf, then the Lone Wolf will not join the wolves' ranks yet.

    Killing a player is an end effect
    the lone wolf will attack a victim at the end of the night.

    If the look - alike copies the lone wolf, then the lone wolves won't join. The look-alike will know the lone wolf's role, of course, but the original lone wolf won't know the look-alike's.

    The lone wolf does not appear as a threat to the aura teller.

    The infected wolf can turn the lone wolf into a werewolf.

    If the lone wolf turns undead, they will lose all their powers.

    '''
    if role == "Sacred Wolf":
        msg = '''
    The sacred wolf is a werewolf that cannot die during the night. However, if purified by a priestess, they will turn into a regular werewolf.

    The sacred wolf appears as a threat to the aura teller.

    If the look - alike copies a sacred werewolf, they will be added to the wolf pack, but their role will not be revealed
    after all, they might as well have copied the white werewolf...

    The sacred werewolf can be purified by the priestess. If that happens, they will turn into a regular werewolf.

    The infected wolf can turn the sacred wolf into a werewolf.

    The sacred wolf cannot die during the night, so they cannot turn undead. However, they can be demonized by the Vampire. If they happen to turn into a normal werewolf, they will be able to get killed during the night and turn undead.

    '''
    if role == "Tanner":
        msg = '''
    Each day, the tanner can disguise three players
    the night after, to roles like the fortune teller, the crowd seeker and the warlock, their roles will appear to be what the tanner has disguised the players as. The tanner may disguise themselves.

    Disguising players is an immediate effect.

    If the tanner dies, the assigned players will keep their disguises. All players lose their disguise at the end of the night.

    The tanner does not appear as a threat to the aura teller.

    If the look - alike copies the tanner, then the tanners won't join. The look-alike will know the tanner's role, of course, but the original tanner won't know the look-alike's.

    The infected wolf can turn the tanner into a werewolf.

    If the tanner turns undead, they will lose all their powers.

    '''
    if role == "Warlock":
        msg = '''
    The warlock is the corrupted version of a fortune teller. Each night, they can inspect a player, and they will learn what their role is
    however, it is the warlock's goal to survive with all the werewolves.

    Inspecting a player is an immediate effect.

    The warlock does not appear as a threat to the aura teller.

    If the look - alike copies the warlock, then the priests won't join. The look-alike will know the warlock's role, of course, but the original warlock won't know the look-alike's.

    The infected wolf can turn the warlock into a werewolf.

    The warlock's powers are influenced by the flute player; if they're enchanted, and there's still a flute player alive, inspecting a player has a 60\% chance of displaying them as a flute player, and a 40\% chance of displaying them as their actual role(or at least the role that the tanner gave them).

    If the warlock turns undead, they will lose all their powers.

    '''
    if role == "White Werewolf":
        msg = '''
    To the werewolves, the white werewolf will appear to be a regular werewolf. However, it is the white werewolf's goal to win the game completely alone
    even the other werewolves must die. This is a difficult but very enjoyable role to play.

    Killing a werewolf is an end effect.

    If the werewolves' win condition is reached before the white werewolf could kill them all, then the werewolves win and the white werewolf loses. This is the case when all the innocents are dead before the werewolves are. It is the white werewolves' task to kill the werewolves off before all non - werewolves are dead.

    The white werewolf appears as a threat to the aura teller.

    If the look - alike copies a white werewolf, they will be added to the wolf pack, but their role will not be revealed, for obvious reasons.

    The infected wolf can turn the white werewolf into a werewolf.

    If the white werewolf turns undead, they will no longer be able to kill a werewolf every other night, but they will keep access to the wolf pack. The werewolves will still be able to kill a player every other night, until all the werewolves are either dead or undead.

    '''
    if role == "Wolf's Cub":
        msg = '''
    Whenever this werewolf dies, the other werewolves will be able to kill a second player in one night. They are allowed to attack the same player twice, if they like. This is useful in scenarios where the werewolves want to kill runners or players who may have been demonized.

    The wolf's cub appears as a threat to the aura teller.

    If the look - alike copies a wolf's cub, they will be added to the wolf pack, but their role will not be revealed
    after all, they might as well have copied the white werewolf...

    The infected wolf can turn the wolf's cub into a werewolf.

    If the wolf's cub turns undead, the werewolves will no longer get to kill a second player when the wolf's cub dies. However, the undead wolf's cub will keep access to the wolf pack. The werewolves will still be able to kill a player every night, until all werewolves are either dead or undead.

    '''

    # Solo Teams

    if role == "Angel":
        msg = '''
    The angel's only go is to die during the first lynch, which happens on the second day. If this doesn't happen, the angel will turn into a regular innocent.

    If the Angel dies the night before the first lynch, then the Angel does not win.

    If the cupid falls in love with the angel, and the angel is killed on the first day, then both the angel and their lover win the game.

    If the look-alike copies the angel, then the angels won't join. The look-alike will know the angel's role, of course, but the original angel won't know the look-alike's.

    The infected wolf can turn the angel into a werewolf.

    If the Angel turns undead, they will no longer win if they die during the first lynch.

    '''
    if role == "Despot":
        msg = '''
    If the despot is chosen Mayor, and they survive for three consecutive nights, then the despot wins.

    If the look-alike copies the despot, then the despots won't join. The look-alike will know the despot's role, of course, but the original despot won't know the look-alike's.

    If the cupid falls in love with the cupid, they will win the game if either all other players are dead, or if the despot has reached their win condition.

    The infected wolf can turn the despot into a werewolf.

    '''
    if role == "Devil":
        msg = '''
    Each night, the devil may choose a player to send the Devil's Wager to. The Devil's Wager means that the player is given the following choice; the player can either learn another player's role, or they can kill another player - but sell their soul in the process.

    If the player chooses to see another player's role, it will work like the fortune teller powers; effects like the flute player's and the tanner's still apply. These effects are seen from the player's perspective, not the devil's; the flute player powers apply if the chosen player is enchanted, not when the devil is enchanted. If the player attempts to learn the devil's role, it will show them they're a regular innocent.

    If the player chooses to kill another player, then they will become a **soulless one**. All normal rules like the end condition and your team still apply, but the Devil can no longer target a soulless one to give them the Devil's Wager. The person the soulless one chooses to kill, dies at the end of the night, though normal effects like the sacred wolf, the Amulet of Protection and being demonized still applies. The two exceptions are that killing the Devil always fails, and the Devil **is** able to kill the Immortal if they receive a soul in return.

    The Devil can use a soul to either protect themselves or a soulless one, or they can use it to kill a player (either soulless or not). If all other players are either soulless ones or dead, the Devil wins.

    If the cupid chooses to fall in love with the Devil, they will both fall in love and turn into a demon. If the lover dies, the Devil commits suicide, regardless of how many souls they had to save thsemselves.

    If the look-alike attempts to copy the Devil, they will turn into a demon instead of the Devil.

    The infected wolf cannot turn the Devil into a werewolf. Instead, the infected wolf turns into a demon.

    '''
    if role == "Demon":
        msg = '''
    The Demon is a rare role that is theoretically possible to gain, but should seldom appear in games. A Demon is like the Undead, though their leader is not the vampire, but the Devil himself. Their win condition is the same as the Devil's.

    If the look-alike copies a demon, they will turn into a demon as well. They will join forces.

    The infected wolf cannot turn the Demon into a werewolf. Instead, the infected wolf turns into a demon as well.

    '''
    if role == "Flute Player":
        msg = '''
    Each night, the flute player can choose one player, who will be enchanted. If all living players but the flute player(s) are enchanted, the flute player wins.

    Whenever a player is enchanted, they will know the other enchanted players. If an enchanted player is a fortune teller, crowd seeker or warlock, their powers will also be influenced. Whenever they attempt to inspect/seek a player, they will have a 60\% chance that the player is displayed as the fortune teller, and a 40\% chance that they are be displayed as their actual role (or the role the tanner has disguised them as). This effect will disappear once all the flute players are dead.

    Enchanting a player is an immediate effect.

    If there are multiple flute players, then they are one team, and they will work together. Each flute player will be able to enchant one player.

    If there's only one flute player, then they will be able to enchant two players at night. This also counts when a flute player is the only flute player left alive.

    If the look-alike copies the flute player, then he will join the flute player team, and help the others enchant the town.

    The infected wolf can turn the flute player into a werewolf.

    If the flute player turns undead, they will only be able to enchant a player if there's still another flute player alive. If all flute players are either dead or undead, then the undead flute players will lose their powers.

    '''
    if role == "Four Horsemen":
        msg = '''
    The Four Horsemen are four players. They do not know each other, but they each gain a list with 5 random players, of which one is another Horseman. Every night, one Horseman may choose a player to kill. This means that each Horseman individually may choose one player every four nights to kill. If the Horseman attempts to kill another Horseman, the kill will be prevented, and the two Horsemen unite. When all four Horseman are united, they will unleash Doomsday. Once Doomsday has been revealed, all Horsemen will be able to kill one player per night. They can also no longer be killed during the night.

    Doomsday can still be unleashed when a horseman is dead. If all players that were on the list with the dead horseman on it, are dead, then the horseman will count as united, allowing the other horsemen to unleased a -possibly delayed- Doomsday.

    The infected wolf can only turn a horseman if they weren't united yet. If they are united, then the horseman will merely pretend to have turned into a werewolf, while they remain a horseman.

    '''
    if role == "Ice King":
        msg = '''
    Each night, the Ice King can submit a list of players; they can guess the roles of as many players as they want. If they have submitted all their guesses, and all guesses are correct, then all guessed players will be frozen. They can no longer talk in any chat, nor can they participate in the voting. If all players but the Ice King are frozen, the Ice King wins.

    When the Ice King dies, all frozen players will be unfrozen and able to talk again. Frozen players can also be unfrozen by the Innkeeper.

    If the look-alike copies the Ice King, they will join forces, and each be able to submit a list.

    The infected wolf can turn the Ice King into a werewolf. If any frozen players are left, they will remain frozen, even if the Ice King dies. Sucks to be them, I guess.

    If the Ice King turns undead, all frozen players will be unfrozen once the undead Ice King finally dies. However, the Ice King can no longer freeze other players.

    '''
    if role == "Immortal":
        msg = '''
    The Immortal cannot die in any way. They cannot be killed by the werewolves, the cult or the barber. The only way the Immortal dies, is when the daily death poll votes unanimously to kill the Immortal. That does not mean that everyone has to vote for the Immortal, it simply means that no-one must vote for anyone else.

    If the Immortal gets chosen to be Mayor, then the Immortal dies as well. If a player sells their soul to the Devil and chooses to kill the Immortal, then the Immortal dies as well. During votes, the Immortal's vote counts thrice.

    The cupid cannot vote to kill their lover, naturally, which means that the immortal cannot die, as long as their lover votes for someone else. However, the immortal will commit suicide if their lover dies.

    If the look-alike copies the Immortal, then the Immortals do not join forces. Instead, they will need to kill each other.

    The infected wolf can turn the immortal into a werewolf. They will lose their immortal powers, and continue the game as a regular (mortal) wolf.

    '''
    if role == "Psychopath":
        msg = '''
    At the start of the game, the psychopath is being given a list with half the town's population on it. If all players on that list are dead, the psychopath wins.

    Naturally, the psychopath must still be alive when everyone on the list is dead.

    If the Look-Alike becomes the psychopath, then the two psychopaths will get to learn about each other and they will share their win condition. If the look-alike was originally on the psychopath's list, they will be removed.

    The infected wolf can turn the psychopath into a werewolf.

    If the psychopath turns undead, they will lose their original win condition.

    '''
    if role == "Pyromancer":
        msg = '''
    Every night, the pyromancer may choose to powder a player, or to ignite all powdered players. All ignited players are being killed. Effects like the Amulet of Protection, the vampire's bite and the Sacred Wolf powers still apply. However, if a powdered player doesn't die, they will remain powdered. The Pyromancer wins the game when all other players are dead.

    If the look-alike becomes the pyromancer, then the two pyromancers will get to learn about each other and they will share their win condition.

    '''
    if role == "The Thing":
        msg = '''
    Every night, The Thing may choose to abduct up to 5 players into his swamp. Whilst in the swamp, players get no contact with the outside world through either the Conspiracy Channels, Public Channels, or Secret Channels. The Thing is also in the swamp, however, nobody knows who is abducted and who is The Thing. Every night in the swamp, there is a poll held to kill a member of the swamp, with the goal being to kill The Thing. Once The Thing is dead, all players are released from the swamp. If The Thing kills all participants of the swamp except himself, he may abduct a new group of up to five players.

    The Thing can also kill one player in The Swamp each night, and knows the role of all the players in The Swamp.

    Players in the swamp are immune to any action used upon them.
    Players in the swamp cannot use their powers.

    The Thing's win condition is to kill all other players.

    '''
    if role == "Undead":
        msg = '''
    If a demonized player dies during the night, they will lose their original role and become an Undead. They are now part of the Vampire's team, and they have the same win condition as the Vampire; they will win once all players are either Vampire, Dead or Undead.

    The Undead is one of the most complex roles in the game. The Undead is a dead player who pretends to be alive. Their previous role has fallen, but as long as they have someone to leech their old role from, they will still keep the role's properties.

    The look-alike isn\'t supposed to be able to copy the Undead. May this ever happen in the future, then the look-alike will be told to choose again. They copy the role and become demonized, however.

    The infected wolf cannot turn the undead into a werewolf. The undead counts as a dead player. As the undead usually does, they only pretend to have a certain role. The infected player will pretend like they have turned into a werewolf, while secretly, they remain undead.

    The Undead cannot be demonized again.

    '''
    if role == "Vampire":
        msg = '''
    Each night, the Vampire can demonize a player. The target will not know about it by that time. When a demonized player dies, they will turn into an Undead. The Vampire wins the game, along with the Undead, if all players are either Vampire, Dead or Undead.

    Demonizing a player is an immediate effect.

    If the look-alike copies the vampire, then they will join forces and work together.

    The infected wolf cannot turn the vampire into a werewolf. The vampire counts as a dead player. The Vampire will join the wolves' ranks, but they will only pretend to be a werewolf; secretly, they remain a vampire.

    The vampire cannot be demonized.

    '''
    if role == "Zombie":
        msg = '''
    Zombies are not allowed to talk throughout the game, except for in their zombie channel. Each night, the Zombie may bite a player. When a player has been bitten twice, they will turn into a zombie as well. However, they will also die if their murderer gets bitten. Notice how this forms a chain; all zombies can be killed instantly when the original zombie dies.

    A zombie does not need to bite a player two times in a row; even further, a player can get bitten once and much later on in the game get bitten by a second player. Whoever bites the zombie the second time, will become the player's "mother".

    Biting is an immediate effect, though it takes a whole night; a player getting bitten by multiple zombies counts as one bite, which means that you can\'t turn a player into a zombie instantly. If a player turns into a zombie, they do turn instantly.

    '''

    return msg
