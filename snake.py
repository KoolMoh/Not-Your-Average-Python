import tkinter as tk
import random
import json

WIN_WIDTH = 1140
WIN_HEIGHT = 760

class Game(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("Not Your Average Python")
    self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
    self.resizable(False, False)

    self.gameIcon = tk.PhotoImage(file="assets/icon.png")
    self.iconphoto(True, self.gameIcon)
    
    container = tk.Frame(self)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)
    
    self.bg_photo = tk.PhotoImage(file='assets/bg.png')
    
    self.load_settings()
    
    self.frames = {}
      
    for F in (WelcomeScreen, GameScreen, LeaderboardScreen, SettingsScreen):
      frame = F(container, self)
      self.frames[F] = frame
      frame.grid(row=0, column=0, sticky="nsew")
    
    self.show_frame(WelcomeScreen)
  
  def show_frame(self, screen):
    frame = self.frames[screen]
    frame.tkraise()
    if screen == LeaderboardScreen:
      frame.refresh_leaderboard()
  
  def load_settings(self):
    try:
      with open('settings.json', 'r') as f:
        self.settings = json.load(f)
    except FileNotFoundError:
      settings = {"difficulty": "Normal", "leaderboard": []}
      self.save_settings(settings)
  
  def save_settings(self, settings):
    with open('settings.json', 'w') as f:
      json.dump(settings, f)
    self.settings = settings

