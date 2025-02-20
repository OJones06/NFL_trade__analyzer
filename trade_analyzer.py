# Define a Player class to represent a player with attributes like ID, name, position, team, and value
class Player:
    def __init__(self, player_id, name, position, team, value):
        self.player_id = player_id
        self.name = name
        self.position = position
        self.team = team
        self.value = value

# Define a Team class to represent a team with a name and a list of players
class Team:
    def __init__(self, name):
        self.name = name
        self.players = []

    # Method to add a player to the team
    def add_player(self, player):
        self.players.append(player)

    # Method to remove a player from the team
    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
        else:
            print(f"Player {player.name} not found in team {self.name}")

    # Method to calculate the total value of the team by summing up the values of all players
    def total_value(self):
        return sum(player.value for player in self.players)

# Function to analyze a trade between two teams
def analyze_trade(team1, team2, players_from_team1, players_from_team2):
    # Calculate the initial total values of both teams
    team1_value_before = team1.total_value()
    team2_value_before = team2.total_value()

    # add up team player values
    team2_value = sum(player.value for player in players_from_team1)
    team1_value = sum(player.value for player in players_from_team2)

    # Determine which team is favored by the trade
    if team1_value > team2_value:
        favored_team = "Team 1"
        points = team1_value - team2_value
    else:
        favored_team = "Team 2"
        points = team2_value - team1_value

    # Return the trade analysis result as a dictionary
    return {
        "favored_team": favored_team,
        "points": points,
    }

# Example usage:
# player1 = Player("1", "Player 1", "QB", "Team A", 100)
# player2 = Player("2", "Player 2", "RB", "Team B", 80)
# team1 = Team("Team 1")
# team2 = Team("Team 2")
# team1.add_player(player1)
# team2.add_player(player2)
# result = analyze_trade(team1, team2, [player1], [player2])
# print(result)

