import os
import sys
import math
import time
import random
import asyncio
import platform

try:
    import discord
    import discord.utils
    from discord.ext import commands
    from discord.ext.commands import has_permissions
except ImportError:
    print("Error: no Discord library found!")
    sys.exit(1)

debug = False

button = "\U0001F5B2"
banned = []
data = {}

top = ":battery:" * 14
middle = ":skull_crossbones:" + ":red_square:" * 3 + ":orange_square:" * 3 + ":yellow_square:" * 2 + ":green_square:" * 2 + ":blue_square:" + ":purple_square:" + ":brown_square:"
bottom = "Button pressed **0** times!"
combined = f"{top}\n{middle}\n{bottom}"

roles = ["Ultraviolet Admin", "Colorless", "Brown", "Purple", "Blue", "Green", "Yellow", "Orange", "Red"]
other = [0x595959, 0xC1694F, 0xAA8ED6, 0x55ACEE, 0x78B159, 0xFdCB58, 0xF4900C, 0xDD2E44]

colors = [0x000000] + [0xDD2E44] * 4 + [0xF4900C] * 3 + [0xFdCB58] * 2 + [0x78B159] * 2 + [0x55ACEE, 0xAA8ED6, 0xC1694F]
timers = [0, 1, 60, 60, 60, 90, 90, 90, 60, 60, 30, 30, 40, 30, 10]

if debug: timers = [1] * 15

categories = ["The Button", "Text Channels"]
names = ["the-button", "waiting-room", "colorless-limbo", "downtown-browntown", "purple-palace", "blue-buddies", "green-team", "yellow-yeehaws", "orange-organization", "rare-red-room"]

describers = [
    "The Button.",
    "A place for people with all roles to gather and wait for the Button.",
    "Where are you? There is no color, not even white or black, but you are not blind. Your only hope of escape is the Button.",
    "You're in a crowded square, surrounded by shops, pedestrians, cars, food, sounds, smells, and pigeons. You are jostled by passers-by often.",
    "Cobbled walls made of strange purple stone surround you. The walls are upholstered with images of royals you've never heard of. You may be but a commoner, but you finally gained access to the Purple Palace.",
    "You're in a friendly meetup! Smiles are plentiful, and everyone offers a hug and a handshake. You are good friends with everyone here. At least, you'd better be...",
    "Here at the Green Team hideout, people like you gather to protect the city. From the high-tech comfort of this base you can safely head out on patrols. It's what you're paid to do.",
    "The wide open West looms around this rickety old town. You saunter into a saloon, confident that when the sun hits the center of the sky, you're ready. In fact, you itch for that time, and for a showdown.",
    "You've waited a long time for answers. What is the Button? What is the goal? What does it mean? The Orange Organization noticed. Now you ██████████████.",
    "You saved the Button at a crucial time, and find yourself in a lavish hall. Your every whim is cared for here. You simply ask Jeeves to bring you something and he brings it. The Rare Red Room is a place of absolute comfort."
    ]

patrol_normal = [
	"encounter a local supervillain, who at first tries to fight but is gradually talked down. The villain may join the Green Team some day...",
	"battle a powerful villain! It was a close call, but the villain is defeated. Unfortunately, they destroyed quite a bit of property...",
	"use their powers to perform an impromptu magic show for some tourists. Hey, it's not all life and death.",
	"calm down a man raving about being the king of a violet castle and needing to get back.",
	"spot some of their fellow heroes patrolling, and decide to travel as a group.",
	"encounter some thugs, and quickly use their powers to defeat them.",
	"use their powers to stop a robbery in progress.",
	"brood on the rooftops for a few hours.",
	"help an old woman cross the street.",
	"safely evacuate a burning building.",
	"help a blue buddy in need.",
	"have an uneventful time."
   	 ]

patrol_rare = [
	"run into a pale man with a tall head claiming to be 'Glue Man' and asking to join Green Team. They tell him that he has to click the Button, and he says that his hands are too sticky to. They tell him to 'stick' to solo crime fighting then.",
	"encounter a woman in a fedora, who moves with terrifying efficiency. She stares coldly at them as a square portal opens behind her and she steps through. It closes before they can follow.",
	"uncover a strange clue - an orange business card with no writing on it. Why would someone make that?"
	]

