import discord
import asyncio
from discord.ext import commands
import datetime
import json
import random
import os
import math
import requests

Client = discord.Client()
client = commands.Bot(command_prefix='>')
client.remove_command('help')

#logs on discord bot
@client.event
async def on_ready():
	await client.change_presence(game=discord.Game(type=2, name='provide help in DMs'))
	print('I am logged in as ' + client.user.name + ' and connected to Gaming')

#start command for battle
@client.command(pass_context=True)
async def start(ctx):
	with open('user.json', 'r') as f:
		users = json.load(f)
	await update_data(users, ctx.message.author)
	with open('user.json', 'w') as f:
		json.dump(users, f)
		
async def update_data(users, user):
	if not user.id in users:
		embed = discord.Embed(title='A New Adventure', description='A new hero named, **{}**, has embarked on a new adventure. Will (s)he prevail or be forever lost?'.format(user.name))
		embed.set_thumbnail(url=user.avatar_url)
		await client.say(embed=embed)
		wooden_spear = users["weapon"]["Wooden Spear"]['name']
		ws_dmg = users["weapon"][wooden_spear]['dmg']
		users[user.id] = {}
		users[user.id]['weapons'] = [wooden_spear]
		users[user.id]
		users[user.id]['hp'] = 150
		users[user.id]['restart_hp'] = 150
		users[user.id]['gold'] = 0
		users[user.id]['equipped_weapon'] = {}
		users[user.id]['equipped_weapon']['name'] = wooden_spear
		users[user.id]['equipped_weapon']['dmg'] = ws_dmg
		users[user.id]['xp'] = 0
		users[user.id]['level'] = 0
		users[user.id]['xp_end'] = 1000
		
#battle command
@client.command(pass_context=True)
async def battle(ctx):
	with open('user.json', 'r') as f:
		users = json.load(f)
	r = random.randint(1, 5)
	if r == 1 or r == 2 or r == 3 or r == 4:
		await werewolf(users, ctx.message.author)
	else:
		await wyvern(users, ctx.message.author)
		
async def wyvern(users, user):
	if user.id in users:
		randomhp = random.randint(450, 1000)
		lvl_start = users[user.id]['level']
		xp_end = users[user.id]['xp_end']
		wyv = 'https://goo.gl/images/fcxmwE'
		weapon = users[user.id]['equipped_weapon']['name']
		dmg = users[user.id]['equipped_weapon']['dmg']
		enemyhp = randomhp
		maxEnemyhp = randomhp
		hp = users[user.id]['hp']
		givehp = random.randint(100, 150)
		restarthp = users[user.id]['restart_hp']
		xp = random.randint(2, 3)
		calc = 100/xp
		percent = int(calc)
		earnxp = random.randint(200, 550)
		while enemyhp > 0 and hp > 0:
			damage = random.randint(15, 30)
			embed = discord.Embed(title='A Wyvern has Appeared!', description='Type **attack** to attack it!\n**Wyvern HP**: {}/{}'.format(enemyhp, maxEnemyhp), color=discord.Colour.red())
			embed.set_author(name='HP: {}/{}'.format(hp, restarthp), icon_url=user.avatar_url)
			embed.set_footer(text='Weapon Equipped: {}'.format(weapon))
			embed.set_thumbnail(url=wyv)
			await client.say(embed=embed)
			await client.wait_for_message(author=user, content='attack')
			enemyhp -= dmg
			hp -= damage
			users[user.id]['hp'] -= damage
			with open('user.json', 'w') as f:
				json.dump(users, f)
		if enemyhp <= 0:
			users[user.id]['hp'] += givehp
			if users[user.id]['hp'] > users[user.id]['restart_hp']:
				users[user.id]['hp'] = users[user.id]['restart_hp']
			embed2 = discord.Embed(description='You earned **+{} xp**!\nType `>stats` to see how much xp you have.'.format(earnxp), color=16768768)
			embed2.set_author(name='{} has won the battle!'.format(user.name))
			embed2.set_thumbnail(url=user.avatar_url)
			users[user.id]['xp'] += earnxp
			await client.say(embed=embed2)
			if users[user.id]['xp'] >= users[user.id]['xp_end']:
				users[user.id]['level'] += 1
				users[user.id]['xp_end'] *= 4
				await client.say('**{}** has leveled up to level **{}**!'.format(users[user.id]['level']))
				users[user.id]['restart_hp'] += 50
				users[user.id]['hp'] = users[user.id]['restart_hp']
				users[user.id]['xp'] = users[user.id]['xp'] - users[user.id]['xp_end']
			with open('user.json', 'w') as f:
				json.dump(users, f)
		if hp <= 0:
			embed3 = discord.Embed(description='You lost the battle and lost **{}%** of their **xp**.\nBetter luck next time!'.format(percent), color=discord.Colour.red())
			embed3.set_author(name='{} lost the battle.'.format(user.name))
			embed3.set_thumbnail(url=user.avatar_url)
			users[user.id]['xp'] /= xp
			final2 = int(users[user.id]['xp'])
			users[user.id]['xp'] = final2
			users[user.id]['hp'] = restarthp
			await client.say(embed=embed3)
			with open('user.json', 'w') as f:
				json.dump(users, f)
	else:
		await client.say('Looks like you are not prepared, **{}**. Type **`>start`** to prepare for battle!'.format(user.name))
		
			
	
