import tkinter as tk
import random

# TODO ideas:
# - standardize naming to snake case
# - move hardcoded values to uppercase constants
# - don't use `global` :)
# - I'd use `numpy` to deal with performance issues

N = 15
M = 30

time = 0
number_of_mines = 0
number_of_flags = number_of_mines
number_of_hitted_mines = 0

save_time = 0

if_end_game = False

score_save = ""

# CONSTANTS:
ASSETS_FILEPATH = "./assets/"
RESULTS_FILEPATH = "wyniki.txt"

try:
    with open(RESULTS_FILEPATH, mode="r") as score_txt:
        # Opens txt file with scoreboard

        for line in sorted(score_txt):
            score_save += line
except FileNotFoundError:
    open(RESULTS_FILEPATH, "a").close()


def window():
    # Main root for window

    root = tk.Tk()
    root.geometry("390x250")
    root.title("saper")

    return root


def startWindow(game_difficulty):
    # Window suitable for starting scene where you choose game difficulty and can see a scoreboard

    game_difficulty.pack(fill="both", expand=1)
    game.forget()
    scores.forget()
    root.geometry("390x250")
    text = tk.Label(game_difficulty, font=("Digital-7", 20))
    text.grid(row=0, column=0, pady=10, padx=10)
    text["text"] = "Wybierz poziom trudności gry"

    easy = tk.Button(game_difficulty, command=easyDifficulty)
    easy.grid(row=10, column=0, ipadx=25, padx=0, pady=5)
    easy["text"] = "Łatwy"

    medium = tk.Button(game_difficulty, command=mediumDifficulty)
    medium.grid(row=20, column=0, ipadx=25, padx=0, pady=5)
    medium["text"] = "Średni"

    hard = tk.Button(game_difficulty, command=hardDifficulty)
    hard.grid(row=30, column=0, ipadx=25, padx=0, pady=5)
    hard["text"] = "Trudny"

    scoreboard = tk.Button(game_difficulty, command=showScore)
    scoreboard.grid(row=40, column=0, ipadx=25, padx=0, pady=5)
    scoreboard["text"] = "Tabela wynikow"

    startowy_panel = [text, easy, medium, hard]
    return startowy_panel


def easyDifficulty():
    # Sets number of mines for easy difficulty

    global number_of_mines
    number_of_mines = 20
    choose_difficulty.forget()
    scores.forget()
    game.pack(fill="both", expand=1)
    root.geometry("850x550")
    upper_panel[1]["image"] = icons["buzki"][0]
    buttons = board(game, upper_panel, icons)

    global if_end_game
    if_end_game = False

    global time
    time = 0

    global number_of_flags
    number_of_flags = number_of_mines
    update_number_of_mines(upper_panel[0])


def mediumDifficulty():
    # Sets number of mines for medium difficulty

    global number_of_mines
    number_of_mines = 45
    choose_difficulty.forget()
    scores.forget()
    game.pack(fill="both", expand=1)
    root.geometry("850x550")
    upper_panel[1]["image"] = icons["buzki"][0]
    buttons = board(game, upper_panel, icons)

    global if_end_game
    if_end_game = False

    global time
    time = 0

    global number_of_flags
    number_of_flags = number_of_mines
    update_number_of_mines(upper_panel[0])


def hardDifficulty():
    # Sets number of mines for hard difficulty

    global number_of_mines
    number_of_mines = 70
    choose_difficulty.forget()
    scores.forget()
    game.pack(fill="both", expand=1)
    root.geometry("850x550")
    upper_panel[1]["image"] = icons["buzki"][0]
    buttons = board(game, upper_panel, icons)

    global if_end_game
    if_end_game = False

    global time
    time = 0

    global number_of_flags
    number_of_flags = number_of_mines
    update_number_of_mines(upper_panel[0])