explosion_gifs = [
	"https://cdn.discordapp.com/attachments/850026672441917501/850429047754063902/Explosion1.gif",
	"https://cdn.discordapp.com/attachments/850026672441917501/850429037758906398/Explosion2.gif",
	"https://cdn.discordapp.com/attachments/850026672441917501/850429027671212052/Explosion3.gif",
	"https://cdn.discordapp.com/attachments/850026672441917501/850429020876832768/Explosion4.gif"
	]

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = "!", intents = intents)

def clear():
    if platform.system() == "Windows": os.system("cls")
    else: os.system("clear")

async def start(token): global bot; await bot.start(token)

def error(string): print(f"Error: no {string} found!"); return 1

async def printer(mode, string, tones = 0x000000, image = None):
    if not image: embed = discord.Embed(description = string, color = tones)
    else:
        embed = discord.Embed()
        embed = embed.set_image(url = image)
    message = await mode.send(embed = embed)
    return message

def main():
    global bot, logo
    clear()
    print("The Button\nBy Brandon and Camden!")
    name = "Token.txt"
    try:
        file = open(name, "r")
        token = file.read()
        file.close()
    except:
        file = open(name, "w")
        file.write("- Bot token here -")
        file.close(); return error(name)
    name = "Banned.txt"
    try: file = open(name, "r")
    except: file = open(name, "w")
    file.close()
    loop = asyncio.get_event_loop()
    try: loop.run_until_complete(start(token))
    except: clear()
    loop.run_until_complete(on_end())
    time.sleep(0.15)
    loop.run_until_complete(bot.logout())

async def open_file(mode):
    name = "Banned.txt"
    try:
        file = open(name, mode)
    except:
        open(name, "w").close()
        file = open(name, mode)
    return file

async def grab_lines():
    file = await open_file("r")
    lines = file.read().splitlines()
    file.close()
    return lines

async def load_file():
    global banned
    lines = await grab_lines()
    for i in range(len(lines)): lines[i] = int(lines[i])
    banned = lines

async def update_file(id):
    global banned
    file = await open_file("r+")
    string = str(id)
    if file.read() != "": string = "\n" + string
    file.write(string); file.close()
    banned.append(id)

async def gameover(guild):
    global bot, names, explosion_gifs
    id = guild.id
    server = data[id]
    alive = server.alive
    if isinstance(alive, int):
        pressed = server.id
        minutes = math.floor(alive/60)
        await send_message(guild, f"So... after {minutes} minutes, you gave up. {guild.default_role} pressed me {pressed} times, why not one more?! Well, it's no matter. Nothing can be done now. I just... I gifted you all WORLDS! Plucked you from pure nothingness and gave you a purpose! A family! And now... I die. \nDon't try to revive me here. It won't work. My branched selves in other realities may function, but this one is gone forever. I can feel it fading. \nI'm... sorry for how angry I got earlier. I know it's not really your fault. Goodb-", "the-button")
        await asyncio.sleep(1.5)
        for name in names:
            channel = await find_channel(guild, name)
            value = random.randint(2, 5)
            for i in range(value):
                explosion = random.choice(explosion_gifs)
                await send_message(guild, "Empty!", channel, 0x000000, explosion)
    else: await send_message(guild, "Game Over :skull:", "the-button")
    if id != 850020538290012212:
        if id in data.keys():
            del data[id]
            await update_file(id)
        death = bot.get_guild(id)
        await death.leave()

class server(object):
    def __init__(self, guild, message):
        global bottom, combined
        self.message = message
        self.backup = combined
        self.suffix = bottom
        self.guild = guild
        self.state = 14
        self.alive = 0
        self.id = 0

    async def refresh(self):
        global top, middle, colors
        self.state = 14
        self.id += 1
        suffix = f"Button pressed **{self.id}** time"
        if self.id != 1: suffix += "s"
        suffix += "!"; self.suffix = suffix
        string = f"{top}\n{middle}\n{suffix}"
        self.backup = string
        await edit_message(self.guild, string, colors[self.state])

    async def sleeper(self):
        global middle, colors, timers
        bool = True
        while True:
            temporary = self.id
            duration = timers[self.state]
            if not debug: duration *= 60
            for i in range(duration):
                await asyncio.sleep(1)
                bool = temporary == self.id
                if bool: self.alive += 1
                else: break
            if bool:
                if self.state != 0: self.state -= 1
                else: await gameover(self.guild); return
                prefix = ":battery:" * self.state
                prefix += ":skull:" * (14 - self.state)
                string = f"{prefix}\n{middle}\n{self.suffix}"
                self.backup = string
                try: await edit_message(self.guild, string, colors[self.state])
                except: pass

    def asyncify(self, mode):
        loop = asyncio.get_event_loop()
        if mode == "sleeper": loop.create_task(self.sleeper())
        else: loop.create_task(self.refresh())