async def werewolf(users, user):
	if user.id in users:
		randomhp = random.randint(200, 500)
		exp = users[user.id]['xp']
		lvl_start = users[user.id]['level']
		xp_end = users[user.id]['xp_end']
		werew = 'https://cdn.discordapp.com/attachments/364310715521040384/469297938997313537/832d2ac094db3633ddd7deff8b176ff1-01.jpeg'
		weapon = users[user.id]['equipped_weapon']['name']
		dmg = users[user.id]['equipped_weapon']['dmg']
		enemyhp = randomhp
		maxEnemyhp = randomhp
		hp = users[user.id]['hp']
		givehp = random.randint(30, 50)
		restarthp = users[user.id]['restart_hp']
		xp = random.randint(2, 4)
		calc = 100/xp
		percent = int(calc)
		earnxp = random.randint(100, 180)
		while enemyhp > 0 and hp > 0:
			damage = random.randint(5, 20)
			embed = discord.Embed(title='A Werewolf has Appeared!', description='Type **attack** to attack it!\n**Werewolf HP**: {}/{}'.format(enemyhp, maxEnemyhp), color=discord.Colour.red())
			embed.set_author(name='HP: {}/{}'.format(hp, restarthp), icon_url=user.avatar_url)
			embed.set_footer(text='Weapon Equipped: {}'.format(weapon))
			embed.set_thumbnail(url=werew)
			await client.say(embed=embed)
			await client.wait_for_message(author=user, content='attack')
			enemyhp -= dmg
			hp -= damage
			users[user.id]['hp'] -= damage
			with open('user.json', 'w') as f:
				json.dump(users, f)
		if enemyhp <= 0:
			users[user.id]['hp'] += givehp
			if users[user.id]['hp'] > users[user.id]['restart_hp']:
				users[user.id]['hp'] = users[user.id]['restart_hp']
			embed2 = discord.Embed(description='You earned **+{} xp**!\nType `>stats` to see how much xp you have.'.format(earnxp), color=16768768)
			embed2.set_author(name='{} has won the battle!'.format(user.name))
			embed2.set_thumbnail(url=user.avatar_url)
			users[user.id]['xp'] += earnxp
			await client.say(embed=embed2)
			if users[user.id]['xp'] >= users[user.id]['xp_end']:
				users[user.id]['level'] += 1
				users[user.id]['xp_end'] *= 4
				await client.say('**{}** has leveled up to level **{}**!'.format(users[user.id]['level']))
				users[user.id]['restart_hp'] += 50
				users[user.id]['hp'] = users[user.id]['restart_hp']
				users[user.id]['xp'] = users[user.id]['xp'] - users[user.id]['xp_end']
			with open('user.json', 'w') as f:
				json.dump(users, f)
		if hp <= 0:
			embed3 = discord.Embed(description='You lost the battle and lost **{}%** of their **xp**.\nBetter luck next time!'.format(percent), color=discord.Colour.red())
			embed3.set_author(name='{} lost the battle.'.format(user.name))
			embed3.set_thumbnail(url=user.avatar_url)
			users[user.id]['xp'] /= xp
			final2 = int(users[user.id]['xp'])
			users[user.id]['xp'] = final2
			users[user.id]['hp'] = restarthp
			await client.say(embed=embed3)
			with open('user.json', 'w') as f:
				json.dump(users, f)
	else:
		await client.say('Looks like you are not prepared, **{}**. Type **`>start`** to prepare for battle!'.format(user.name))
		

