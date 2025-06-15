import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from toast_db import (create_user_table, increase_blue_dogs, get_blue_dogs, get_top_blue_dogs, delete_blue_dog, set_blue_dog, 
                      create_message_table, add_message_id, check_if_message_exists)
from rps import initialize_rps, play_rps

create_user_table()
create_message_table()

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

guild = 1066404180631224441
GUILD_ID = discord.Object(id=guild)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

BLUE_DOG_STICKER_ID = 1323013060067196980
BLUE_DOG_MESSAGE_CHANNEL = 1380677819020873788
BLUE_DOG_EMOTE_ID = 1323012300554375178
BLUE_DOG_EMOTE_NAME = 'BestBoi1stplace'
BLUE_DOG_PIC_URL = "https://media.discordapp.net/stickers/1323013060067196980.webp?size=160&quality=lossless"

DOG_BLUE = discord.Color.from_str("#2C4A85")

@bot.event
async def on_ready():
    await bot.tree.sync(guild=GUILD_ID)
    initialize_rps(bot)
    print(f'{bot.user} is online!')

# @bot.event
# async def on_message(message: discord.Message):
#     print(message.stickers)

@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    exists = check_if_message_exists(reaction.message.id)
    try:
        # if the reaction is a blue dog and it's only the instance
        if (reaction.emoji.id == BLUE_DOG_EMOTE_ID and reaction.count == 1):
            # check if this message has already been awarded a blue dog
            exists = check_if_message_exists(reaction.message.id)
            if (not exists):
                add_message_id(reaction.message.id)
                # send the blue dog message in the channel the reaction happened in
                channel = reaction.message.channel
                await channel.send(content=f"```[{reaction.message.author.name} has earned (1) Blue Dog]!```", stickers=[discord.Object(id=BLUE_DOG_STICKER_ID)])
                increase_blue_dogs(reaction.message.author.id)
                # send a link message to the blue dog channel
                channel = bot.get_channel(BLUE_DOG_MESSAGE_CHANNEL)
                embed = discord.Embed(title="Blue Dog", color=DOG_BLUE)
                embed.set_thumbnail(url=BLUE_DOG_PIC_URL)
                message_link = f"https://discord.com/channels/{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id}"
                embed.add_field(name=f'{reaction.message.author.name}', value=reaction.message.content)
                embed.add_field(name="Link", value=f'[go to message]({message_link})')
                await channel.send(embed=embed, content=f'<#{reaction.message.channel.id}>')
    except:
        return

# Blue Dog commands

@bot.tree.command(name="bdcount", description="Gets the number of blue dogs you have", guild=GUILD_ID)
async def get_blue_dog_count(interaction: discord.Interaction):
    try:
        count = get_blue_dogs(interaction.user.id)
        embed = discord.Embed(title="Blue Dog", color=DOG_BLUE, description=f'{interaction.user.name} has {count} `[Blue Dog]`!')
        embed.set_thumbnail(url=BLUE_DOG_PIC_URL)
        await interaction.response.send_message(embed=embed)
    except:
        toast_failed(interaction)

@bot.tree.command(name="bdrank", description="Gets the top 10 blue dog winners", guild=GUILD_ID)
async def get_blue_dog_rank(interaction: discord.Interaction):
    try:
        rank = get_top_blue_dogs()
        content = ""
        if (rank != None):
            for index, user_row in enumerate(rank):
                if (len(user_row) == 2):
                    user = bot.get_user(user_row[1])
                    if (user != None):
                        content = content + f'\n`{index+1}: {user.name} - {user_row[0]}`'
                    else:
                        content = content + f'\n`{index+1}: *REDACTED* - {user_row[0]}`'

        embed = discord.Embed(title="Blue Dog Rank", color=DOG_BLUE, description="The current blue dog leaderboard")
        embed.add_field(name="Top 10", value=content)
        
        await interaction.response.send_message(embed=embed)
    except:
        toast_failed(interaction)

@bot.tree.command(name="bdremove", description="Remove user's blue dog count", guild=GUILD_ID)
async def delete_blue_dogs(interaction: discord.Interaction, user: str):
    if (is_not_admin(interaction)):
        send_not_admin_message(interaction)
        return
    
    try:
        for member in interaction.guild.members:
            if str(member.name) == user:
                delete_blue_dog(member.id)
                await interaction.response.send_message(content=f'Removed {member.name} blue dogs :(')
                return
        await interaction.response.send_message(content=f'Unable to remove {member.name} blue dogs')
    except:
        toast_failed(interaction)

@bot.tree.command(name="bdset", description="Set a user's blue dog count", guild=GUILD_ID)
async def set_blue_dog_count(interaction: discord.Interaction, user: str, count: int):
    if (is_not_admin(interaction)):
        send_not_admin_message(interaction)
        return

    try:
        for member in interaction.guild.members:
            if str(member.name) == user:
                set_blue_dog(member.id, count)
                await interaction.response.send_message(content=f'Updated {member.name} blue dog count!')
                return
        await interaction.response.send_message(content=f'Unable to update {member.name} blue dogs')
    except:
        toast_failed(interaction)

# Rock, paper scissors commands

@bot.tree.command(name="rps", description="Play a game of Rock, Paper, Scissors", guild=GUILD_ID)
async def rpc(interaction: discord.Interaction, selection: str):
    result = play_rps(bot, selection.lower(), interaction.user.name)
    await interaction.response.send_message(content=result)

# Utilities

def is_not_admin(interaction: discord.Interaction) -> bool:
    return not interaction.user.guild_permissions.administrator

async def send_not_admin_message(interaction: discord.Interaction) -> bool:
    try:
        await interaction.user.send(content="\*Toast prints out a message that reads: `You need to be an admin silly >.<`\*")
        await interaction.response.send_message("", ephemeral=True)
    except:
        await interaction.response.send_message(content=f'\*Toast glitches out and the command fails\*')

async def toast_failed(interaction: discord.Interaction) -> bool:
    await interaction.response.send_message(content=f'\*Toast glitches out and the command fails\*')
    
bot.run(TOKEN)