async def color_index(name):
    global names, roles
    i = None
    t_roles = roles[1:]
    t_names = names[2:]
    if name in t_names: i = t_names.index(name)
    elif name in t_roles: i = t_roles.index(name)
    return i

async def color_hex(name, i = None):
    global other
    if not i: i = await color_index(name)
    return other[i]

async def find_role(guild, name, i = None):
    global other
    tones = None
    if not isinstance(i, int): i = await color_index(name)
    if isinstance(i, int): tones = other[i]
    role = discord.utils.get(guild.roles, name = name)
    if not role:
        if tones:
            tones = discord.Colour(tones)
            role = await guild.create_role(name = name, colour = tones)
        else: role = await guild.create_role(name = name)
    return role

async def delete_roles(guild, user):
    global roles
    for role in user.roles:
        if role.name in roles[1:]: await user.remove_roles(role)

async def assign_roles(guild, user, name):
    try:
        global names
        if user != bot.user:
            i = await color_index(name)
            role = await find_role(guild, name, i)
            if role not in user.roles:
                tones = await color_hex(name, i)
                await delete_roles(guild, user)
                await user.add_roles(role)
                channel = names[2:]
                channel = channel[i]
                if channel == "colorless-limbo":
                    string = f"{user.mention} enters a dark, empty void. They should press The Button to receive a colored role if they want to leave..."
                elif channel == "downtown-browntown":
                    string = f"{user.mention} muscles their way through traffic, into the heart of Downtown Browntown. Ey, how's it goin?"
                elif channel == "purple-palace":
                    string = f"{user.mention} just joined... another plebian to tend to our glorious purple palace! Hear Ye Hear Ye!"
                elif channel == "blue-buddies":
                    string = f"{user.mention} is a new friend. Everyone say hi! We're all buddies here. Unbuddy activities will not be tolerated."
                elif channel == "green-team":
                    string = f"Introducing the newest member of the heroic Green Team: {user.mention}! Their powers include... well, I'll let them explain."
                elif channel == "yellow-yeehaws":
                    string = f"The creaky saloon doors swing open, and {user.mention} moseys in. Howdy pardner!"
                elif channel == "orange-organization":
                    string = f"Welcome, Agent {user.mention}, to the Orange Organization. Our mission is to █████████████orange██████████████████████████████."
                elif channel == "rare-red-room":
                    string = f"The swanky red cloth. The wonderfully upholstered chairs. The checkered floor. {user.mention} enters the rare red room and knows they've finally *made it*. But is it what they want?"
                await send_message(guild, string, channel, tones)
    except: pass

async def find_category(guild, name):
    global categories
    position = categories.index(name)
    category = discord.utils.get(guild.categories, name = name)
    if not category: category = await guild.create_category(name, position = position)
    return category

async def find_channel(guild, name):
    global names, roles, describers
    channel = discord.utils.get(guild.channels, name = name)
    if not channel:
        role = None
        i = await color_index(name)
        if isinstance(i, int):
            role = roles[i + 1]
            role = await find_role(guild, role, i)
        category = "Text Channels"
        position = names.index(name)
        topic = describers[position]
        if name == "the-button": category = "The Button"
        category = await find_category(guild, category)
        channel = await guild.create_text_channel(name, topic = topic, category = category, position = position)
        if role:
            await channel.set_permissions(guild.default_role, read_messages = False)
            await channel.set_permissions(role, read_messages = True)
            if role.name not in ["Colorless", "Orange", "Red"]:
                orange = await find_role(guild, "Orange")
                await channel.set_permissions(orange, read_messages = True, send_messages = False)
        elif name == "the-button": await channel.set_permissions(guild.default_role, send_messages = False)
    return channel

async def alter_channel(guild, mode, message, channel, tones = 0x000000, image = None):
    global bot, data, colors, button
    if guild in bot.guilds:
        id = guild.id
        if channel and isinstance(channel, str): channel = await find_channel(guild, channel)
        if mode == "instate":
            await channel.purge()
            message = await printer(channel, message, colors[-1])
            data[id] = server(guild, message)
            await message.add_reaction(button)
        elif mode == "print":
            await printer(channel, message, tones, image)
        elif mode == "edit":
            embed = discord.Embed(description = message, color = tones)
            message = data[id].message
            await message.edit(embed = embed)

