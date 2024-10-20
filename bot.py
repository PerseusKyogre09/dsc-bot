import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import yt_dlp
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define the intents
intents = discord.Intents.default()
intents.message_content = True  # Enable specific intent to read messages

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize XP and level storage
user_data = {}

def get_level_and_xp(xp):
    level = 0
    while xp >= (level + 1) * 100:  # Assume 100 XP per level
        level += 1
    return level, xp - level * 100  # Return level and current XP

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Increment XP
    if message.author.id not in user_data:
        user_data[message.author.id] = {'xp': 0}
    
    user_data[message.author.id]['xp'] += 10  # Gain 10 XP per message

    # Get level and xp for the user
    level, xp = get_level_and_xp(user_data[message.author.id]['xp'])
    
    # Update the user's level
    user_data[message.author.id]['level'] = level
    user_data[message.author.id]['current_xp'] = xp
    
    # Process commands
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    embed = discord.Embed(title="Ping Command", description="Pong!", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command(name='invite')
async def invite(ctx):
    invite_link = f'https://discord.com/oauth2/authorize?client_id=750388471834607707&permissions=8&integration_type=0&scope=bot'
    embed = discord.Embed(title="Invite Me", description=f'[Invite Me From Here](invite_link)', color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command(name='xp')
async def xp(ctx):
    user_id = ctx.author.id
    if user_id not in user_data:
        embed = discord.Embed(title="XP Info", description="You have not sent any messages yet.", color=0xff0000)
        await ctx.send(embed=embed)
        return
    
    level = user_data[user_id]['level']
    current_xp = user_data[user_id]['current_xp']
    embed = discord.Embed(title="XP Info", description=f"You are level {level} with {current_xp} XP.", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command(name='play')
async def play(ctx, *, url):
    if not ctx.author.voice:
        embed = discord.Embed(title="Error", description="You need to be in a voice channel to play music!", color=0xff0000)
        await ctx.send(embed=embed)
        return
    
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    # Download and play the audio
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'type': 'audioconvert',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        url = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(url))

    embed = discord.Embed(title="Now Playing", description=f"Playing: **{info['title']}**", color=0x00ff00)
    await ctx.send(embed=embed)

@bot.command(name='stop')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        embed = discord.Embed(title="Stopped", description="Stopped playing music and disconnected from the voice channel.", color=0xff0000)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="I am not currently playing any music.", color=0xff0000)
        await ctx.send(embed=embed)

@bot.command(name='pokedex')
async def pokedex(ctx, *, pokemon_name):
    # Fetch Pokémon data from PokeAPI
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        embed = discord.Embed(title="Error", description="Pokémon not found!", color=0xff0000)
        await ctx.send(embed=embed)
        return

    data = response.json()

    # Extract relevant information
    pokemon_id = data['id']
    name = data['name'].capitalize()
    height = data['height']
    weight = data['weight']
    types = ', '.join([type_info['type']['name'].capitalize() for type_info in data['types']])
    sprite_url = data['sprites']['front_default']

    # Create an embed with the Pokémon data
    embed = discord.Embed(title=f"{name} (#{pokemon_id})", color=0x00ff00)
    embed.add_field(name="Height", value=f"{height * 10} cm", inline=True)  # Height in cm
    embed.add_field(name="Weight", value=f"{weight / 10} kg", inline=True)  # Weight in kg
    embed.add_field(name="Types", value=types, inline=True)
    embed.set_image(url=sprite_url)
    embed.set_footer(text="Data from PokeAPI")

    await ctx.send(embed=embed)

# Run the bot
bot.run(TOKEN)
