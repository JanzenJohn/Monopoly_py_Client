import random
import Network
import os
from _thread import *
import pygame

n = Network.Network()

class render_store:
    def __init__(self):
        self.board = "not filled"
        self.users = "not filled"
        self.default = 13

rs = render_store()
def Client():
    while True:
        try:
            message, is_req = n.recv()
        except BrokenPipeError as e:
            print(e)
            print("exit")
        except EOFError as e:
            print("Server stopped responding")
            exit()
        if is_req and message != "OS":
            reply = input(str(message) + " : ")
            n.send("str", reply)
        elif is_req:
            n.send("str", str("GUI 1.0"))
        elif message == "you won":
            print("You won")
            exit()
        elif message == "BOARD":
            print("BOARD INCOMING")
            rs.board, rec = n.recv()
            rs.users, rec = n.recv()
            print(rs.board)
            print(rs.users)
            print("BOARD DONE")
        elif message == "you loose":
            print("The game is over and you didn't win")
            exit()
        else:
            print(message)

start_new_thread(Client, ())
print("what")
pygame.init()
x_size = 800
y_size = 800
amount = 13
pygame.display.set_caption("Gclient")
clock = pygame.time.Clock()
scaler_value = min(x_size, y_size)


def draw_base():
    use_colors = True
    if type(rs.board) == list:
        amount = int(len(rs.board)/4)+2
    else:
        amount = rs.default
        use_colors = False
    field_texture_blank = pygame.Surface((scaler_value / amount, (scaler_value / amount) * 2))
    field_texture_blank.fill((255, 255, 255))
    field_seperator = pygame.Surface((5, (scaler_value/amount) * 2))
    field_seperator.fill((0, 0, 0))
    field_lenght = scaler_value/amount
    for side in range(2):
        if side % 2 == 0:
            field_texture_blank = pygame.transform.rotate(field_texture_blank, 90)
            field_seperator = pygame.transform.rotate(field_seperator, 90)
            for field_id in range(amount):

                if field_id > 1 and field_id < amount - 2:
                    col = (145, 242, 126)
                    field_texture_blank.fill(col)
                    screen.blit(field_texture_blank, (0, (scaler_value / amount) * field_id))
                    screen.blit(field_seperator, (0, (scaler_value / amount) * field_id - 1))
                    screen.blit(field_texture_blank, (scaler_value-(field_lenght*2), (scaler_value / amount) * field_id))
                    screen.blit(field_seperator, (scaler_value-(field_lenght*2), (scaler_value / amount) * field_id-1))
        else:
            field_texture_blank = pygame.transform.rotate(field_texture_blank, 90)
            field_seperator = pygame.transform.rotate(field_seperator, 90)
            for field_id in range(amount):
                if field_id > 1 and field_id < amount - 2:
                    col = (145, 242, 126)
                    field_texture_blank.fill(col)
                    screen.blit(field_texture_blank, (field_lenght * field_id, scaler_value - field_lenght * 2))
                    screen.blit(field_seperator, (field_lenght * field_id - 1, scaler_value - field_lenght * 2))
                    screen.blit(field_texture_blank, (field_lenght * field_id, 0))
                    screen.blit(field_seperator, (field_lenght * field_id - 1, 0))
    go_text = pygame.Surface((field_lenght*2, field_lenght*2))
    prison_text = pygame.Surface((field_lenght + 1, field_lenght + 1))
    prison_text.fill((23,24,24))
    go_text.fill((145, 242, 126))
    screen.blit(go_text, (0, 0))
    screen.blit(prison_text, (scaler_value/amount, scaler_value/amount))
    screen.blit(go_text, (scaler_value-field_lenght*2, 0))
    screen.blit(go_text, (0, scaler_value-field_lenght*2))
    screen.blit(go_text, (scaler_value-field_lenght*2, scaler_value-field_lenght*2))
    field_seperator = pygame.transform.rotate(field_seperator, 90)
    screen.blit(field_seperator, (0, scaler_value - scaler_value / amount * 2 - 1))
    screen.blit(field_seperator, (scaler_value-scaler_value/amount*2, scaler_value - scaler_value / amount * 2 - 1))
    field_seperator = pygame.transform.rotate(field_seperator, 90)
    screen.blit(field_seperator, (scaler_value-scaler_value/amount*2 - 2, 0))
    screen.blit(field_seperator, (scaler_value - scaler_value / amount * 2 - 2, scaler_value-scaler_value/amount*2))