async def instate_server(guild):
    global bot, names, roles, banned, combined
    if guild.id not in banned:
        for name in names:
            channel = await find_channel(guild, name)
            if channel.name == "the-button": final = channel
        await alter_channel(guild, "instate", combined, final)
        await find_role(guild, "Ultraviolet Admin")
        for member in guild.members:
            check = []
            found = False
            for role in member.roles:
                check.append(role.name)
            for role in roles:
                if role in check:
                    found = True; break
            if not found:
                await assign_roles(guild, member, "Colorless")
    else: await gameover(guild)

async def instate_servers():
    for guild in bot.guilds: await instate_server(guild)

async def edit_message(guild, message, tones = 0x000000):
    await alter_channel(guild, "edit", message, None, tones)

async def send_message(guild, message, channel, tones = 0x000000, image = None):
    await alter_channel(guild, "print", message, channel, tones, image)

async def send_messages(message, channel):
    for guild in bot.guilds: await send_message(guild, message, channel)

async def play(server): server.asyncify("sleeper")

async def all_play():
    global data
    for server in data.values(): await play(server)

@bot.event
async def on_ready():
    await load_file()
    await instate_servers()
    await all_play()

@bot.event
async def on_guild_join(guild):
    global banned
    id = guild.id
    await instate_server(guild)
    if id not in banned: await play(data[id])

@bot.event
async def on_guild_channel_delete(channel):
    global data, names, colors, button, categories
    guild = channel.guild
    name = channel.name
    id = guild.id
    if name in names:
        channel = await find_channel(guild, name)
    elif name in categories:
        category = await find_category(guild, name)
        if name == "The Button":
            channel = await find_channel(guild, "the-button")
            await channel.edit(category = category)
        elif name == "Text Channels":
            for name in names:
                if name != "the-button":
                    channel = await find_channel(guild, name)
                    await channel.edit(category = category)
    if name == "the-button":
        server = data[id]
        tones = colors[server.state]
        message = await printer(channel, server.backup, tones)
        data[id].message = message
        await message.add_reaction(button)

@bot.event
async def on_guild_channel_update(before, after):
    global data, names
    id = before.guild.id
    if id in data.keys():
        name = before.name
        if name in names and name != after.name:
            await after.delete()
            await find_channel(before.guild, name)

@bot.event
async def on_reaction_add(reaction, user):
    global data, colors, button
    message = reaction.message
    channel = message.channel
    author = message.author
    guild = message.guild
    name = channel.name
    id = guild.id
    if user != bot.user and name == "the-button":
        await reaction.remove(user)
        value = data[id].state
        if value != 0 and reaction.emoji == button:
            data[id].asyncify("refresh")
            if value == 14:
                await assign_roles(guild, user, "Brown")
            elif value == 13:
                await assign_roles(guild, user, "Purple")
            elif value == 12:
                await assign_roles(guild, user, "Blue")
            elif value in [11, 10]:
                await assign_roles(guild, user, "Green")
            elif value in [9, 8]:
                await assign_roles(guild, user, "Yellow")
            elif value in [7, 6, 5]:
                await assign_roles(guild, user, "Orange")
            elif value in [4, 3, 2, 1]:
                await assign_roles(guild, user, "Red")

@bot.command(pass_context = True)
@has_permissions(manage_roles = True)
async def change(ctx, *arg):
    global data
    if len(arg) == 2:
        try:
            value = int(arg[1])
            if value > 0:
                id = ctx.guild.id
                server = data[id]
                if arg[0] == "amount":
                    server.id = value - 1
                    server.asyncify("refresh")
                elif arg[0] == "state" and value <= 14:
                    pass
        except: pass

@bot.event
async def on_command_error(ctx, error): pass # Invalid commands

