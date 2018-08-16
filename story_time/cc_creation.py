import random as randium

# Rule of thumb: the first id in the list is the conspiracy channel owner
def cc_intro(list):
    amount = len(list)
    msgtable = []

    if randium.random() < 0.01:
        msg = '''Once upon a time there was a duck. The duck pooped out an entire conspiracy channel.'''
        msgtable.append(msg)
    
    if amount == 0:
        return "That is strange... a channel with zero members?"

    if amount == 1:
        msg = '''\
This is what <@{}> was looking for... solitude. Nowhere in town could they find a place with such peace, \
but this was JUST the spot. Excellent!'''.format(list[0])
        msgtable.append(msg)

    if amount == 1:
        print(list)
        print(list[0])
        msg = '''\
Some believed the hidden room behind <@{0}>'s stairs was a silent place to take notes. \
Others thought they were just... \"testing\", whatever that may mean.
In reality, they were wrong. Only <@{0}> knew this channel\'s **TRUE** purpose...'''.format(list[0])
        msgtable.append(msg)

    if amount == 2:
        msg = '''\
It all started with a bunch of drinks at the bar, but when <@{1}> got so wasted that they could barely walk, \
<@{0}> decided to walk them home. That\'s when the two of them start talking \
about the strange events in their town...'''.format(list[0],list[1])
        msgtable.append(msg)

    if amount == 2:
        msg = '''\
"Excuse me, neighbour, but may I make use of your lavatory? Mine's a bit... occupied." \
It sounded like a not so strange request from <@{0}>, but <@{1}> understood what was going on.
"Come in," they responded. "But be careful, as some bugs seem to hear." \
<@{0}> smiled and walked inside, where they started having an interesting conversation.'''.format(list[0],list[1])
        msgtable.append(msg)

    if amount == 2:
        msg = '''\
The town square does not seem like the most ordinary way to hold a secret conversation, but both <@{0}> and <@{1}> \
were pretty good at hiding in plain sight. Even though they were among a crowd, they knew they weren't spied on.'''.format(list[0],list[1])
        msgtable.append(msg)

    if amount == 2:
        msg = '''\
<@{1}> was quite confused when they noticed their front door wasn't locked and that <@{0}> was sitting inside in the biggest chair.
*"Hello, <@{1}>,"* they said. *"I\'m gonna give you an offer you can't refuse."*
*"What do you mean,"* <@{1}> asked, being even more confused from seeing their neighbour sip out of a cup of tea.
*"Let's just say... I want to play a game."*
*"...are you making references now?"* *"Nevermind,"* <@{0}> responded quickly, *"let\'s just get down to business."*'''.format(list[0],list[1])
        msgtable.append(msg)

    if amount == 2:
        msg = '''\
**Who let the dogs out?**
<@{1}> did, and they later found out it was a smart decision after having talked to <@{0}> on their way to the forest.'''.format(list[0],list[1])
        msgtable.append(msg)

    if amount == 2:
        msg = '''\
It was at this point that <@{1}> and <@{0}> realised they were lost in the woods! \
Oh well, at least they now had a chance to discuss some secretive matters together...'''.format(list[0],list[1])
        msgtable.append(msg)

    if amount == 3:
        msg = '''\
Was it a spiritual force bringing them together? Was it a ghost haunting them to that hidden place in the forest? Neither of them knew, \
but they were all happy with <@{0}>'s decision to use the opportunity to discuss some important matters.
If they survived, <@{0}>, <@{1}> and <@{2}> could use the spot later on to have some strategical conversations.'''.format(list[0],list[1],list[2])
        msgtable.append(msg)

    if amount == 3:
        msg = '''\
It is not what <@{1}> expected when <@{0}> said they would \"put on something more comfortable\", but sure, having a conversation \
with them and <@{2}> was enjoyable as well.'''.format(list[0],list[1],list[2])
        msgtable.append(msg)

    if amount == 3:
        msg = '''\
The chess evening <@{0}> had organised wasn\'t as succesfull as they had hoped, but <@{1}> and <@{2}> did show up. \
As there was no partner for <@{1}>, they watched along with the match between <@{2}> and <@{0}>.
It was an interesting game, but it got even better when the three of them started talking...'''.format(list[0],list[1],list[2])
        msgtable.append(msg)

    if amount == 3:
        msg = '''\
Studying foreign languages had its benefits; for example, only <@{0}>, <@{1}> and <@{2}> understood the next town's odd language. \
This meant they could share anything they wanted, without a spy ever knowing what they said...'''.format(list[0],list[1],list[2])
        msgtable.append(msg)

    if amount == 4:
        msg = '''\
Though the town did not need four barbers anymore, the barber quartet <@{0}>, <@{1}>, <@{2}> and <@{3}> was \
still making the town a brighter place. It was always a happy couple on stage, but the mood had changed \
since the town was drained with blood...'''.format(list[0],list[1],list[2],list[3])
        msgtable.append(msg)

    if amount == 4:
        msg = '''\
Most of the town could handle a drink or two, but things would get really wild during a bright night. \
For example, when <@{1}> and <@{3}> were lying on the town's square, drunkenly looking into the sky, \
<@{0}> walked up to them and got them to stand in a circle around the well. <@{0}> and <@{1}> couldn't grasp \
each other's hands, so <@{2}> decided to join the group.
After running a few circles around the well, they all headed to <@{3}>'s \
basement to talk about whatever their minds would come up with.'''.format(list[0],list[1],list[2],list[3])
        msgtable.append(msg)

    if amount == 4:
        msg = '''\
From the outside, it just looked like the group that would get some berries in the wood was an innocent group \
of happy people. In reality, the gardeners <@{2}> and <@{0}>, and the berry-experts <@{1}> and <@{3}> would use \
this opportunity to have a rather difficult chat about what they could do for each other...'''.format(list[0],list[1],list[2],list[3])
        msgtable.append(msg)

    if amount == 4:
        msg = '''\
Even though the town did not know the concept of a gun, they could still have a standoff in the middle of the town's square. With bows.
*"You better start talking,"* <@{1}> said, sweat dripping from their head.
*"You first,"* <@{3}> responded, watching <@{0}> in the corner of their left eye.
*"Both of you shut up,"* said <@{2}> with a calm but dominant voice.
*"You watch your attitude, or it\'ll be your last."* <@{0}> moved their bow slowly towards <@{2}>.

They were slowly forcing each other to share information, and the spectators guessed that three of them would not survive \
the standoff. Was it all faked, however? Did they all trust each other, and were the bows merely a decoy to make sure \
no-one thought they work together?

...or maybe it was an actual standoff. That still sounds really cool.'''.format(list[0],list[1],list[2],list[3])
        msgtable.append(msg)

    if amount == 5:
        msg = '''\
<@{1}> may have been too drunk, but they all formed a great team together! <@{4}> would get the booze, \
<@{1}> would make sure <@{2}> didn't pee all over the lavatory, <@{3}> would give the moral support and \
<@{0}> would clean <@{1}>\'s vomit off of <@{3}>'s clothes.
<@{0}>, being the least drunk of \'em all, decided to start the conversation they all wished to \
start.'''.format(list[0],list[1],list[2],list[3],list[4])
        msgtable.append(msg)

    if amount == 5:
        msg = '''\
How many people fit in one lavatory if you want to say something secret? \
It seemed <@{0}>, <@{1}>, <@{2}>, <@{3}> and <@{4}> were breaking a new record without telling anyone...'''.format(list[0],list[1],list[2],list[3],list[4])
        msgtable.append(msg)

    if amount == 5:
        msg = '''\
<@{3}> was trying to drink his misery away, and as they drunkenly walked home from the tavern, <@{3}> fell into a wall - or so it seemed.\
The wall turned out to be a (magical?) curtain that looked like a wall, and <@{3}> just walked in on <@{2}>, <@{0}>, <@{4}> \
who were about to have a conversation! They couldn\'t resist keeping <@{3}> in - else they'd speak their mind for *sure*.\
 '''.format(list[0],list[1],list[2],list[3],list[4])

    if amount == 69:
        return 'Heh. Nice.'

    if msgtable == []:
        return 'Look, look, over @here! A new **conspiracy channel** has been created!'

    return msgtable[randium.randint(0,len(msgtable)-1)]

def secret_intro(role,members):
    if role == 'Assassin':
        msg = '**Hello there, {}!**\n\nThis town has been corrupted, and you can feel it! '
        msg += 'Luckily, you will put it out of its misery soon, for you shall kill all the evil ones!'
    else:
        msg = 'That is strange! Your role doesn\'t exist in my logs.... or not yet, at least.'
    return msg
