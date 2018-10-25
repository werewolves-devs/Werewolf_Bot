import re
from typing import List, Optional

from discord import Message, User, Embed

from config import ghost_prefix as prefix
from interpretation import check
from main_classes import Mailbox
from management.db import isParticipant
from management.general import get_credits, get_user, gen_get
from management.profile import ProfileModel


def is_command(message, commandtable, help=False):
    return check.is_command(message, commandtable, help, prefix)


def set_age(message: Message) -> List[Mailbox]:
    _, *params = message.content.split(' ')
    if len(params) == 0:
        return [Mailbox().respond("Invalid arguments. Please check the help.", temporary=True)]
    new_age, *_ = params  # because im too cool for params[0] ~ roman
    if not new_age.isdigit():
        return [Mailbox().respond('Sorry bro, only positive whole numbers', temporary=True)]
    new_age = int(new_age)
    if new_age > 2 ** 31 - 1:
        if new_age > 15556000000:
            return [Mailbox().respond(
                "You sure, bud? That\'s older than the universe. Time wasn\'t "
                "a thing back then. ...there is no such thing as a **BEFORE** the Big Bang.",
                True)]
        if new_age > 4560000000:
            return [Mailbox().respond("Yeah, sure thing! The creation of our planet must\'ve been enjoyable to watch.",
                                      True)]
        return [Mailbox().respond(f"Bruh, I know yo momma's as heavy as Mother Earth, "
                                  f"but that doesn't make you as old as her.", temporary=True)]
    profile = ProfileModel.get_or_insert(message.author)
    profile.age = new_age
    profile.save()
    return [Mailbox().respond("Updated your profile!")]


def set_gender(message: Message) -> List[Mailbox]:
    _, gender = re.split(r'\s+', message.content, 1)
    if len(gender) >= 255:
        return [Mailbox().respond(
            "Invalid gender. If you really need more than 255 chars to express your gender, contact a GM",
            temporary=True)]
    profile = ProfileModel.get_or_insert(message.author)
    if gender.lower().startswith('m'):
        profile.gender = 'Male'
    elif gender.lower().startswith('f'):
        profile.gender = 'Female'
    elif gender.lower().startswith('r'):
        profile.gender = 'Randium'
    else:
        profile.gender = 'Other'
    profile.save()
    return [Mailbox().respond("Updated your profile!")]


def set_bio(message: Message):
    _, bio = re.split(r'\s+', message.content, 1)
    profile = ProfileModel.get_or_insert(message.author)
    profile.bio = bio
    profile.save()
    return [Mailbox().respond("Updated your profile!")]


def view_profile(message: Message):
    users = check.users(message, amount=1, delete_duplicates=True, must_be_participant=False)
    user: User = message.author
    if users:
        if isParticipant(message.author.id) and not isParticipant(users[0]):
            return [Mailbox().respond("I am sorry! To prevent any accidental spoilers, you cannot view the profile of dead players.",True)]
        user = message.channel.guild.get_member(users[0])
    model = ProfileModel.get_or_insert(user)
    em = Embed(
        title=f'Profile of {user.display_name}',
        description=model.bio,
    )
    em.set_author(name=user.display_name, icon_url=user.avatar_url)
    em.add_field(name="Age", value=str(model.display_age))
    em.add_field(name="Gender", value=model.gender)
    em.add_field(name="Credits", value=get_credits(user.id))
    em.add_field(name="Referral score", value=gen_get(user.id,'refer_score'))
    if get_user(user.id)[4] > 0:
        em.add_field(name="Roulette Highscore", value=get_user(user.id)[4])
    return [Mailbox().embed(em, destination=message.channel.id, temporary=True)]


def process_profile(message: Message, is_game_master, is_admin, is_peasant) -> Optional[List[Mailbox]]:
    if is_command(message, ['age', 'setage'], help=True):
        return [Mailbox().respond("Use this command to set your age in your profile", temporary=True)]
    if is_command(message, ['age', 'setage']):
        return set_age(message)

    if is_command(message, ['gender', 'setgender'], help=True):
        return [Mailbox().respond("Use this command to set your gender in your profile. We left it free to fill "
                                  "anything in, but if this gets abused ya getting whipped!", temporary=True)]
    if is_command(message, ['gender', 'setgender']):
        return set_gender(message)

    if is_command(message, ['setbio', 'bio'], help=True):
        return [Mailbox().respond("Use this command to set your biography in your profile.", temporary=True)]
    if is_command(message, ['setbio', 'bio']):
        return set_bio(message)

    if is_command(message, ['profile', 'view_profile'], help=True):
        return [Mailbox().respond("Use this command to view your or other peoples profile.", temporary=True)]
    if is_command(message, ['profile', 'view_profile']):
        return view_profile(message)
    return None