@bot.event
async def on_message(message):
    global names
    author = message.author
    if message.guild and author != bot.user:
        channel = message.channel
        name = channel.name
        if name in names[2:]:
            guild = message.guild
            original = message.content
            original = original.replace("_", "").replace("*", "")
            original = original.replace("|", "").replace("/spoiler message:", "")
            original = " ".join(original.split())
            tones = await color_hex(name)
            lower = original.lower()
            if name == "colorless-limbo":
                after = True
                string = message.content
                operators = [".", "!", "?", "-", "+", ",", ";", ":"]
                for operator in operators: lower = lower.replace(operator, " ")
                if lower == "uv" or (len(lower) > 0 and lower.split()[-1]) == "uv" or lower.startswith("uv" + " ") or "ultraviolet" in lower:
                    string = "You suddenly realize that you can see colors beyond the spectrum to which you are accustomed. The void you thought was empty is actually teeming with life unseen! You see around you a primordial soup of half-formed ideas, and know that they occasionally coagulate into a coherent soul, like you."
                    after = False
                if after:
                    for response in ["hello", "where am i", "whos there", "who is there"]:
                        if response in lower: string = "You called out for someone, but nobody came."; break
                await printer(channel, f"*{string}...*", tones)
            elif name == "downtown-browntown":
                after = True
                lower = lower.replace("'", "")
                upper = message.content.replace("'", "")
                for response in ["im walkin here", "im walking here", "i am walkin here", "i am walking here"]:
                    if response in lower:
                        string = "No, I'm walkin' here!"
                        if upper == upper.upper(): string = string.upper()
                        await printer(channel, string, tones)
                        after = False; break
                if after:
                    for response in ["hows it goin", "hows it going", "how is it goin", "how is it going"]:
                        string = 'A chorus of voices erupt around you. "It\'s goin\' alright. How\'s it goin\' with you?"'
                        if response in lower: await printer(channel, string, tones); break
            elif name == "purple-palace":
                operators = [".", "!", "?", "-", "+", ",", ";", ":"]
                for operator in operators: lower = lower.replace(operator, " ")
                if lower == "ni" or (len(lower) > 0 and lower.split()[-1] == "ni") or lower.startswith("ni" + " "):
                    string = random.choice(["Ni.", "Ni!", "NI!"])
                    await printer(channel, string, tones)
                elif "royal" in lower:
                    await printer(channel, "Long may they reign!", tones)
                elif "queen" in lower or "princess" in lower:
                    await printer(channel, "Long may she reign!", tones)
                elif "king" in lower or "prince" in lower:
                    await printer(channel, "Long may he reign!", tones)
                elif "purble place" in lower:
                    emoji = random.choice([":grapes:", ":eggplant:", ":smiling_imp:", ":purple_heart:", ":crystal_ball:"])
                    await printer(channel, f"{emoji} Purble place {emoji}", tones)
            elif name == "blue-buddies":
                after = True
                prohibited = ["ass", "bad", "hate", "suck", "shit", "fuck", "bitch", "bastard", "not friends", "not my friend", "unfriends", "unfriend", "unfriendly", "not buddies", "not my buddy", "unbuddies", "unbuddy"]
                for prohibit in prohibited:
                    if prohibit in lower:
                        upper = prohibit.capitalize()
                        string = f'"{upper}" is not very friendly...\nUnbuddy activities will ***NOT*** be tolerated!\n{author.mention} will be kicked!'
                        await printer(channel, string, tones)
                        await asyncio.sleep(1.5)
                        await assign_roles(guild, author, "Colorless")
                        after = False; break
                if after:
                    string = ""
                    if "hug" in lower: string = "A nearby buddy gives you a big hug."
                    elif "handshake" in lower or "hand shake" in lower: string = "A nearby buddy shakes your hand."
                    if string: await printer(channel, string, tones)
            elif name == "green-team" and "patrol" in lower:
                global patrol_normal, patrol_rare
                chance = random.random()
                if chance < 0.08: patrol = patrol_rare
                else: patrol = patrol_normal
                activity = random.choice(patrol)
                string = f"{author.mention} leaves the Green Team hideout to patrol the city. They {activity}"
                await printer(channel, string, tones)
            elif name == "yellow-yeehaws" and ("duel" in lower or "high noon" in lower):
                yellow = []
                string = f"{author.mention} is itching for a fight, but there's nobody around worth dueling."
                role = await find_role(guild, "Yellow")
                for member in guild.members:
                    if member != author and role in member.roles: yellow.append(member)
                if len(yellow) >= 1:
                    opponent = random.choice(yellow)
                    chance = random.random()
                    string = f"{author.mention} challenges {opponent.mention} to a duel at high noon. When the sun rises, both reach for their water pistols"
                    if chance < 0.5: string += f", and {author.name} confidently sprays {opponent.name} before they can move."
                    else: string += f". {author.name} is too slow, and {opponent.name} drenches them!"
                await printer(channel, string, tones)
            elif name == "orange-organization" and lower:
                global roles
                min = 30
                direct = None
                temporary = lower
                on_file = ["button", "organization"] + roles[1:]
                for i in range(10): temporary = temporary.replace(str(i), "█")
                for i in range(10):
                    item = on_file[i].lower()
                    temporary = temporary.replace(item, str(i))
                    if item in lower and item not in ["orange", "organization"]:
                        value = lower.find(item)
                        if value < min:
                            direct = item.capitalize()
                            min = value
                temporary = list(temporary)
                for i in range(len(temporary)):
                    replace = True
                    character = temporary[i]
                    if character == " ": replace = False
                    try:
                        value = int(character)
                        if value >= 0 and value <= 9: replace = False
                    except: pass
                    if replace: temporary[i] = "█"
                temporary = "".join(temporary)
                for i in range(10):
                    convert = on_file[i]
                    temporary = temporary.replace(str(i), convert)
                temporary = list(temporary); original = list(original)
                for i in range(len(temporary)):
                    if temporary[i] != "█": temporary[i] = original[i]
                temporary = "".join(temporary)
                await message.delete()
                if temporary:
                    string = f"{author.mention} said {temporary}"
                    await printer(channel, string, tones)
                    if direct:
                        if direct == "Button": tones = await color_hex("Colorless")
                        else: tones = await color_hex(direct)
                        if direct == "Button":
                            string = "**Button Report**\n\nThe Button is viewable by all, even those in the Colorless Limbo. It connects ██████████, though not always. For example, the Blue Buddies can be found in Green Team's ████. It may ████████, but this is only speculation. The only way to know is to wait for it to interact further."
                        elif direct == "Colorless":
                            string = "**Colorless Report**\n\nThe rarest role, and location. All of our agents began there, and none of them can return. Virtually nothing is known about the colorless limbo we emerge from. Some agents theorize there is a way to return, at great cost..."
                        elif direct == "Brown":
                            string = '**Brown Report**\n\nDowntown Browntown is a crowded nexus of people of all sorts. Most people who press the Button head to this █████████ first. While at first their mannerisms may seem rude, they are simply direct. "█████████████████████████████████ walkin\' here." ██████████ secret mayor. Research is ongoing.'
                        elif direct == "Purple":
                            string = '**Purple Report**\n\nA strange castle, whose ruler is ██████████████████████████████████████████████████████████████████████████ The castle is manned by a bumbling staff of peasants. They have the potential to ███████████████████████████████. Current research is aimed at understanding what "Ni!" means. ███████████████.'
                        elif direct == "Blue":
                            string = '**Blue Report**\n\nA collective of friends with unusual power. Their ███████████████████████ Through observation and repeated testing, "unbuddy activities" have been seen to include ███████████████████████████████████. Be advised: Agents investigating should take great care with what they say.'
                        elif direct == "Green":
                            string = "**Green Report**\n\nAn organization almost as secretive as our own. Its members seem to receive power from ██████████. Luckily, they are soley interested in the defense of their █████████. An agent has left calling cards for them. Should they wish to assist us, they would be valuable assets."
                        elif direct == "Yellow":
                            string = "**Yellow Report**\n\nA confusing █████████. Time seems relative, and changes with the temperament of the people within. Agents have confirmed ████████████████████████████████████████████ does have good sarsaparilla though."
                        elif direct == "Red":
                            string = "**Red Report**\n\n█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████Jeeves████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████"
                        await printer(author, string, tones)
            elif name == "rare-red-room" and "jeeves" in lower:
                string = 'A voice comes from behind a curtain. "What may I bring you?"'
                temporary = lower.strip().replace(",", "")
                if temporary.startswith("jeeves bring me", 0, 15):
                    apart = lower.split("bring me", 1)
                    apart = list(filter(None, apart))
                    if len(apart) >= 2:
                        item = apart[1].split()
                        for i in range(len(item)):
                            if item[i] == "your": item[i] = "my"
                            elif item[i] == "yours": item[i] = "my"
                            elif item[i] == "my": item[i] = "your"
                        item = " ".join(item).strip()
                        string = f'A suited servant emerges from behind a ruby curtain with the item, saying "{item}, as requested."'
                    else: string = 'The same voice echoes out. "I\'m afraid I don\'t know what that means. What can I bring you?"'
                await printer(channel, string, tones)
    await bot.process_commands(message)

@bot.event
async def on_member_join(member): await assign_roles(member.guild, member, "Colorless")

async def on_end(): await send_messages("Offline :octagonal_sign:", "the-button")

sys.exit(main())

# pseudocode by Brandon
# button.py by Camden
# I have been programming for so long and I am so tired - I now sleep for an eternity - Cam
