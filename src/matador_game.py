import pygame
import numpy as np
import random
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.backend.spiller import Spiller
from src.backend.felt import Felt, Grund
random.seed()

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 1000))
clock = pygame.time.Clock()
running = True
dt = 0
zoom = 1.0
min_zoom = 0.5
max_zoom = 2.5
zoom_focus = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
dragging = False
drag_start_mouse = None
drag_start_focus = None
rotation_angle = 0.0
rotating = False
rotate_start_mouse = None
rotate_start_angle = None

# Player visual config
PLAYER_COLORS = [(0, 200, 255), (255, 80, 80), (80, 255, 80), (255, 200, 50)]
PLAYER_OFFSETS = [(-10, -10), (10, -10), (-10, 10), (10, 10)]
player_radius = 15

# Game state: "WAIT_ROLL", "WAIT_BUY", "GAME_OVER"
game_state = "WAIT_ROLL"
messages = []
MAX_MESSAGES = 8
buy_grund = None

# Pop-up state
popup_open = False
popup_tile = -1
popup_rect = pygame.Rect(0, 0, 400, 350)
popup_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
popup_close_rect = pygame.Rect(0, 0, 30, 30)


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)
GREEN = (0, 128, 0)
PINK = (255, 192, 203)
#CREATE MORE COLORS
MAGENTA = (255, 0, 255)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_YELLOW = (255, 255, 224)
LIGHT_BROWN = (210, 180, 140)


n_brikker = 40


center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def get_tile_screen_center(i):
    """Get the screen-space center of tile i's button."""
    base_radius = np.minimum(screen.get_width(), screen.get_height()) / 2
    board_radius = base_radius * zoom
    inner_radius = board_radius - 200 * zoom
    angle = i * 360 / n_brikker + rotation_angle + 90
    mid_angle = angle + (360 / n_brikker) / 2
    btn_distance = (board_radius + inner_radius) / 2 / zoom
    btn_center_world = center + pygame.Vector2(np.cos(np.radians(mid_angle)), np.sin(np.radians(mid_angle))) * btn_distance * 1.1
    return zoomed(btn_center_world)


