import discord
from discord.ext import commands
from config import BOT_TOKEN

# checks if the bot token is set
if BOT_TOKEN == "put_token_here":
    raise ValueError("Please set your BOT_TOKEN in bot_token.py!")

# Initialise bot with command prefix
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Displays when the bot logged in
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Command for displaying the pinned messages of the channel/thread
@bot.command(name='showPinned')
async def show_pinned(ctx):
    print('Displaying list of pinned messages! Await answer.')
    pinned_messages = await ctx.channel.pins()
    if pinned_messages:
        message_list = [msg.content if msg.content else "[Embed/Attachment]" for msg in pinned_messages]
        message_output = "\n".join(message_list)
        await ctx.send(f"**Pinned messages in this thread:**\n{message_output}")
        print('Pinned messages were displayed.')
    else:
        await ctx.send("No pinned messages found in this thread.")
        print('No pinned messages found in this thread.')

# Command for pinning the message before the command call
@bot.command(name='pinThat')
async def pin_message(ctx):
    try:
        messages = [message async for message in ctx.channel.history(limit=2)] # Fetches the last 2 messages
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

@bot.command(name='pinThis')
async def pin_message(ctx):
    try:
        if ctx.message.reference:
            message_to_pin = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            if message_to_pin.pinned:
                await message_to_pin.unpin()  # Pins the message
                await ctx.send(f"Message successfully unpinned.")
                print(f'Message was unpinned: "{message_to_pin.content}"')
            else:
                await message_to_pin.pin()  # Pins the message
                await ctx.send(f"Message successfully pinned.")
                print(f'Message was pinned: "{message_to_pin.content}"')
        else:
            await ctx.send("You need to reply to the message with this command for me to know what to pin!")
            return

    except discord.Forbidden:
        await ctx.send("I don't have permission to pin messages in this channel.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {e}")

bot.run(BOT_TOKEN)