#add weapon to database (me only)
@client.command(pass_context=True)
async def update(ctx):
	required_role = [role.name for role in ctx.message.author.roles]
	if "Owner" in required_role:
		with open('user.json', 'r') as f:
			users = json.load(f)
		wooden_spear = "Wooden Spear"
		ws_value = 150
		m66 = "M66"
		m66_dmg = 150
		m66_value = 1000
		vc9 = "VC9"
		vc9_dmg = 250
		vc9_value = 1600
		ws_dmg = 50
		blades_of_chaos = "Blades of Chaos"
		boc_dmg = 500
		boc_value = 9550
		dark_sword = "Dark Sword"
		ds_dmg = 400
		ds_value = 8450
		users["weapon"] = {}
		users["weapon"][wooden_spear] = {}
		users["weapon"][wooden_spear]['name'] = wooden_spear
		users["weapon"][wooden_spear]['dmg'] = ws_dmg
		users["weapon"][wooden_spear]['value'] = ws_value
		users["weapon"][blades_of_chaos] = {}
		users["weapon"][blades_of_chaos]['name'] = blades_of_chaos
		users["weapon"][blades_of_chaos]['dmg'] = boc_dmg
		users["weapon"][blades_of_chaos]['value'] = boc_value
		users["weapon"][m66] = {}
		users["weapon"][m66]['name'] = m66
		users["weapon"][m66]['dmg'] = m66_dmg
		users["weapon"][m66]['value'] = m66_value
		users["weapon"][vc9] = {}
		users["weapon"][vc9]['name'] = vc9
		users["weapon"][vc9]['dmg'] = vc9_dmg
		users["weapon"][vc9]['value'] = vc9_value
		users["weapon"][dark_sword]={}
		users["weapon"][dark_sword]['name'] = dark_sword
		users["weapon"][dark_sword]["dmg"] = ds_dmg
		users["weapon"][dark_sword]['value'] = ds_value
		
		with open('user.json', 'w') as f:
			json.dump(users, f)
		await client.say("**Weapon database has been updated!**")
		#weapons command
@client.command(pass_context=True)
async def weapons(ctx):
	with open('user.json', 'r') as f:
		users = json.load(f)
	await listed_weapons(users, ctx.message.author)
	
async def listed_weapons(users, user):
	if user.id in users:
		listed = users[user.id]['weapons']
		await client.say(':crossed_swords: | **{}**, here are your available weapons: **{}**'.format(user.name, '\n'.join(listed)))
	else:
		await client.say('**{}**, looks like you do not own a weapon. Type **`>start`** to do so!'.format(user.name))

#amount of gold
@client.command(pass_context=True)
async def gold(ctx):
	with open('user.json', 'r') as f:
		users = json.load(f)
	await amt_gold(users, ctx.message.author)
	
async def amt_gold(users, user):
	if user.id in users:
		list = users[user.id]['gold']
		await client.say(':moneybag: **| {}**, you have **{}** gold.'.format(user.name, list))
	else:
		await client.say('**{}**, you have not earned any gold yet. Type **`>start`** to earn some!'.format(user.name))
		
#equip command
@client.command(pass_context=True)
async def equip(ctx, *, weapon_chosen):
	with open('user.json', 'r') as f:
		users = json.load(f)
	await weapon_equip(users, ctx.message.author, weapon_chosen)
	with open('user.json', 'w') as f:
		json.dump(users, f)
	
