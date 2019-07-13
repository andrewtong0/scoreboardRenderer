from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

playerDict = {}  # KEY: Player name, VAL: Array of scores
fontSize = 70
img = Image.open("standings_empty.jpg")
draw = ImageDraw.Draw(img)
fontName = ""
font = ImageFont.truetype(fontName, fontSize)
textHorizontalPos = 110
textVerticalPos = 270
nameSpacing = fontSize*2.65


def add_player(player):
    if player not in playerDict:
        playerDict[player] = []


def remove_player(player):
    playerDict.pop(player, None)


def add_player_score(player, new_score):
    playerDict[player].append(new_score)


def remove_player_score(player):
    del playerDict[player][-1]


def render_player_scores():
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