def assign_color(id, colors):
    colors[id] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_x_y(player, range_x , range_y):
    try:
        x = player.x
        y = player.y
    except AttributeError:
        x = random.randint(int(range_x[0]), int(range_x[1]))
        y = random.randint(int(range_y[0]), int(range_y[1]))
        player.x = x
        player.y = y

    return x, y
def draw_players(players, colors):
    if type(rs.board) == list:
        amount = int(len(rs.board)/4)+2
    else:
        amount = rs.default
    player_texuture = pygame.Surface(((scaler_value/amount)/4, (scaler_value/amount)/4))
    for player in players:
        try:
            color = colors[player.id]
        except KeyError:
            assign_color(player.id, colors)
        except AttributeError:
            return
        player_texuture.fill(colors[player.id])
        pos = player.position
        if player.in_prison:
            x, y = get_x_y(player,
                           (scaler_value/amount, scaler_value/amount*2),
                           (scaler_value/amount, scaler_value/amount*2)
                           )
        elif pos == 0:
            x, y = get_x_y(player,
                           (0, (int(scaler_value / amount) * 2)-scaler_value/amount/2),
                           (scaler_value - int(scaler_value / amount * 2),int(scaler_value - scaler_value / amount / 2)))

        elif 0 < pos < amount-3:
            x, y = get_x_y(player,
                           (0, (scaler_value/amount*2)-scaler_value/amount/2),
                           (0,scaler_value/amount/2)
                           )
            r_pos = amount - 4 - pos
            y += (scaler_value / amount) * 2
            y += (scaler_value/amount)*r_pos

        elif pos == amount-3:
            x, y = get_x_y(player,
                           (0, (scaler_value/amount)*1.5),
                           (0, (scaler_value/amount)))
        elif amount-3 < pos < amount*2 - 6:
            x, y = get_x_y(player,
                           (0, (scaler_value/amount/2)),
                           (0, (scaler_value/amount))
                            )
            x += (scaler_value/amount)*(pos-amount+4)

        elif pos == amount*2 - 6:
            x, y = get_x_y(player,
                           (scaler_value-((scaler_value/amount)*2), scaler_value-scaler_value/amount/2),
                           (0, (scaler_value/amount)*1.5))
        elif amount*2 -6 < pos < amount*3 -9:
            x, y = get_x_y(player,
                           ((scaler_value-((scaler_value/amount)*2))+(scaler_value/amount/2), scaler_value-scaler_value/amount/2),
                           (0, scaler_value/amount/2))
            y += (scaler_value/amount)*(pos-(amount*2-6)+1)
        elif pos == amount*3-9:
            x, y = get_x_y(player,
                           (scaler_value-(scaler_value/amount)*2, scaler_value-scaler_value/amount/2),
                           (scaler_value-(scaler_value/amount)*2, scaler_value-scaler_value/amount/2)
                           )
        elif amount*3-9 < pos < amount*4-12:
            x, y = get_x_y(player,
                           (scaler_value-scaler_value/amount, scaler_value-scaler_value/amount/2),
                           (scaler_value-(scaler_value/amount)*1.5, scaler_value-scaler_value/amount/2)
                           )
            e = (pos-(amount*3-6))+4
            x -= (scaler_value/amount)*e
        elif pos == amount*4-12:
            x, y = get_x_y(player,
                           (0, (int(scaler_value / amount) * 2) - scaler_value / amount / 2),
                           (scaler_value - int(scaler_value / amount * 2), int(scaler_value - scaler_value / amount / 2))
                           )
        try:
            coords = (x, y)
            screen.blit(player_texuture, coords)
        except:
            pass


colors = {}
while True:
    screen = pygame.display.set_mode((x_size, y_size))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()

    screen.fill((0,0,20))
    draw_base()
    players = rs.users

    draw_players(players, colors)
    pygame.display.update()


    clock.tick(60)


