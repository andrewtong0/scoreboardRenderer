import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import discord

playerDict = {}  # KEY: Player name, VAL: Array of scores
fontSize = 70
input_image = "input_publish.jpg"
fontName = os.environ.get('FONT_NAME')
font = ImageFont.truetype(fontName, fontSize)
textHorizontalPos = 110
textVerticalPos = 270
nameSpacing = fontSize*2.65

#ENVIRONMENT VARIABLES
verifiedUsers = [160296617382117377]
publishChannelID = 546495546198589440


def add_player(player):
    if player not in playerDict:
        playerDict[player] = []


def remove_player(player):
    playerDict.pop(player, None)


def add_player_score(player, new_score):
    playerDict[player].append(new_score)


def remove_player_score(player):
    del playerDict[player][-1]


def view_all_players():
    players = []
    for player in playerDict:
        players.append(player)
    return players


def view_player_scores(player):
    return playerDict[player]


def clear_all():
    playerDict.clear()


def render_player_scores():
    img = Image.open(input_image)
    draw = ImageDraw.Draw(img)
    player_counter = 0
    for player in playerDict:
        draw.text((textHorizontalPos, textVerticalPos + player_counter * fontSize * 1.15), player,
                  (255, 255, 255), font=font)
        score_counter = 1
        total_score = 0
        for score in playerDict[player]:
            draw.text((textHorizontalPos + nameSpacing + score_counter * 10 * fontSize/4,
                       textVerticalPos + player_counter * fontSize * 1.15), score, (255, 255, 255), font=font)
            score_counter += 1
            total_score += int(score)
        draw.text((textHorizontalPos + nameSpacing + score_counter * 10 * fontSize/4,
                   textVerticalPos + player_counter * fontSize * 1.15), str(total_score), (255, 0, 0), font=font)
        player_counter += 1
    img.save("output.jpg")


client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author.id in verifiedUsers:
        if message.content.startswith("/"):
            command = message.content[1:]
            keyword = command.partition(' ')[0]
            value = command.partition(' ')[2]
            if keyword == "addPlayer":
                add_player(value)
                await message.channel.send(value + " has been added to the list of players.")
            elif keyword == "removePlayer":
                try:
                    remove_player(value)
                    await message.channel.send(value + " has been removed from the list of players.")
                except:
                    await message.channel.send("Player could not be removed. Please ensure"
                                               "they exist in the player list.")
            elif keyword == "addScore":
                try:
                    player = value.partition(' ')[0]
                    score = value.partition(' ')[2]
                    add_player_score(player, score)
                    await message.channel.send("Score of " + score + " has been added to " + player + "'s total score.")
                except:
                    await message.channel.send("An error occurred. Please check that you spelled the player's name"
                                               "correctly (case-sensitive), and that you included a score to set as"
                                               "well (should be in the form /addScore playerName score")
            elif keyword == "removeScore":
                try:
                    remove_player_score(value)
                    await message.channel.send(value + "'s most recent score has been removed.")
                except:
                    await message.channel.send("Player not found or player has no scores to remove.")
            elif keyword == "render":
                render_player_scores()
                await message.channel.send(file=discord.File('output.jpg'))
            elif keyword == "getScores":
                await message.channel.send(view_player_scores(value))
            elif keyword == "getPlayers":
                await message.channel.send(view_all_players())
            elif keyword == "clear":
                clear_all()
                await message.channel.send("All player and score information cleared.")
            elif keyword == "publish":
                try:
                    publish_channel = client.get_channel(publishChannelID)
                    await publish_channel.send("Current player standings:")
                    await publish_channel.send(file=discord.File('output.jpg'))
                except:
                    await message.channel.send("Error locating image or error locating channel to send to.")
            elif keyword == "help":
                await message.channel.send("List of commands: /addPlayer /removePlayer /addScore /removeScore"
                                           "/render /getScores /getPlayers /clear /publish /help")

client.run(os.environ.get('BOT_TOKEN'))

### Refactot to use error codes instead
