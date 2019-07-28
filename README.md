# scoreboardRenderer
Quick and easy way to render a simple scoreboard graphic. Includes modifiable spacing and sizing parameters, font selection, background images, and more.

Originally created for a Teamfight Tactics tournament for my friend. He was hosting the tournament, which made it difficulty to also simultaneously update a score graphic, so I designed him a simple script to do it quickly and esaily.

![Sample Image](https://raw.githubusercontent.com/andrewtong0/scoreboardRenderer/master/publish.jpg)

### Dependencies
- Pillow (PIL fork)

### How to use it
1. Place a font file (.ttf/.otf) in the code directory, and set fontName to the file name (e.g. Arial.ttf)
2. Invoke the predefined functions to set up your scoreboard
  - Start by adding players to the list (e.g. add_player("player_name"))
  - Record each player's scores (as a string) at each round (e.g. add_player_score("2"))
3. Render the scorecard (render_player_scores())

### Additional Features
- You can specify the spacing, font size, and initial X/Y values with the global variables
- If you have your own custom scorecard background, you can upload and replace the preset one