def scoreTabel(scores, score_save):
    # Window showing scoreboard

    game.forget()
    scores.forget()
    choose_difficulty.pack(fill="both", expand=1)
    text = tk.Label(scores, font=("Digital-7", 10))
    text.grid(pady=10, padx=20)
    text["text"] = score_save

    back_button = tk.Button(scores, command=showStartingWindow)
    back_button.grid(padx=M // 2 - 1, pady=5)
    back_button["text"] = "Powrot do głównego okna"

    panel = [text, back_button]
    return panel


def showScore():
    # Button to change from starting window to scoreboard window

    scores.pack(fill="both", expand=1)
    game.forget()
    choose_difficulty.forget()
    root.geometry("300x500")


def showStartingWindow():
    # Responsible for changing screen from game or scoreboard to starting window with difficulty options

    choose_difficulty.pack(fill="both", expand=1)
    game.forget()
    scores.forget()
    root.geometry("390x250")


def upperPanel(game, icons):
    # Panel in main game window showing number of bombs, timer and central smiley face

    number_of_mines = tk.Label(game, bg="black", fg="red", font=("Digital-7", 40))
    number_of_mines.grid(row=0, column=0, columnspan=7, ipadx=10, pady=30)
    update_number_of_mines(number_of_mines)

    smiley_face = tk.Button(game)
    smiley_face.grid(row=0, column=M // 2 - 1, columnspan=3, pady=30)
    smiley_face["image"] = icons["buzki"][0]

    timer = tk.Label(game, bg="black", fg="red", font=("Digital-7", 40))
    timer.grid(row=0, column=M - 6, columnspan=7, ipadx=10, pady=30)
    updateTimer(game, timer)

    upper_panel = [number_of_mines, smiley_face, timer]

    return upper_panel


def board(game, upper_panel, icons):
    # Main board responsible for placing buttons with bombs

    buttons = [tk.Button(game, image=icons["tlo"]) for i in range(N * M)]

    game_table = gameTable()

    for i in range(N):
        for j in range(M):
            placeButtonOnSquare(buttons, j, i)
            buttons[i * M + j].bind(
                "<Button-1>",
                lambda event, p=buttons[i * M + j]: leftClick(
                    buttons, p, upper_panel, game_table, icons
                ),
            )
            buttons[i * M + j].bind(
                "<Button-3>",
                lambda event, p=buttons[i * M + j]: rightClick(
                    buttons, p, upper_panel, game_table, icons
                ),
            )
            buttons[i * M + j].bind(
                "<ButtonRelease>", lambda event: normalFace(upper_panel[1])
            )

    return buttons


def where_neighbors(table, x, y):
    # Creates chart showing how many bombs are near every square(button)

    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                if 0 <= y + i < N:
                    if 0 <= x + j < M:
                        neighbors.append((x + j, y + i))

    return neighbors


def gameTable():
    # Placing bombs on board

    game_table = [[0 for j in range(M)] for i in range(N)]

    l_min = number_of_mines

    while l_min:
        x = random.randint(0, M - 1)
        y = random.randint(0, N - 1)

        if game_table[y][x] == 0:
            game_table[y][x] = "x"
            l_min -= 1

    for i in range(N):
        for j in range(M):
            if game_table[i][j] == 0:
                neighbors = where_neighbors(game_table, j, i)

                l_min = 0

                for x, y in neighbors:
                    if game_table[y][x] == "x":
                        l_min += 1

                game_table[i][j] = l_min

    return game_table


def updateTimer(game, timer):
    # Adds time to timer in the upper panel in main game

    global time
    time += 1
    timer["text"] = "0" * (4 - len(str(time))) + str(time)
    game.after(1000, updateTimer, game, timer)


def update_number_of_mines(count_mines):
    # Sets number of mines in the upper panel

    count_mines["text"] = "0" * (4 - len(str(number_of_mines))) + str(number_of_mines)


def normalFace(smiley):
    # Function to place smiley face on the upper panel

    if not if_end_game:
        upper_panel[1]["image"] = icons["buzki"][0]


def loadIcons():
    # Loads icons

    icons = {}

    icons["cyfry"] = [
        tk.PhotoImage(file=ASSETS_FILEPATH + str(i) + ".png") for i in range(1, 9)
    ]
    icons["buzki"] = [
        tk.PhotoImage(file=ASSETS_FILEPATH + "buzka" + str(i) + ".png")
        for i in range(1, 5)
    ]
    icons["flaga"] = tk.PhotoImage(file=ASSETS_FILEPATH + "flaga.png")
    icons["miny"] = [
        tk.PhotoImage(file=ASSETS_FILEPATH + "mina.png"),
        tk.PhotoImage(file=ASSETS_FILEPATH + "pierwsza.png"),
    ]

    icons["tlo"] = [tk.PhotoImage(file=ASSETS_FILEPATH + "tlo.png")]
    return icons


def placeButtonOnSquare(buttons, x, y):
    # Placeing clicable buttons on main board

    if x == 0:
        buttons[y * M + x].grid(row=y + 1, column=x, padx=(30, 0))

    else:
        buttons[y * M + x].grid(row=y + 1, column=x)


def gameLost(buttons, game_table, icons):
    # Responsible for when game is lost

    global if_end_game

    if_end_game = True

    for i in range(N):
        for j in range(M):
            if (
                isinstance(buttons[i * M + j], tk.Button)
                and buttons[i * M + j]["state"] != "disabled"
            ):
                buttons[i * M + j]["state"] = "disabled"
                buttons[i * M + j].unbind("<Button-1>")
                buttons[i * M + j].unbind("<Button-3>")

                if game_table[i][j] == "x":
                    buttons[i * M + j] = tk.Label(game, image=icons["miny"][0])
                    placeButtonOnSquare(buttons, j, i)


def ifGameWon(buttons, game_table):
    # Responsible for when game is won

    global if_end_game, score_save

    if_end_game = True

    with open(RESULTS_FILEPATH, mode="a+") as save:
        save.write(
            "Wygrana gra z czasem: "
            + str(time)
            + " Liczba min: "
            + str(number_of_mines)
            + "\n"
        )

    for i in range(N):
        for j in range(M):
            if (
                isinstance(buttons[i * M + j], tk.Button)
                and buttons[i * M + j]["state"] != "disabled"
            ):
                buttons[i * M + j]["state"] = "disabled"
                buttons[i * M + j].unbind("<Button-1>")
                buttons[i * M + j].unbind("<Button-3>")
    for linijka in score_txt.readlines():
        score_save += linijka


def updateButtons(buttons, button, index, field, game_table, icons):
    # Function responsible for what happens when button pressed on board

    buttons[index].configure(state="disabled", border=1, highlightbackground="black")
    buttons[index].unbind("<Button-1>")
    buttons[index].unbind("<Button-3>")

    if field != "x":
        if field != 0:
            buttons[index] = tk.Label(game, image=icons["cyfry"][field - 1])
            placeButtonOnSquare(buttons, index % M, index // M)

        else:
            neighbors = where_neighbors(game_table, index % M, index // M)

            for x, y in neighbors:
                if (
                    isinstance(buttons[y * M + x], tk.Button)
                    and buttons[y * M + x]["state"] != "disabled"
                ):
                    updateButtons(
                        buttons,
                        button,
                        y * M + x,
                        game_table[y][x],
                        game_table,
                        icons,
                    )


def leftClick(buttons, button, upper_panel, game_table, icons):
    # Function to make left mouse button working to uncover board

    upper_panel[1]["image"] = icons["buzki"][1]

    indeks = buttons.index(button)
    pole = game_table[indeks // M][indeks % M]

    if pole == "x":
        upper_panel[1]["image"] = icons["buzki"][2]
        gameLost(buttons, game_table, icons)

    else:
        updateButtons(buttons, button, indeks, pole, game_table, icons)


def rightClick(buttons, button, upper_panel, game_table, icons):
    # Function to make right mouse button working to place a flag

    upper_panel[1]["image"] = icons["buzki"][1]

    index = buttons.index(button)
    field = game_table[index // M][index % M]

    global number_of_flags
    global number_of_hitted_mines
    global number_of_mines

    if button.cget("image") == str(icons["flaga"]):
        button["image"] = icons["tlo"]
        number_of_flags += 1
        number_of_mines += 1
        if field == "x":
            number_of_hitted_mines -= 1

    else:
        button["image"] = icons["flaga"]
        number_of_flags -= 1
        number_of_mines -= 1
        if field == "x":
            number_of_hitted_mines += 1
            if number_of_hitted_mines == number_of_mines:
                upper_panel[1]["image"] = icons["buzki"][3]
                ifGameWon(buttons, game_table)

    update_number_of_mines(upper_panel[0])


def restartGame(game, upper_panel, icons):
    # Restarts game and changing from game window to starting window

    upper_panel[1]["image"] = icons["buzki"][0]
    buttons = board(game, upper_panel, icons)

    global if_end_game
    if_end_game = False

    global time
    time = 0

    global number_of_flags
    number_of_flags = number_of_mines
    update_number_of_mines(upper_panel[0])

    global score_save
    with open(RESULTS_FILEPATH, mode="r") as scores_txt:
        for line in sorted(scores_txt):
            score_save += line

    startWindow(choose_difficulty)


if __name__ == "__main__":
    # Main to activate functions for game to start and work
    root = window()

    scores = tk.Frame(root)
    game = tk.Frame(root)
    choose_difficulty = tk.Frame(root)

    startWindow(choose_difficulty)

    icons = loadIcons()

    upper_panel = upperPanel(game, icons)

    buttons = board(game, upper_panel, icons)

    scores_tabel = scoreTabel(scores, score_save)

    upper_panel[1].bind(
        "<Button-1>", lambda event: restartGame(game, upper_panel, icons)
    )

    root.mainloop()