class WelcomeScreen(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller
    
    self.canvas = tk.Canvas(self, width=WIN_WIDTH, height=WIN_HEIGHT)
    self.canvas.pack(fill="both", expand=True)
    self.canvas.create_image(0, 0, image=self.controller.bg_photo, anchor="nw")
    
    label = tk.Label(
      self.canvas, 
      text="🐍 Not Your Average Python 🐍", 
      fg='white',
      bg='#88c550', 
      font="Arial 25 bold"
    )
    label.place(relx=0.5, rely=0.25, anchor='center')
    
    self.play_btn = tk.Button(
      self.canvas, 
      text="Play", 
      bg='green',
      fg='white',
      width=30,
      height=1,
      font="Arial 15 bold",
      activebackground="light green",
      command=lambda: self.controller.show_frame(GameScreen)
    )

    self.leaderboard_btn = tk.Button(
      self.canvas, 
      text="Leaderboard", 
      bg='green',
      fg='white',
      width=30,
      height=1,
      font="Arial 15 bold",
      activebackground="light green",
      command=lambda: self.controller.show_frame(LeaderboardScreen)
    )

    self.settings_btn = tk.Button(
      self.canvas, 
      text="Settings", 
      bg='green',
      fg='white',
      width=30,
      height=1,
      font="Arial 15 bold",
      activebackground="light green",
      command=lambda: self.controller.show_frame(SettingsScreen)
    )
    
    self.play_btn.place(relx=0.5, rely=0.4, anchor='center')
    self.leaderboard_btn.place(relx=0.5, rely=0.5, anchor='center')
    self.settings_btn.place(relx=0.5, rely=0.6, anchor='center')

class LeaderboardScreen(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller
    
    self.canvas = tk.Canvas(self, width=WIN_WIDTH, height=WIN_HEIGHT)
    self.canvas.pack(fill="both", expand=True)
    self.canvas.create_image(0, 0, image=self.controller.bg_photo, anchor="nw")

    back_button = tk.Button(
      self.canvas, 
      text="<< Back",
      fg='white',
      bg='green',
      font="Arial 10 bold",
      command=lambda: controller.show_frame(WelcomeScreen)
    )
    back_button.place(relx=0, rely=0, x=20, y=20, anchor='nw')

    self.label = tk.Label(
      self.canvas, 
      text="Leaderboard", 
      fg='white',
      bg='#88c550', 
      font="Arial 25 bold"
    )
    self.label.place(relx=0.5, rely=0.2, anchor='center')

    self.container = tk.Frame(self.canvas, bg='#88c550')
    self.container.grid(row=0, column=0, sticky="nsew")
    self.container.columnconfigure(0, weight=1)
    self.container.columnconfigure(1, weight=1)
    self.container.place(relx=0.5, rely=0.5, anchor='center')

    self.update_labels()

  def update_labels(self):
    for widget in self.container.grid_slaves():
      widget.destroy()

    data = self.controller.settings['leaderboard']
    for i, (name, score) in enumerate(data):
      label1 = tk.Label(self.container, text=f"{i+1}. {name}", bg="lightblue", font=("Arial", 14))
      label2 = tk.Label(self.container, text=f"{score}", bg="lightgreen", font=("Arial", 14))
      label1.grid(row=i, column=0, sticky="w", padx=(10, 100))
      label2.grid(row=i, column=1, sticky="e", padx=(100, 10))

  def refresh_leaderboard(self):
    self.controller.settings['leaderboard'].sort(key=lambda x: x[1], reverse=True)
    print(self.controller.settings['leaderboard'])
    self.update_labels()

class SettingsScreen(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller
    
    self.canvas = tk.Canvas(self, width=WIN_WIDTH, height=WIN_HEIGHT)
    self.canvas.pack(fill="both", expand=True)
    self.canvas.create_image(0, 0, image=self.controller.bg_photo, anchor="nw")

    back_button = tk.Button(
      self.canvas, 
      text="<< Back",
      fg='white',
      bg='green',
      font="Arial 10 bold",
      command=lambda: controller.show_frame(WelcomeScreen)
    )
    back_button.place(relx=0, rely=0, x=20, y=20, anchor='nw')
    
    label = tk.Label(
      self.canvas, 
      text="Game Settings", 
      fg='white',
      bg='#88c550', 
      font="Arial 25 bold"
    )
    label.place(relx=0.5, rely=0.25, anchor='center')
    
    container = tk.Frame(self.canvas, bg='#88c550')
    container.place(relx = 0.5, rely = 0.5, anchor = "center")
    
    label = tk.Label(
      container, 
      text="Game Difficulty:", 
      fg='white',
      bg='#88c550', 
      font="Arial 20 bold",
      padx=10
    )
    label.pack(side=tk.LEFT)

    with open('settings.json') as f:
      settings = json.load(f)
    difficulty = settings['difficulty']
    self.diff_btns = {}
    for diff in ['Easy', 'Normal', 'Hard']:
      button = tk.Button(
        container, 
        text=diff.title(), 
        width=10,
        command=lambda d=diff: self.set_diff(d)
      )

      if difficulty == diff:
        button.config(bg='green')

      button.pack(side=tk.LEFT, padx=5)
      self.diff_btns[diff] = button

  def set_diff(self, difficuilty):
    for (diff, btn) in self.diff_btns.items():
      if diff == difficuilty:
        btn['bg'] = 'green'
      else:
        btn['bg'] = 'white'
    settings = self.controller.settings
    settings['difficulty'] = difficuilty
    self.controller.save_settings(settings)

class GameScreen(tk.Frame):
  def __init__(self, parent, controller):
    super().__init__(parent)
    self.controller = controller
    
    self.canvas = tk.Canvas(self, width=WIN_WIDTH, height=WIN_HEIGHT)
    self.canvas.pack(fill="both", expand=True)
    self.canvas.create_image(0, 0, image=self.controller.bg_photo, anchor="nw")

    self.playground = tk.Canvas(self.canvas, width=700, height=500, bg='#c2b280')
    self.playground.place(relx=0.5, rely=0.5, y=40, anchor='center')

    self.snake = [(10, 10), (9, 10), (8, 10), (7, 10), (6, 10)]
    self.direction = 'Right'
    self.running = False
    self.game_started = False
    self.paused = False
    self.score = 0
    self.food = -1, -1
    self.power_up = []

    self.game_screen_label = tk.Label(
      self.canvas, 
      text=f"Score: {self.score}", 
      fg='white',
      bg='#88c550', 
      font="Arial 25 bold"
    )
    self.game_screen_label.place(relx=0.5, rely=0.1, anchor='center')

    for part in self.snake:
      x, y = part
      self.playground.create_rectangle(
        x * 10, y * 10, x * 10 + 10, y * 10 + 10, fill='green', tags="snake"
      )

    self.bind_all("<KeyPress>", self.on_key_press)

  def on_key_press(self, event):
    if not self.game_started:
      self.game_started = True
      self.start_game()
      self.generate_food()
    if event.keysym in ['Up', 'Down', 'Left', 'Right']:
      if (self.direction == 'Up' and event.keysym != 'Down') or \
          (self.direction == 'Down' and event.keysym != 'Up') or \
          (self.direction == 'Left' and event.keysym != 'Right') or \
          (self.direction == 'Right' and event.keysym != 'Left'):
            self.direction = event.keysym
    elif event.keysym in ['Escape', 'space']:
      self.paused = not self.paused
      if self.paused:
        self.running = False
      else:
        self.running = True
        self.move_snake()

  def start_game(self):
    self.running = True
    diff = self.controller.settings.get('difficulty')
    self.speed = 50 * (1 if diff == 'Normal' else (1.5 if diff == 'Easy' else 0.5))
    
    self.move_snake()

  def move_snake(self):
    if not self.running: return

    head_x, head_y = self.snake[0]
    if self.direction == 'Up':
      head_y -= 1
    elif self.direction == 'Down':
      head_y += 1
    elif self.direction == 'Left':
      head_x -= 1
    elif self.direction == 'Right':
      head_x += 1

    new_head = (head_x, head_y)

    if head_x < 0 or head_x >= 70 or head_y < 0 or head_y >= 50 or new_head in self.snake[1:]:
      self.running = False
      return self.game_over()
    self.snake = [new_head] + self.snake[:-1]

    if new_head == self.food:
      self.snake.append(self.snake[-1])
      self.score += 1
      self.game_screen_label.config(text=f"Score: {self.score}")
      self.playground.delete("food")
      self.generate_food()

    for i, tup in enumerate(self.power_up):
      x, y, item_id = tup
      if (x, y) == new_head:
        del self.power_up[i]
        if len(self.snake) - 10 > 3:
          self.snake = self.snake[:-10]
        else:
          self.snake = self.snake[:3]
        self.playground.delete(item_id)
        break

    self.playground.delete("snake")
    for part in self.snake:
      x, y = part
      self.playground.create_rectangle(
        x * 10, y * 10, x * 10 + 10, y * 10 + 10, fill='green', tags="snake"
      )

    self.after(int(self.speed), self.move_snake)

  def generate_food(self):
    self.food = (random.randint(0, 69), random.randint(0, 49))
    self.playground.create_rectangle(
      self.food[0] * 10, self.food[1] * 10, self.food[0] * 10 + 10, self.food[1] * 10 + 10, fill='red', tags="food"
    )
    
    if random.random() < 0.05:
      self.generate_power_up()

  def generate_power_up(self):
    x, y = random.randint(0, 69), random.randint(0, 49)
    item_id = self.playground.create_rectangle(
      x * 10, y * 10, (x * 10) + 10, (y * 10) + 10, fill='blue', tags="power_up"
    )
    self.power_up.append((x, y, item_id))

  def game_over(self):
    self.game_over_cont = tk.Canvas(self.playground, width= 350, height= 200, bg='#000000')
    self.game_over_cont.place(relx=0.5, rely=0.5, anchor='center')

    label = tk.Label(
      self.game_over_cont, 
      text="Game Over", 
      fg='white',
      bg='#000000', 
      font="Arial 25 bold"
    )
    label.place(relx=0.5, rely=0.25, anchor='center')

    label = tk.Label(
      self.game_over_cont, 
      text=f"Score: {self.score}", 
      fg='white',
      bg='#000000', 
      font="Arial 15 bold"
    )
    label.place(relx=0.5, rely=0.5, anchor='center')

    frame = tk.Frame(self.game_over_cont)
    self.name = tk.StringVar()
    entry = tk.Entry(frame, textvariable=self.name)
    submit = tk.Button(frame, text="Save", command=self.back_btn)

    frame.place(relx=0.5, rely=0.75, anchor='center')
    entry.pack(side='left')
    submit.pack(side='right')

  def back_btn(self):
    settings = self.controller.settings

    foundInd = self.find_player("Player" if not len(self.name.get()) else self.name.get(), settings['leaderboard'])

    if foundInd > 0:
      if settings['leaderboard'][foundInd][1] < self.score:
        settings['leaderboard'][foundInd][1] = self.score
    elif len(settings['leaderboard']) < 10:
      settings['leaderboard'].append(["Player" if not len(self.name.get()) else self.name.get(), self.score])
      settings['leaderboard'].sort(key=lambda x: x[1], reverse=True)
    elif settings['leaderboard'][-1][1] < self.score:
      settings['leaderboard'].append(["Player" if not len(self.name.get()) else self.name.get(), self.score])
      settings['leaderboard'].sort(key=lambda x: x[1], reverse=True)
      settings['leaderboard'].pop()
    self.controller.save_settings(settings)

    self.snake = [(10, 10), (9, 10), (8, 10), (7, 10), (6, 10)]
    self.direction = 'Right'
    self.running = False
    self.game_started = False
    self.paused = False
    self.score = 0
    self.food = -1, -1
    self.power_up = []

    self.game_screen_label.config(text=f"Score: {self.score}")

    for child in self.playground.children:
      self.playground.delete(child)

    for part in self.snake:
      x, y = part
      self.playground.create_rectangle(
        x * 10, y * 10, x * 10 + 10, y * 10 + 10, fill='green', tags="snake"
      )

    self.controller.show_frame(LeaderboardScreen)
    self.game_over_cont.destroy()

  def find_player(self, user, leaderboard):
    for i, (name, score) in enumerate(leaderboard):
      if user == name:
        return i
    return -1

if __name__ == "__main__":
  game = Game()
  game.mainloop()