async def weapon_equip(users, user, equip):
	if user.id in users:
		weapon = users[user.id]['weapons']
		dmg = users["weapon"][equip]['dmg']
		if equip in weapon:
			await client.say('**{}** has been equipped!'.format(equip))
			users[user.id]['equipped_weapon']['name'] = equip
			users[user.id]['equipped_weapon']['dmg'] = dmg
	else:
		await client.say('Looks like you do not own any weapons, **{}**. Type **`>start`** to own one!'.format(user.name))
		
#stats for battle
@client.command(pass_context=True)
async def stats(ctx):
	with open('user.json', 'r') as f:
		users = json.load(f)
		hp = users[ctx.message.author.id]['hp']
		maxHP = users[ctx.message.author.id]['restart_hp']
		gold = users[ctx.message.author.id]['gold']
		weapon_e = users[ctx.message.author.id]['equipped_weapon']['name']
		weapon_d = users[ctx.message.author.id]['equipped_weapon']['dmg']
		xp = users[ctx.message.author.id]['xp']
		level = users[ctx.message.author.id]['level']
		xp_end = users[ctx.message.author.id]['xp_end']
	embed = discord.Embed(description='**HP**: {}/{}\n**Gold**: {}\n**Level**: {}\n**XP**: {}/{}\n**Weapon Equipped**: {}\n	**Weapon Damage**: {}'.format(hp, maxHP, gold, level, xp, xp_end, weapon_e, weapon_d), color=discord.Colour.purple())
	embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
	embed.set_thumbnail(url=ctx.message.author.avatar_url)
	await client.say(embed=embed)

#earn gold
@client.listen()
async def on_message(message):
	if message.author == client.user:
		return
	with open('user.json', 'r') as f:
		users = json.load(f)
		rgold = random.randint(15, 25)
		await addgold(users, message.author, rgold)
		with open('user.json', 'w') as f:
			json.dump(users, f)
	
async def addgold(users, user, amount):
	if user.id in users:
		users[user.id]['gold'] += amount

#dad joke
@client.listen()
async def on_message(message):
	if message.author == client.user:
		return
	if message.content.lower().startswith("i'm "):
		output = message.content.lower().split("i'm")
		await client.send_message(message.channel, "Hello," + ''.join(output[:2]) + "\nI\'m " + client.user.mention + ".")
	if message.content.lower().startswith('im '):
		output = message.content.lower().split('im')
		await client.send_message(message.channel, "Hello," + ''.join(output[:2]) + "\nI\'m " + client.user.mention + ".")
	
#reacts to hi
@client.listen()
async def on_message(message):
	if message.author == client.user:
		return
	if message.content.lower() == "hi":
		await client.add_reaction(message, emoji='👋')
		
#info command
@client.listen()
async def on_message(message):
	if message.author == client.user:
		return
	if message.content == ">info":
		bot_spamRequired = client.get_channel(id='335901699678011392')
		if message.channel == bot_spamRequired:
			roles = [role.name for role in message.author.roles]
			embed = discord.Embed(title=message.author.name + "#" + message.author.discriminator, description=message.author.mention, color = discord.Colour.orange())
			embed.set_thumbnail(url=message.author.avatar_url)
			embed.add_field(name='Status', value=message.author.status, inline=False)
			embed.add_field(name="User ID", value=message.author.id, inline=False)
			embed.add_field(name="Roles", value=', '.join(roles), inline=False)
			embed.set_footer(text="Joined At | {}".format(message.author.joined_at.strftime("%A, %B %d %Y at %I:%M:%S %p")))
			await client.send_message(message.channel, embed = embed)
	
#remove afk
@client.listen()
async def on_message(message):
	if message.author == client.user:
		return
	already_afk = [role.name for role in message.author.roles]
	AFK = discord.Object(id='465470033544347658')
	if "AFK" in already_afk:
		await client.remove_roles(message.author, AFK)
		await client.change_nickname(message.author, message.author.name)
		await client.send_message(message.channel, "Welcome back, {}!".format(message.author.mention))
		

#token
client.run(os.getenv('TOKEN'))

