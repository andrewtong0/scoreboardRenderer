# scoreboardRenderer
Quick and easy way to render a simple scoreboard graphic. Includes modifiable spacing and sizing parameters, font selection, background images, and more.

Originally created for a Teamfight Tactics tournament for my friend. He was hosting the tournament, which made it difficulty to also simultaneously update a score graphic, so I designed him a simple script to do it quickly and esaily.

![Sample Image](https://raw.githubusercontent.com/andrewtong0/scoreboardRenderer/master/publish.jpg)

### Dependencies
- Pillow (PIL fork)
- Discord (bot interfacing), and all associated parameters (verified user UUIDs, channel ID, bot token)

### How to use it
1. Place a font file (.ttf/.otf) in the code directory, and set fontName to the file name (e.g. Arial.ttf)
2. Specify the environment variables necessary (verified user UUIDs, channel IDs, bot token)
3. Invite the bot to your Discord server
4. Invoke the necessary commands to add players and add scores to the players
  - Note, all commands are case sensitive, must be preceded by '/', and all player names are case sensitive to what you set when you add them.
  - Commands can be found by typing /help
  -  Commands reference
  ```
  /addPlayer PLAYERNAME         # Adds the specified player to the list of players
  /removePlayer PLAYERNAME      # Removes the specified player from the list of players
  /addScore PLAYERNAME SCORE    # Adds the specified score (integer) to player
  /removeScore PLAYERNAME       # Removes the most recent score from the specified player
  /render                       # Outputs a chroma-key output of the scoreboard for verification and chroma purposes
  /getScores PLAYERNAME         # Get an array of all the scores of a specified player
  /getPlayers                   # Outputs all players (will show their case sensitivity as well for referencing)
  /clear                        # Clears all players and their associated scores
  /publish                      # Outputs all player scores in a nicely formatted manner to the specified channel ID for publishing
  /help                         # Lists all available commands
  ```

### Additional Features
- You can specify the spacing, font size, and initial X/Y values with the global variables
- If you have your own custom scorecard background, you can upload and replace the preset one
