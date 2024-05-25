import pygame, sys, time, random, json, tkinter, os

leaderboard_file = 'leaderboard.json'
if not os.path.exists(leaderboard_file):
    with open(leaderboard_file, 'w') as file:
        json.dump([], file)

# Difficulties
DIFFICULTY_EASY = 10
DIFFICULTY_MEDIUM = 15
DIFFICULTY_HARD = 20
DIFFICULTY_HARDER = 30
DIFFICULTY_IMPOSSIBLE = 100

# Difficulty settings
difficulty = DIFFICULTY_EASY

frame_size_x = 720
frame_size_y = 480

check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(255, 165, 0)
# green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


fps_controller = pygame.time.Clock()

snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('GAME OVER', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    enter_name()

# Load leaderboard data
def load_leaderboard(file_path='leaderboard.json'):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save leaderboard data
def save_leaderboard(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Add entry to leaderboard and sort by score
def add_entry(name, score, file_path='leaderboard.json'):
    if name == "":
        return
    leaderboard = load_leaderboard(file_path)
    leaderboard.append({'name': name, 'score': score})
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    save_leaderboard(file_path, leaderboard)

def enter_name():
    root = tkinter.Tk()
    root.title("Rangliste")
    center_window(root, 300, 200)

    label = tkinter.Label(root, text="Gebe deinen Namen ein:")
    label.pack(padx=20, pady=(20, 0))

    entry = tkinter.Entry(root)
    entry.pack(padx=20, pady=(0, 20))

    button = tkinter.Button(root, text="Submit", command=lambda: on_submit(entry.get(), score, root))
    button.pack(pady=(0, 20))

    root.mainloop()

def on_submit(name, score, root):
    add_entry(name, score)
    show_leaderboard(root)

def show_leaderboard(root):
    for widget in root.winfo_children():
        widget.destroy()

    leaderboard = load_leaderboard()
    string = ""

    for index, entry in enumerate(leaderboard, start=1):
        if index <= 10:
            string += f"{index}. {entry['name']} - {entry['score']}\n"

    new_label = tkinter.Label(root, text=string.strip())
    new_label.pack(padx=20, pady=20)

# Center tkinter window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)

idle = True

# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
                idle = False
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
                idle = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
                idle = False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
                idle = False
            if event.key == ord('x'):
                idle = True
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if idle == True and direction == "RIGHT":
        change_to = "DOWN"
    if idle == True and direction == "DOWN":
        change_to = "LEFT"
    if idle == True and direction == "LEFT":
        change_to = "UP"
    if idle == True and direction == "UP":
        change_to = "RIGHT"

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    # The snake
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Game Over conditions
    
    # Getting out of bounds
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
        game_over()
    
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'consolas', 20)
    
    # Refresh game screen
    pygame.display.update()

    match score:
        case 10: 
            difficulty = DIFFICULTY_MEDIUM
        case 20: 
            difficulty = DIFFICULTY_HARD
        case 50: 
            difficulty = DIFFICULTY_HARDER
        case 100: 
            difficulty = DIFFICULTY_IMPOSSIBLE
    # Refresh rate
    fps_controller.tick(difficulty)