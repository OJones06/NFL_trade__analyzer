# Import necessary modules
import pandas as pd
from trade_analyzer import Player

# Function to load players from an Excel file
def load_players_from_excel(file_path):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path)
    players = []
    # Iterate over each row in the DataFrame and create Player objects
    for _, row in df.iterrows():
        player = Player(
            player_id=row['player_id'],
            name=row['name'],
            position=row['position'],
            team=row['team'],
            value=row['value']
        )
        players.append(player)
    return players

# Example usage:
# players = load_players_from_excel('/path/to/your/excel/file.xlsx')
# for player in players:
#     print(player.name, player.team, player.value)
