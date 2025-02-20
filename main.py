# Import necessary functions and classes
from load_players import load_players_from_excel
from trade_analyzer import Team, analyze_trade

def main():
    # Replace with the actual path to your local Excel file
    file_path = '/Users/owenjones/Trade_analyzer/NFL_Trade_values_Feb.xlsx'
    
    # Load players from the Excel file
    players = load_players_from_excel(file_path)
    
    # Print player details to verify they loaded correctly
    for player in players:
        print(f"ID: {player.player_id}, Name: {player.name}, Position: {player.position}, Team: {player.team}, Value: {player.value}")
    
    # Create teams and add players
    team1 = Team("Team 1")
    team2 = Team("Team 2")
    
    # Add first 5 players to team1
    for player in players[:5]:
        team1.add_player(player)
    
    # Add next 5 players to team2
    for player in players[5:10]:
        team2.add_player(player)
    
    # Print initial team values
    print(f"Team 1 initial value: {team1.total_value()}")
    print(f"Team 2 initial value: {team2.total_value()}")
    
    # Analyze a trade between the first player of each team
    result = analyze_trade(team1, team2, [team1.players[0]], [team2.players[0]])
    
    # Print trade analysis result
    print(f"Team 1 value change: {result['team1_value_change']}")
    print(f"Team 2 value change: {result['team2_value_change']}")

# Run the main function if this script is executed
if __name__ == "__main__":
    main()