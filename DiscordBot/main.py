import discord
from discord.ext import commands
from config import BOT_TOKEN

# checks if the bot token is set
if BOT_TOKEN == "put_token_here":
    raise ValueError("Please set your BOT_TOKEN in bot_token.py!")

# Channel id for the showPinned command
CHANNEL_ID = 1164973198174077038

# Initialise bot with command prefix
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Displays when the bot logged in
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Command for displaying the pinned messages in a certain channel
@bot.command(name='showPinned')
async def show_pinned(ctx):
    print(f'Displaying list of pinned messages! Await answer.')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        pinned_messages = await channel.pins()
        if pinned_messages:
            message_list = [f"{msg.content}" for msg in pinned_messages]
            message_output = "\n".join(message_list)
            await ctx.send(f"**Pinned messages in {channel.name}:**\n{message_output}")
            print(f'List was displayed.')
        else:
            await ctx.send("No pinned messages found.")
            print(f'No list of pinned messages was found.')
    else:
        await ctx.send(f"Channel with ID {CHANNEL_ID} not found.")
        print(f'Error - Channel with {CHANNEL_ID} was not found.')

# Command for displaying the pinned messages in the thread the command was invoked
@bot.command(name='showThreadPin')
async def show_thread_pin(ctx):
    # Check if the command was called in a thread
    if isinstance(ctx.channel, discord.Thread):
        pinned_messages = await ctx.channel.pins()
        if pinned_messages:
            message_list = [f"{msg.content}" for msg in pinned_messages]
            message_output = "\n".join(message_list)
            await ctx.send(f"**Pinned messages in this thread:**\n{message_output}")
            print(f'Pinned messages were displayed.')
        else:
            await ctx.send("No pinned messages found in this thread.")
            print(f'No pinned messages found in this thread.')
    else:
        await ctx.send("This command can only be used in threads.")
        print(f'Error - Command was not called in a thread.')

# Command for pinning the message before the command call
@bot.command(name='pinThat')
async def pin_message(ctx):
    try:
        messages = [message async for message in ctx.channel.history(limit=2)] # Fetches the command message and the message to be pinned
        if len(messages) < 2:
            await ctx.send("No previous message to pin.")
            return

        message_to_pin = messages[1]

        await message_to_pin.pin() # Pins the message
        await ctx.send(f"Message successfully pinned.")
        print(f'Message was pinned: "{message_to_pin}"')

    except discord.Forbidden:
        await ctx.send("I don't have permission to pin messages in this channel.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {e}")

bot.run(BOT_TOKEN)
