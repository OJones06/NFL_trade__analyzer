# Import necessary modules
import tkinter as tk
from tkinter import messagebox
from load_players import load_players_from_excel
from trade_analyzer import Team, analyze_trade

# Define the main application class for the trade analyzer GUI
class TradeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynasty Football Trade Calculator")
        self.root.geometry("800x600")

        # Title and Subtitle
        self.title_label = tk.Label(root, text="Dynasty Football Trade Calculator", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)
        self.subtitle_label = tk.Label(root, text="Created by: Owen Jones", font=("Arial", 12))
        self.subtitle_label.pack(pady=5)

        # Main Frame
        self.main_frame = tk.Frame(root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Search Bars
        self.search_frame = tk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=10)

        self.search_label1 = tk.Label(self.search_frame, text="Seach Players")
        self.search_label1.grid(row=0, column=0, padx=5)
        self.search_entry1 = tk.Entry(self.search_frame, width=30)
        self.search_entry1.grid(row=0, column=1, padx=5, sticky="nsew")
        self.search_entry1.bind("<KeyRelease>", self.search_player1)

        # Player Lists
        self.players_frame = tk.Frame(self.main_frame)
        self.players_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.team1_frame = tk.LabelFrame(self.players_frame, text="Team 1", padx=10, pady=10)
        self.team1_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        self.team1_listbox_frame = tk.Frame(self.team1_frame)
        self.team1_listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.selected_team1_frame = tk.LabelFrame(self.players_frame, text="Selected Team 1 Players", padx=10, pady=10)
        self.selected_team1_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.selected_team1_listbox_frame = tk.Frame(self.selected_team1_frame)
        self.selected_team1_listbox_frame.pack(fill=tk.BOTH, expand=False)

        self.selected_team2_frame = tk.LabelFrame(self.players_frame, text="Selected Team 2 Players", padx=10, pady=10)
        self.selected_team2_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.selected_team2_listbox_frame = tk.Frame(self.selected_team2_frame)
        self.selected_team2_listbox_frame.pack(fill=tk.BOTH, expand=False)

        # Trade Summary
        self.summary_frame = tk.Frame(self.main_frame)
        self.summary_frame.pack(fill=tk.X, pady=10)

        self.summary_label = tk.Label(self.summary_frame, text="Trade Summary", font=("Arial", 14, "bold"))
        self.summary_label.pack()

        self.summary_text = tk.Text(self.summary_frame, height=5, width=80)
        self.summary_text.pack(anchor="center")

        # Favored Team Bar
        self.favored_team_frame = tk.Frame(self.main_frame)
        self.favored_team_frame.pack(fill=tk.X, pady=10)

        self.favored_team_canvas = tk.Canvas(self.favored_team_frame, height=20)
        self.favored_team_canvas.pack(fill=tk.X)

        self.favored_team_indicator = self.favored_team_canvas.create_rectangle(0, 0, 0, 20, fill="red")

        # Reset Button
        self.reset_button = tk.Button(self.main_frame, text="Reset", command=self.reset_trade)
        self.reset_button.pack(pady=10)

        # Initialize player and team data
        self.players = []
        self.team1 = Team("Team 1")
        self.team2 = Team("Team 2")

        # Configure grid weights for resizing
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.players_frame.grid_rowconfigure(0, weight=1)
        self.players_frame.grid_rowconfigure(1, weight=1)
        self.players_frame.grid_columnconfigure(0, weight=1)
        self.players_frame.grid_columnconfigure(1, weight=1)

        self.search_frame.grid_columnconfigure(1, weight=1)
        self.search_frame.grid_columnconfigure(2, weight=1)

        # Automatically load players from the Excel file
        self.load_players()

    # Method to load players from the Excel file
    def load_players(self):
        file_path = '/Users/owenjones/Trade_analyzer/NFL_Trade_values_Feb.xlsx'
        try:
            self.players = load_players_from_excel(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load players: {e}")

    # Method to update the listboxes with players from the search results
    def update_listboxes(self, team1_players, team2_players):
        for widget in self.team1_listbox_frame.winfo_children():
            widget.destroy()

        for player in team1_players[:6]:  # Limit results to 6
            frame = tk.Frame(self.team1_listbox_frame)
            label = tk.Label(frame, text=f"{player.name} ({player.team}) - {player.value}")
            button1 = tk.Button(frame, text="+", command=lambda p=player: self.add_player_to_team1(p))
            button2 = tk.Button(frame, text="+", command=lambda p=player: self.add_player_to_team2(p))
            button1.pack(side=tk.LEFT)
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            button2.pack(side=tk.RIGHT)
            frame.pack(fill=tk.X)

    # Method to search for players for Team 1 based on the search term
    def search_player1(self, event):
        search_term = self.search_entry1.get().lower()
        team1_players = [player for player in self.players if search_term in player.name.lower()]
        self.update_listboxes(team1_players, team1_players)

    # Method to add a player to Team 1
    def add_player_to_team1(self, player):
        self.team1.add_player(player)
        self.update_selected_listbox(self.selected_team1_listbox_frame, self.team1.players, self.remove_player_from_team1)
        self.update_trade_summary()

    # Method to add a player to Team 2
    def add_player_to_team2(self, player):
        self.team2.add_player(player)
        self.update_selected_listbox(self.selected_team2_listbox_frame, self.team2.players, self.remove_player_from_team2)
        self.update_trade_summary()

    # Method to remove a player from Team 1
    def remove_player_from_team1(self, player):
        self.team1.remove_player(player)
        self.update_selected_listbox(self.selected_team1_listbox_frame, self.team1.players, self.remove_player_from_team1)
        self.update_trade_summary()

    # Method to remove a player from Team 2
    def remove_player_from_team2(self, player):
        self.team2.remove_player(player)
        self.update_selected_listbox(self.selected_team2_listbox_frame, self.team2.players, self.remove_player_from_team2)
        self.update_trade_summary()

    # Method to update the selected players listbox
    def update_selected_listbox(self, frame, players, remove_callback):
        for widget in frame.winfo_children():
            widget.destroy()
        for player in players:
            player_frame = tk.Frame(frame)
            label = tk.Label(player_frame, text=f"{player.name} ({player.team}) - {player.value}")
            button = tk.Button(player_frame, text="Remove", command=lambda p=player: remove_callback(p))
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            button.pack(side=tk.RIGHT)
            player_frame.pack(fill=tk.X)

    # Method to update the trade summary
    def update_trade_summary(self):
        # Ensure that the trade summary is updated correctly when players are added or removed from either team
        players_from_team1 = self.team1.players
        players_from_team2 = self.team2.players

        # Analyze the trade considering all selected players for both teams
        result = analyze_trade(self.team1, self.team2, players_from_team1, players_from_team2)

        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, f"{result['favored_team']} is favored by {result['points']} points\n")

        # Update the favored team indicator
        canvas_width = self.favored_team_canvas.winfo_width()
        if canvas_width > 0:
            midpoint = canvas_width / 2
            max_points = max(result['points'], 1)  # Avoid division by zero
            offset = (result['points'] / max_points) * (midpoint - 10)
            if result['favored_team'] == "Team 1":
                x1 = midpoint - offset
                x2 = midpoint
            else:
                x1 = midpoint
                x2 = midpoint + offset
            self.favored_team_canvas.coords(self.favored_team_indicator, x1, 0, x2, 20)

            # Change color based on fairness
            if abs(result['points']) < 5:  # Adjust threshold as needed
                self.favored_team_canvas.itemconfig(self.favored_team_indicator, fill="green")
            else:
                self.favored_team_canvas.itemconfig(self.favored_team_indicator, fill="red")

    # Method to reset the trade
    def reset_trade(self):
        self.team1.players.clear()
        self.team2.players.clear()
        self.update_selected_listbox(self.selected_team1_listbox_frame, self.team1.players, self.remove_player_from_team1)
        self.update_selected_listbox(self.selected_team2_listbox_frame, self.team2.players, self.remove_player_from_team2)
        self.summary_text.delete(1.0, tk.END)
        self.favored_team_canvas.coords(self.favored_team_indicator, self.favored_team_canvas.winfo_width() / 2 - 10, 0, self.favored_team_canvas.winfo_width() / 2 + 10, 20)
        self.favored_team_canvas.itemconfig(self.favored_team_indicator, fill="red")

# Run the application if this script is executed
if __name__ == "__main__":
    root = tk.Tk()
    app = TradeAnalyzerApp(root)
    root.mainloop()