import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import discord

playerDict = {}  # KEY: Player name, VAL: Array of scores
fontSize = 70
fontName = ""
font = ImageFont.truetype(fontName, fontSize)
textHorizontalPos = 80
textVerticalPos = 270
nameSpacing = fontSize * 2.85
spacingPerScore = 8
firstAndTotalTextSpacing = 1255

render_input_image = "input_render.jpg"
publish_input_image = "input_publish2.jpg"  # Must be absolute path when deployed for whatever reason

render_image_filename = "render"
publish_image_filename = "publish"

# ENVIRONMENT VARIABLES
verifiedUsers = [0]
publishChannelID = 0


class PlayerData:
    def __init__(self, player_name):
        self.name = player_name
        self.scores = []
        self.total = 0
        self.placement = -1
        self.first_places = 0

    def add_score(self, score):
        score = int(score)
        self.scores.append(score)
        self.total += score
        if score == 1:
            self.first_places += 1

    def remove_score(self):
        if self.scores:
            self.total -= self.scores[-1]
            del self.scores[-1]

    def get_player_scores(self):
        return self.scores

    def set_placement(self, placement):
        self.placement = placement


def add_player(player):
    if player not in playerDict:
        playerDict[player] = PlayerData(player)


def remove_player(player):
    playerDict.pop(player, None)


def view_all_players():
    players = []
    for player in playerDict:
        players.append(player)
    return players


def clear_all():
    print("Clear...")


def render_image(image_filename, input_image, data):
    img = Image.open(input_image)
    draw = ImageDraw.Draw(img)
    player_counter = 0
    for player in data:
        placement = str(player[0])
        name = player[1]
        scores = player[2]
        first_places = str(player[3])
        total = str(player[4])

        draw.text((textHorizontalPos, textVerticalPos + player_counter * fontSize * 1.15), placement + ".",
                  (255, 255, 255), font=font)
        draw.text((textHorizontalPos + 90, textVerticalPos + player_counter * fontSize * 1.15), name,
                  (255, 255, 255), font=font)
        score_counter = 1
        for score in scores:
            draw.text((textHorizontalPos + nameSpacing + score_counter * spacingPerScore * fontSize / 4,
                       textVerticalPos + player_counter * fontSize * 1.15), str(score), (255, 255, 255), font=font)
            score_counter += 1

        rect_width = 220
        rect_height = 60
        rect_hori_spacing = 15
        rect_vert_spacing = 30
        vertical_position = textVerticalPos + player_counter * fontSize * 1.15
        draw.rectangle([(textHorizontalPos + firstAndTotalTextSpacing - rect_width/2 + rect_hori_spacing,
                         vertical_position - rect_height/2 + rect_vert_spacing),
                       (textHorizontalPos + firstAndTotalTextSpacing + rect_width/2 + rect_hori_spacing,
                        vertical_position + rect_height/2 + rect_vert_spacing)],
                       fill=(255, 255, 255))
        draw.text((textHorizontalPos + firstAndTotalTextSpacing, vertical_position),
                  first_places, (255, 0, 0), font=font)
        draw.rectangle([(textHorizontalPos + firstAndTotalTextSpacing - rect_width / 2 + rect_hori_spacing + 330,
                         vertical_position - rect_height / 2 + rect_vert_spacing),
                        (textHorizontalPos + firstAndTotalTextSpacing + rect_width / 2 + rect_hori_spacing + 330,
                         vertical_position + rect_height / 2 + rect_vert_spacing)],
                       fill=(255, 255, 255))
        draw.text((textHorizontalPos + firstAndTotalTextSpacing + 330, vertical_position),
                  total, (255, 0, 0), font=font)
        player_counter += 1
    img.save(image_filename + ".jpg")


def generate_ordered_dict():
    updated_player_dict = {}
    for player in playerDict:
        player_data = playerDict[player]
        key = player_data.total
        if key not in updated_player_dict:
            updated_player_dict[key] = [player_data]
        else:
            updated_player_dict[key].append(player_data)
    return [updated_player_dict, sorted(updated_player_dict.keys())]


def format_scoreboard_data(ordered_data):
    updated_player_dict = ordered_data[0]
    ordered_keys = ordered_data [1]
    placement = 1
    formatted_data = []
    for score in ordered_keys:
        players_with_score = updated_player_dict[score]
        for playerData in players_with_score:
            name = playerData.name
            scores = playerData.scores
            first_places = playerData.first_places
            total = playerData.total
            formatted_data.append([placement, name, scores, first_places, total])
            playerData.placement = placement
        placement += 1
    return formatted_data


def render_player_scores():
    ordered_dict = generate_ordered_dict()
    scoreboard_data = format_scoreboard_data(ordered_dict)
    render_image(render_image_filename, render_input_image, scoreboard_data)
    render_image(publish_image_filename, publish_input_image, scoreboard_data)


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
                    playerDict[player].add_score(score)
                    await message.channel.send("Score of " + score + " has been added to " + player + "'s total score.")
                except:
                    await message.channel.send("An error occurred. Please check that you spelled the player's name"
                                               "correctly (case-sensitive), and that you included a score to set as"
                                               "well (should be in the form /addScore playerName score")
            elif keyword == "removeScore":
                try:
                    playerDict[value].remove_score()
                    await message.channel.send(value + "'s most recent score has been removed.")
                except:
                    await message.channel.send("Player not found or player has no scores to remove.")
            elif keyword == "render":
                render_player_scores()
                await message.channel.send(
                    file=discord.File(render_image_filename + ".jpg"))
            elif keyword == "getScores":
                await message.channel.send(playerDict[value].get_player_scores())
            elif keyword == "getPlayers":
                await message.channel.send(view_all_players())
            elif keyword == "clear":
                clear_all()
                await message.channel.send("All player and score information cleared.")
            elif keyword == "publish":
                try:
                    publish_channel = client.get_channel(publishChannelID)
                    await publish_channel.send("Current player standings:")
                    await publish_channel.send(
                        file=discord.File(publish_image_filename + ".jpg"))
                except:
                    await message.channel.send("Error locating image or error locating channel to send to.")
            elif keyword == "help":
                print(generate_ordered_dict())
                await message.channel.send("List of commands: /addPlayer /removePlayer /addScore /removeScore"
                                           " /render /getScores /getPlayers /clear /publish /help")


client.run(os.environ["BOT_TOKEN"])
