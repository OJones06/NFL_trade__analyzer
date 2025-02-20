import tkinter as tk
from tkinter import messagebox
from load_players import load_players_from_excel
from trade_analyzer import Team, analyze_trade

class TradeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynasty Football Trade Calculator")
        self.root.geometry("800x600")

        # Title and Subtitle
        tk.Label(root, text="Dynasty Football Trade Calculator", font=("Arial", 20, "bold")).pack(pady=10)
        tk.Label(root, text="Created by: Owen Jones", font=("Arial", 12)).pack(pady=5)

        # Main Frame
        self.main_frame = tk.Frame(root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Search Bar
        self.search_frame = tk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=10)
        tk.Label(self.search_frame, text="Search Player").grid(row=0, column=0, padx=5)
        self.search_entry = tk.Entry(self.search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_player)

        # Player Lists
        self.players_frame = tk.Frame(self.main_frame)
        self.players_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.team1_frame = tk.LabelFrame(self.players_frame, text="Team 1 Gets", padx=10, pady=10)
        self.team1_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        self.team1_listbox = tk.Listbox(self.team1_frame, height=6)
        self.team1_listbox.pack(fill=tk.BOTH, expand=True)

        self.selected_team1_frame = tk.LabelFrame(self.players_frame, text="Team 1 Receives", padx=10, pady=10)
        self.selected_team1_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.selected_team1_listbox = tk.Listbox(self.selected_team1_frame)
        self.selected_team1_listbox.pack(fill=tk.BOTH, expand=True)

        self.selected_team2_frame = tk.LabelFrame(self.players_frame, text="Team 2 Receives", padx=10, pady=10)
        self.selected_team2_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.selected_team2_listbox = tk.Listbox(self.selected_team2_frame)
        self.selected_team2_listbox.pack(fill=tk.BOTH, expand=True)


        # Trade Summary
        self.summary_frame = tk.Frame(self.main_frame)
        self.summary_frame.pack(fill=tk.X, pady=10)
        tk.Label(self.summary_frame, text="Trade Summary", font=("Arial", 14, "bold")).pack()
        self.summary_text = tk.Text(self.summary_frame, height=5, width=80)
        self.summary_text.pack()

        # Favored Team Bar
        self.favored_team_canvas = tk.Canvas(self.main_frame, height=20)
        self.favored_team_canvas.pack(fill=tk.X, pady=10)
        self.favored_team_indicator = self.favored_team_canvas.create_rectangle(0, 0, 0, 20, fill="red")

        # Reset Button
        tk.Button(self.main_frame, text="Reset", command=self.reset_trade).pack(pady=10)

        # Initialize player and team data
        self.players = []
        self.team1 = Team("Team 1")
        self.team2 = Team("Team 2")

        # Load players from Excel
        self.load_players()

    def load_players(self):
        file_path = '/Users/owenjones/Trade_analyzer/NFL_Trade_values_Feb.xlsx'
        try:
            self.players = load_players_from_excel(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load players: {e}")

    def search_player(self, event):
        search_term = self.search_entry.get().lower()
        filtered_players = [player for player in self.players if search_term in player.name.lower()]
        self.update_listboxes(filtered_players)

    def update_listboxes(self, players):
        self.team1_listbox.delete(0, tk.END)
        for player in players:
            self.team1_listbox.insert(tk.END, f"{player.name} ({player.team}) - {player.value}")

    def add_player_to_team(self, team, listbox, player):
        team.add_player(player)
        listbox.insert(tk.END, f"{player.name} ({player.team}) - {player.value}")
        self.update_trade_summary()

    def remove_player_from_team(self, team, listbox, player):
        team.remove_player(player)
        listbox.delete(listbox.get(0, tk.END).index(f"{player.name} ({player.team}) - {player.value}"))
        self.update_trade_summary()

    def update_trade_summary(self):
        result = analyze_trade(self.team1, self.team2, self.team1.players, self.team2.players)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, f"{result['favored_team']} is favored by {result['points']} points\n")

        canvas_width = self.favored_team_canvas.winfo_width()
        if canvas_width > 0:
            midpoint = canvas_width / 2
            offset = (result['points'] / max(abs(result['points']), 1)) * (midpoint - 10)
            x1 = midpoint - offset if result['favored_team'] == "Team 1" else midpoint
            x2 = midpoint if result['favored_team'] == "Team 1" else midpoint + offset
            self.favored_team_canvas.coords(self.favored_team_indicator, x1, 0, x2, 20)
            self.favored_team_canvas.itemconfig(self.favored_team_indicator, fill="green" if abs(result['points']) < 5 else "red")

    def reset_trade(self):
        self.team1.players.clear()
        self.team2.players.clear()
        self.selected_team1_listbox.delete(0, tk.END)
        self.selected_team2_listbox.delete(0, tk.END)
        self.summary_text.delete(1.0, tk.END)
        self.favored_team_canvas.coords(self.favored_team_indicator, self.favored_team_canvas.winfo_width() / 2 - 10, 0, self.favored_team_canvas.winfo_width() / 2 + 10, 20)
        self.favored_team_canvas.itemconfig(self.favored_team_indicator, fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradeAnalyzerApp(root)
    root.mainloop()