def handle_events():
    global running, dragging, drag_start_mouse, drag_start_focus, zoom, zoom_focus
    global rotating, rotate_start_mouse, rotate_start_angle, rotation_angle
    global popup_open, popup_tile
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                popup_open = False
            elif not popup_open:
                if game_state == "WAIT_ROLL" and event.key == pygame.K_SPACE:
                    do_roll()
                elif game_state == "WAIT_BUY":
                    if event.key == pygame.K_j:
                        do_buy(True)
                    elif event.key == pygame.K_n:
                        do_buy(False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse = pygame.Vector2(event.pos)
                # If popup is open, check close button first
                if popup_open:
                    if popup_close_rect.collidepoint(event.pos):
                        popup_open = False
                        continue
                # Check if clicking on a board tile button
                clicked_tile = False
                for i in range(n_brikker):
                    tile_screen = get_tile_screen_center(i)
                    if mouse.distance_to(tile_screen) <= 40 * zoom:
                        popup_open = True
                        popup_tile = i
                        clicked_tile = True
                        break
                if not clicked_tile and not popup_open:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        rotating = True
                        rotate_start_mouse = pygame.Vector2(event.pos)
                        rotate_start_angle = rotation_angle
                    else:
                        dragging = True
                        drag_start_mouse = pygame.Vector2(event.pos)
                        drag_start_focus = zoom_focus.copy()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                rotating = False
        elif event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            old_zoom = zoom
            zoom += event.y * 0.1
            zoom = max(min_zoom, min(max_zoom, zoom))
            if zoom != old_zoom:
                zoom_focus += (mouse_pos - zoom_focus) * (1 - old_zoom / zoom)


def handle_drag():
    global zoom_focus, rotation_angle
    if dragging:
        mouse_now = pygame.Vector2(pygame.mouse.get_pos())
        delta = (drag_start_mouse - mouse_now) / zoom
        zoom_focus = drag_start_focus + delta
    if rotating:
        mouse_now = pygame.Vector2(pygame.mouse.get_pos())
        delta_x = mouse_now.x - rotate_start_mouse.x
        rotation_angle = rotate_start_angle - delta_x * 0.3


def zoomed(pos):
    return zoom_focus + (pos - zoom_focus) * zoom


COLORS = [  RED, LIGHT_BROWN, LIGHT_BROWN, LIGHT_BROWN,
            YELLOW, YELLOW, YELLOW,
            BLACK,
            GRAY, GRAY, GRAY,
            WHITE,
            BLUE, BLUE, BLUE,
            PURPLE, PURPLE, PURPLE,
            RED, RED, RED,
            LIGHT_GREEN,
            WHITE, 
            GREEN, GREEN, GREEN,
            BROWN, BROWN, BROWN,
            PINK, PINK, PINK,
            WHITE,
            MAGENTA, MAGENTA, MAGENTA,
            LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE,
            LIGHT_YELLOW, LIGHT_YELLOW,
        ]

NAMES = ["START", "Østerbrogade", "Grønningen", "Bredgade",
         "Kgs. Nytorv", "Østergade", "Amagertorv",
         "Fængsel",
            "Vesterbrogade", "H.C. Andersens Boulevard", "Rådhuspladsen",
            "Nørrebrogade",
            "Frederiksberg Allé", "Gammel Kongevej", "Valby Langgade",
            "Carlsberg", "Søndre Boulevard",
            "Vesterbro Torv", "Halmtorvet", "Enghave Plads",
            "Kødbyen", "Sydhavns Plads", "Sluseholmen",
            "Amager Strand", "Amager Landevej", "Ørestad",
            "Lufthavnen", "Ørestad Syd", "Ørestad Nord",
            "Refshaleøen", "Nordhavn", "Langelinie", "Kastellet",
            "Østerport", "Nørreport", "Vesterport", "Christianshavn", "Søerne",
            "Rådhuspladsen", "Kgs. Nytorv", "Nørrebrogade", "Frederiksberg Allé",
            ]


# --- Backend game setup ---
priser = [0, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550,
          600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050,
          1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450, 1500,
          1550, 1600, 1650, 1700, 1750, 1800, 1850, 1900, 1950,
          2000]

felter = [Grund(name, color, price) for name, price, color in zip(NAMES, priser, COLORS)]
spillere = [Spiller("Spiller 1"), Spiller("Spiller 2"), Spiller("Spiller 3"), Spiller("Spiller 4")]
nuværende_spiller_index = 0


def add_message(msg):
    messages.append(msg)
    if len(messages) > MAX_MESSAGES:
        messages.pop(0)


def get_nuværende_spiller():
    return spillere[nuværende_spiller_index]


def næste_spiller():
    global nuværende_spiller_index
    nuværende_spiller_index = (nuværende_spiller_index + 1) % len(spillere)
    attempts = 0
    while get_nuværende_spiller().konkurs and attempts < len(spillere):
        nuværende_spiller_index = (nuværende_spiller_index + 1) % len(spillere)
        attempts += 1


def check_game_over():
    global game_state
    alive = [s for s in spillere if not s.konkurs]
    if len(alive) <= 1:
        if alive:
            add_message(f"{alive[0].navn} har vundet spillet!")
        game_state = "GAME_OVER"
        return True
    return False


def do_roll():
    """Execute dice roll and movement for current player."""
    global game_state, buy_grund
    spiller = get_nuværende_spiller()
    if spiller.konkurs:
        add_message(f"{spiller.navn} er konkurs og springer over.")
        næste_spiller()
        return

    add_message(f"--- {spiller.navn}s tur ---")
    terning1 = random.randint(1, 6)
    terning2 = random.randint(1, 6)
    total = terning1 + terning2
    add_message(f"Slog {terning1} + {terning2} = {total}")

    if (spiller.pos + total) >= n_brikker:
        spiller.penge += 4000
        add_message(f"Passerer START - modtager 4000 kr!")

    spiller.pos = (spiller.pos + total) % n_brikker
    felt = felter[spiller.pos]
    add_message(f"Lander på {felt.navn}")

    # Pay rent if owned by someone else
    if isinstance(felt, Grund) and felt.ejer is not None and felt.ejer != spiller:
        leje = int(felt.alle_lejebeløb[felt.huse])
        if spiller.penge >= leje:
            spiller.penge -= leje
            felt.ejer.penge += leje
            add_message(f"Betaler {leje} kr. i leje til {felt.ejer.navn}")
        else:
            add_message(f"Kan ikke betale {leje} kr. - KONKURS!")
            spiller.konkurs = True
            if check_game_over():
                return
            næste_spiller()
            game_state = "WAIT_ROLL"
            return

    # Offer to buy if unowned
    if isinstance(felt, Grund) and felt.ejer is None and felt.pris > 0:
        if spiller.penge >= felt.pris:
            buy_grund = felt
            game_state = "WAIT_BUY"
            add_message(f"Køb {felt.navn} for {felt.pris} kr? (J = Ja, N = Nej)")
            return

    næste_spiller()
    game_state = "WAIT_ROLL"


def do_buy(accept):
    """Handle buy decision."""
    global game_state, buy_grund
    spiller = get_nuværende_spiller()
    if accept and buy_grund:
        if spiller.penge >= buy_grund.pris:
            spiller.penge -= buy_grund.pris
            buy_grund.ejer = spiller
            spiller.ejendomme.append(buy_grund)
            add_message(f"{spiller.navn} køber {buy_grund.navn} for {buy_grund.pris} kr!")
        else:
            add_message(f"Ikke nok penge!")
    else:
        if buy_grund:
            add_message(f"{spiller.navn} køber ikke {buy_grund.navn}.")
    buy_grund = None
    næste_spiller()
    game_state = "WAIT_ROLL"


def draw_board():
    board_radius = (np.minimum(screen.get_width(), screen.get_height()) / 2) * zoom
    inner_radius = board_radius - 200 * zoom
    screen.fill("black")
    pygame.draw.circle(screen, "orange", zoomed(center), board_radius)
    for i in range(n_brikker):
        angle = i * 360 / n_brikker + rotation_angle + 90
        end_pos = center + pygame.Vector2(np.cos(np.radians(angle)), np.sin(np.radians(angle))) * board_radius / zoom
        pygame.draw.line(screen, "black", zoomed(center), zoomed(end_pos), int(5 * zoom))
        # Place text between this line and the next, rotated 90 degrees extra
        mid_angle = angle + (360 / n_brikker) / 2
        font = pygame.font.SysFont(None, int(30 * zoom))
        num = font.render(str(i + 1), True, "black")
        num = pygame.transform.rotate(num, -mid_angle + 90)
        num_pos = center + pygame.Vector2(np.cos(np.radians(mid_angle)), np.sin(np.radians(mid_angle))) * (board_radius - 180 * zoom) / zoom
        num_rect = num.get_rect(center=zoomed(num_pos))
        screen.blit(num, num_rect)

        # Draw colored button (rectangle) centered between the two lines and between inner/outer circle
        btn_distance = (board_radius + inner_radius) / 2 / zoom
        btn_center_world = center + pygame.Vector2(np.cos(np.radians(mid_angle)), np.sin(np.radians(mid_angle))) * btn_distance*1.1
        btn_center_screen = zoomed(btn_center_world)

        btn_w = int(80 * zoom)
        btn_h = int(80 * zoom)
        btn_surface = pygame.Surface((btn_w, btn_h), pygame.SRCALPHA)
        color = COLORS[i % len(COLORS)]
        btn_surface.fill(color)

        # Render name text on the button
        name = NAMES[i % len(NAMES)]
        btn_font = pygame.font.SysFont(None, int(max(12, 14 * zoom)))
        name_surface = btn_font.render(name, True, WHITE if color != WHITE and color != LIGHT_YELLOW and color != YELLOW else BLACK)
        name_rect = name_surface.get_rect(center=(btn_w // 2, btn_h // 2))
        btn_surface.blit(name_surface, name_rect)

        # Rotate button to match the board segment angle
        rotated_btn = pygame.transform.rotate(btn_surface, -mid_angle + 90)
        rotated_rect = rotated_btn.get_rect(center=(int(btn_center_screen.x), int(btn_center_screen.y)))
        screen.blit(rotated_btn, rotated_rect)

    pygame.draw.circle(screen, "beige", zoomed(center), inner_radius)
    pygame.draw.circle(screen, "black", zoomed(center), inner_radius, int(5 * zoom))
    font = pygame.font.SysFont(None, int(200 * zoom))
    text = font.render("MATADOR", True, "black")
    text_rect = text.get_rect(center=zoomed(center))
    text = pygame.transform.rotate(text, -rotation_angle)
    text_rect = text.get_rect(center=zoomed(center))
    screen.blit(text, text_rect)


def get_tile_world_pos(tile_index):
    """Get the world position for a player piece on a given tile."""
    base_radius = np.minimum(screen.get_width(), screen.get_height()) / 2
    inner_r = base_radius - 200
    btn_distance = (base_radius + inner_r) / 2 
    angle = tile_index * 360 / n_brikker + rotation_angle + 90 + (360 / n_brikker) / 2
    return center + pygame.Vector2(np.cos(np.radians(angle)), np.sin(np.radians(angle))) * btn_distance


def draw_players():
    radius = int(player_radius * zoom)
    for idx, spiller in enumerate(spillere):
        if spiller.konkurs:
            continue
        pos = get_tile_world_pos(spiller.pos)
        screen_pos = zoomed(pos)
        ox, oy = PLAYER_OFFSETS[idx]
        draw_x = int(screen_pos.x + ox * zoom)
        draw_y = int(screen_pos.y + oy * zoom)
        pygame.draw.circle(screen, PLAYER_COLORS[idx], (draw_x, draw_y), radius)
        pygame.draw.circle(screen, BLACK, (draw_x, draw_y), radius, max(1, int(2 * zoom)))


def draw_popup():
    global popup_close_rect
    if not popup_open or popup_tile < 0:
        return
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))

    popup_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
    pygame.draw.rect(screen, WHITE, popup_rect, border_radius=12)
    pygame.draw.rect(screen, BLACK, popup_rect, 3, border_radius=12)

    color = COLORS[popup_tile % len(COLORS)]
    color_bar = pygame.Rect(popup_rect.x + 3, popup_rect.y + 3, popup_rect.width - 6, 50)
    pygame.draw.rect(screen, color, color_bar, border_radius=10)

    title_font = pygame.font.SysFont(None, 40)
    tile_num = title_font.render(f"Felt {popup_tile + 1}", True, BLACK)
    screen.blit(tile_num, (popup_rect.x + 20, popup_rect.y + 65))

    name = NAMES[popup_tile % len(NAMES)]
    name_font = pygame.font.SysFont(None, 36)
    name_surface = name_font.render(name, True, BLACK)
    screen.blit(name_surface, (popup_rect.x + 20, popup_rect.y + 110))

    # Show game info for this tile
    if popup_tile < len(felter):
        felt = felter[popup_tile]
        if isinstance(felt, Grund):
            info_font = pygame.font.SysFont(None, 28)
            y = popup_rect.y + 155
            pris_text = info_font.render(f"Pris: {felt.pris} kr.", True, BLACK)
            screen.blit(pris_text, (popup_rect.x + 20, y))
            y += 30
            ejer_name = felt.ejer.navn if felt.ejer else "Ingen"
            ejer_text = info_font.render(f"Ejer: {ejer_name}", True, BLACK)
            screen.blit(ejer_text, (popup_rect.x + 20, y))
            y += 30
            if felt.huse > 0:
                huse_text = info_font.render(f"Huse: {felt.huse}", True, BLACK)
                screen.blit(huse_text, (popup_rect.x + 20, y))
                y += 30
            leje = int(felt.alle_lejebeløb[felt.huse])
            leje_text = info_font.render(f"Leje: {leje} kr.", True, BLACK)
            screen.blit(leje_text, (popup_rect.x + 20, y))

    popup_close_rect = pygame.Rect(popup_rect.right - 40, popup_rect.y + 8, 30, 30)
    pygame.draw.rect(screen, RED, popup_close_rect, border_radius=5)
    close_font = pygame.font.SysFont(None, 30)
    x_text = close_font.render("X", True, WHITE)
    x_rect = x_text.get_rect(center=popup_close_rect.center)
    screen.blit(x_text, x_rect)


def draw_hud():
    """Draw player info panel at the top of the screen."""
    panel_h = 70
    panel = pygame.Surface((screen.get_width(), panel_h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 180))
    screen.blit(panel, (0, 0))

    x = 20
    font = pygame.font.SysFont(None, 26)
    for idx, spiller in enumerate(spillere):
        color = PLAYER_COLORS[idx]
        if spiller.konkurs:
            color = GRAY
        is_current = (idx == nuværende_spiller_index)
        pygame.draw.circle(screen, color, (x + 8, 20), 8)
        if is_current:
            pygame.draw.circle(screen, WHITE, (x + 8, 20), 11, 2)
        info = f"{spiller.navn}: {spiller.penge} kr."
        if spiller.konkurs:
            info = f"{spiller.navn}: KONKURS"
        text = font.render(info, True, color)
        screen.blit(text, (x + 22, 12))
        ejendom_text = font.render(f"Ejendomme: {len(spiller.ejendomme)}", True, color)
        screen.blit(ejendom_text, (x + 22, 38))
        x += 310

    # Turn hint
    hint_font = pygame.font.SysFont(None, 24)
    sp = get_nuværende_spiller()
    if game_state == "WAIT_ROLL":
        hint = f"{sp.navn}s tur - tryk MELLEMRUM for at slå"
    elif game_state == "WAIT_BUY":
        hint = f"{sp.navn}: Tryk J for Ja, N for Nej"
    elif game_state == "GAME_OVER":
        hint = "Spillet er slut!"
    else:
        hint = ""
    hint_surface = hint_font.render(hint, True, YELLOW)
    screen.blit(hint_surface, (20, 56))


def draw_messages():
    """Draw message log at the bottom of the screen."""
    if not messages:
        return
    n = min(len(messages), MAX_MESSAGES)
    panel_h = 28 * n + 20
    panel_y = screen.get_height() - panel_h
    panel = pygame.Surface((screen.get_width(), panel_h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 180))
    screen.blit(panel, (0, panel_y))

    font = pygame.font.SysFont(None, 24)
    for i, msg in enumerate(messages[-n:]):
        text = font.render(msg, True, WHITE)
        screen.blit(text, (20, panel_y + 10 + i * 28))


# --- Welcome messages ---
add_message("Velkommen til Matador!")
add_message(f"{get_nuværende_spiller().navn} starter. Tryk MELLEMRUM for at slå.")

# --- Main loop ---
while running:
    handle_events()
    handle_drag()
    draw_board()
    draw_players()
    draw_popup()
    draw_hud()
    draw_messages()
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()