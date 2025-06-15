import discord

# Define the admin-only check
def is_guild_admin(interaction: discord.Interaction) -> bool:
    return interaction.user.guild_permissions.administrator