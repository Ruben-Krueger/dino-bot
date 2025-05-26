import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from dino_player import DinoPlayer

class DinoGameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chrome Dino Game Interface")
        self.root.geometry("1000x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create stats frame
        self.stats_frame = ttk.LabelFrame(self.main_frame, text="Game State", padding="5")
        self.stats_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N))
        
        # Add dino position label
        self.dino_pos_label = ttk.Label(self.stats_frame, text="Dino position: N/A")
        self.dino_pos_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.dino_obstacles_count_label = ttk.Label(self.stats_frame, text="Obstacles: N/A")
        self.dino_obstacles_count_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        
        # Create and configure log display
        self.log_frame = ttk.LabelFrame(self.main_frame, text="Game Log", padding="5")
        self.log_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_display = scrolledtext.ScrolledText(self.log_frame, width=40, height=20)
        self.log_display.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create control buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(self.button_frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(self.button_frame, text="Stop Game", command=self.stop_game, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Game instance
        self.game = None
        self.game_thread = None
        self.running = False
        
    def log_message(self, message):
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.see(tk.END)
        

    def update_dino_position(self, coordinates):
        self.dino_pos_label.config(text=f"Dino position: {coordinates}")

    def run_game(self):
        self.game = DinoPlayer(ui_callback=self.log_message)
        self.game.start_game()
        self.game.play_game()
        
        
    def start_game(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.log_message("Starting game...")
        

        self.game_thread = threading.Thread(target=self.run_game)
        self.game_thread.start()
        
    def stop_game(self):
        self.running = False
        if self.game:
            self.game.stop_game()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log_message("Game stopped.")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ui = DinoGameUI()
    ui.run() 