import pygame
from src.Game import Game

pygame.init()

CARD_WIDTH, CARD_HEIGHT = 100, 150
MIN_WIDTH, MIN_HEIGHT = 600, 600
POP_OUT_OFFSET = CARD_HEIGHT * 5 / 8

background_image = pygame.image.load('../assets/table.jpg')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (200, 200, 0)
COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "All": (255, 255, 255),
}
CP_WIDTH = 300
CP_HEIGHT = 300
FONT = pygame.font.SysFont("Arial", 20)
AVATAR_SIZE = 100
AVATAR_MARGIN = 50

def display_start_menu(screen, width, height):
    screen.fill(WHITE)
    title_text = FONT.render("UNO Game", True, BLACK)
    title_rect = title_text.get_rect(center=(width // 2, height // 4))
    screen.blit(title_text, title_rect)
    start_button_text = FONT.render("Start Game!", True, WHITE)
    start_button_rect = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 100)
    pygame.draw.rect(screen, BLACK, start_button_rect)
    screen.blit(start_button_text, start_button_text.get_rect(center=start_button_rect.center))
    pygame.display.flip()
    return start_button_rect

def start_menu():
    width, height = 1000, 800
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("UNO Card Interface")
    running = True
    while running:
        start_button_rect = display_start_menu(screen, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.VIDEORESIZE:
                width = max(event.w, MIN_WIDTH)
                height = max(event.h, MIN_HEIGHT)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    running = False
    return width, height

def draw_card(screen, card, x, y, disable_highlight, is_mouse_over=False, draw_pile=False):
    if draw_pile:
        color = (0, 0, 0)
        border_color = (255, 0, 0)
        text = FONT.render("UNO", True, WHITE)
    else:
        color = COLORS[card.color]
        border_color = BLACK
        text = FONT.render(card.value, True, BLACK)
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    border_radius = 10
    pygame.draw.rect(screen, border_color, rect, border_radius=border_radius)
    inner_rect = rect.inflate(-4, -4)
    pygame.draw.rect(screen, color, inner_rect, border_radius=border_radius)
    if is_mouse_over and not disable_highlight:
        pygame.draw.rect(screen, HIGHLIGHT, rect, 5, border_radius=border_radius)
    text_rect = text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
    screen.blit(text, text_rect)

def display_player_hand(screen, width, y, player, is_visible=True, disable_highlight=False):
    num_cards = len(player.cards_in_hand)
    if num_cards == 0:
        return None
    max_width = width - AVATAR_SIZE - AVATAR_MARGIN - 20
    card_spacing = CARD_WIDTH
    if (num_cards - 1) * CARD_WIDTH + CARD_WIDTH > max_width:
        card_spacing = (max_width - CARD_WIDTH) / (num_cards - 1)
    total_width = (num_cards - 1) * card_spacing + CARD_WIDTH
    starting_x = (width - total_width - (AVATAR_SIZE + AVATAR_MARGIN)) // 2
    mouse_pos = pygame.mouse.get_pos()
    highlighted_card = None
    for i in range(num_cards):
        card_rect = pygame.Rect(starting_x + i * card_spacing, y, CARD_WIDTH, CARD_HEIGHT)
        if card_rect.collidepoint(mouse_pos):
            highlighted_card = i
            break
    for i in range(num_cards):
        x = starting_x + i * card_spacing
        is_highlighted = i == highlighted_card and is_visible
        draw_y = y - POP_OUT_OFFSET if is_highlighted else y
        if is_visible:
            draw_card(screen, player.cards_in_hand[i], x, draw_y, disable_highlight, is_highlighted)
        else:
            draw_card(screen, None, x, y, disable_highlight, draw_pile=True)
    return highlighted_card

def display_and_check_deck(screen, width, height, deck, disable_highlight=False):
    x = (width - CARD_WIDTH) // 2
    y = (height - CARD_HEIGHT - 20) // 2
    mouse_pos = pygame.mouse.get_pos()
    card_rect = pygame.Rect(x - CARD_WIDTH, y, CARD_WIDTH, CARD_HEIGHT)
    is_mouse_over = card_rect.collidepoint(mouse_pos)
    draw_card(screen, None, x - CARD_WIDTH, y, disable_highlight, is_mouse_over, True)
    first_card = deck.get_top_discarded_card()
    draw_card(screen, first_card, x, y, disable_highlight)
    return is_mouse_over

def draw_player_avatar(width, height, player_num, y_position):
    background = pygame.Surface((width, height), pygame.SRCALPHA)
    if player_num == 1:
        avatar_image = pygame.image.load('../assets/avatar1.jpg')
    else:
        avatar_image = pygame.image.load('../assets/avatar2.jpg')
    avatar_image = pygame.transform.scale(avatar_image, (AVATAR_SIZE, AVATAR_SIZE))
    avatar_rect = pygame.Rect(width - AVATAR_MARGIN - AVATAR_SIZE, y_position, AVATAR_SIZE, AVATAR_SIZE)
    background.blit(avatar_image, avatar_rect)
    player_text = FONT.render(f"Player {player_num + 1}", True, WHITE)
    text_rect = player_text.get_rect(center=(width - AVATAR_SIZE, y_position + AVATAR_SIZE + 10))
    background.blit(player_text, text_rect)
    return background

def display_final_screen(screen, width, height, main_text, additional_text=None, rgb_color=(0, 0, 0)):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                width = max(event.w, MIN_WIDTH)
                height = max(event.h, MIN_HEIGHT)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        screen.fill(rgb_color)
        text = FONT.render(main_text, True, WHITE)
        text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(text, text_rect)
        if additional_text:
            sub_text = FONT.render(additional_text, True, WHITE)
            sub_text_rect = sub_text.get_rect(center=(width // 2, height // 2 + 20))
            screen.blit(sub_text, sub_text_rect)
        pygame.display.flip()

def wait_for_exit():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

def draw_color(screen, color, x, y):
    mouse_pos = pygame.mouse.get_pos()
    color_rect = pygame.Rect(x, y, CP_WIDTH // 2, CP_HEIGHT // 2)
    is_mouse_over = color_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, color, color_rect, border_radius=10)
    if is_mouse_over:
        pygame.draw.rect(screen, HIGHLIGHT, color_rect, 5, border_radius=10)
    return is_mouse_over

def draw_player_turn(screen, width, height, count_turn):
    if count_turn == 0:
        avatar_rect = pygame.Rect(width - 150, height - 120, 100, 100)
    else:
        avatar_rect = pygame.Rect(width - 150, 20, 100, 100)
    pygame.draw.rect(screen, HIGHLIGHT, avatar_rect, 5)

def read_background(width, height):
    background_surface = pygame.Surface((width, height))
    background_surface.blit(pygame.transform.scale(background_image, (width, height)), (0, 0))
    avatar1 = draw_player_avatar(width, height, 1, 20)
    avatar2 = draw_player_avatar(width, height, 0, height - 120)
    return background_surface, avatar1, avatar2

def display_uno_button(screen, width, height):
    button_width, button_height = 200, 70
    button_rect = pygame.Rect(width - button_width - 20, height - button_height - AVATAR_SIZE - 50, button_width,
                              button_height)
    pygame.draw.rect(screen, (0, 0, 0), button_rect, border_radius=8)
    uno_text = FONT.render("UNO!", True, (255, 255, 255))
    uno_text_rect = uno_text.get_rect(center=button_rect.center)
    screen.blit(uno_text, uno_text_rect)
    mouse_pressed = pygame.mouse.get_pressed(num_buttons=3)
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pressed[0] and button_rect.collidepoint(mouse_pos):
        return True
    return False

def display_timer(screen, elapsed_time, width):
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    time_text = FONT.render(f"Time: {minutes:02}:{seconds:02}", True, WHITE)
    time_rect = time_text.get_rect(topleft=(20, 10))
    screen.blit(time_text, time_rect)

def run():
    width, height = start_menu()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("UNO Card Interface")
    game = Game()
    game.start_game()
    selected_card = None
    is_running = True
    pause_after_card = False
    background_surface, avatar1, avatar2 = read_background(width, height)
    start_time = pygame.time.get_ticks()
    while game.check_winner() is None and is_running:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.VIDEORESIZE:
                width = max(event.w, MIN_WIDTH)
                height = max(event.h, MIN_HEIGHT)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                background_surface, avatar1, avatar2 = read_background(width, height)
        screen.blit(background_surface, (0, 0))
        screen.blit(avatar1, (0, 0))
        screen.blit(avatar2, (0, 0))
        draw_player_turn(screen, width, height, game.count_turn)
        display_player_hand(screen, width, 20, game.players[1], is_visible=False)
        highlighted_card = display_player_hand(screen, width, height - CARD_HEIGHT - 20, game.players[0])
        is_draw_pile_clicked = display_and_check_deck(screen, width, height, game.deck)
        display_timer(screen, elapsed_time, width)
        if pause_after_card:
            is_draw_pile_clicked = display_and_check_deck(screen, width, height, game.deck, True)
            highlighted_card = display_player_hand(screen, width, height - CARD_HEIGHT - 20, game.players[0], True)
            pygame.display.flip()
            pygame.time.wait(500)
            pygame.event.clear()
            pause_after_card = False
            game.track_turn()
        if game.count_turn == 0 and not pause_after_card:
            uno_pressed_this_turn = False
            turn_still_going = True
            while turn_still_going:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_running = False
                        turn_still_going = False
                    elif event.type == pygame.VIDEORESIZE:
                        width = max(event.w, MIN_WIDTH)
                        height = max(event.h, MIN_HEIGHT)
                        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                        background_surface, avatar1, avatar2 = read_background(width, height)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if highlighted_card is not None:
                            selected_card = highlighted_card
                        if event.button == 1:
                            if selected_card is not None and game.play_card(0, selected_card):
                                selected_card = None
                                pause_after_card = True
                                turn_still_going = False
                            if is_draw_pile_clicked:
                                game.draw_card(0)
                                pause_after_card = True
                                turn_still_going = False
                            if game.is_color_changed:
                                color = None
                                while color is None:
                                    screen.blit(background_surface, (0, 0))
                                    screen.blit(avatar1, (0, 0))
                                    screen.blit(avatar2, (0, 0))
                                    draw_player_turn(screen, width, height, game.count_turn)
                                    display_player_hand(screen, width, 20, game.players[1], is_visible=False)
                                    display_player_hand(screen, width, height - CARD_HEIGHT - 20, game.players[0])
                                    display_and_check_deck(screen, width, height, game.deck)
                                    display_timer(screen, elapsed_time, width)
                                    mid_x = width // 2
                                    mid_y = height // 2
                                    picker_rect = pygame.Rect(
                                        mid_x - CP_WIDTH // 2 - 15,
                                        mid_y - CP_HEIGHT // 2 - 15,
                                        CP_WIDTH + 30,
                                        CP_HEIGHT + 30
                                    )
                                    pygame.draw.rect(screen, BLACK, picker_rect, border_radius=15)
                                    red_hover = draw_color(screen, COLORS["Red"], mid_x - CP_WIDTH // 2 - 5, mid_y - CP_HEIGHT // 2 - 5)
                                    blue_hover = draw_color(screen, COLORS["Blue"], mid_x + 5, mid_y - CP_HEIGHT // 2 - 5)
                                    yellow_hover = draw_color(screen, COLORS["Yellow"], mid_x - CP_WIDTH // 2 - 5, mid_y + 5)
                                    green_hover = draw_color(screen, COLORS["Green"], mid_x + 5, mid_y + 5)
                                    pygame.display.flip()
                                    for ev in pygame.event.get():
                                        if ev.type == pygame.QUIT:
                                            is_running = False
                                            color = "Red"
                                        elif ev.type == pygame.VIDEORESIZE:
                                            width = max(ev.w, MIN_WIDTH)
                                            height = max(ev.h, MIN_HEIGHT)
                                            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                                            background_surface, avatar1, avatar2 = read_background(width, height)
                                        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                                            if red_hover:
                                                color = "Red"
                                            elif blue_hover:
                                                color = "Blue"
                                            elif yellow_hover:
                                                color = "Yellow"
                                            elif green_hover:
                                                color = "Green"
                                game.change_color(color)
                                pause_after_card = True
                screen.blit(background_surface, (0, 0))
                screen.blit(avatar1, (0, 0))
                screen.blit(avatar2, (0, 0))
                draw_player_turn(screen, width, height, game.count_turn)
                display_player_hand(screen, width, 20, game.players[1], is_visible=False)
                highlighted_card = display_player_hand(screen, width, height - CARD_HEIGHT - 20, game.players[0])
                is_draw_pile_clicked = display_and_check_deck(screen, width, height, game.deck)
                display_timer(screen, elapsed_time, width)
                if game.players[0].if_last_move() and not uno_pressed_this_turn and pause_after_card == False:
                    pressed = display_uno_button(screen, width, height)
                    if pressed:
                        uno_pressed_this_turn = True
                pygame.display.flip()
                if not is_running or pause_after_card:
                    turn_still_going = False
            if game.players[0].if_uno() and not uno_pressed_this_turn:
                for _ in range(3):
                    game.draw_card(0)
        else:
            game.random_move()
            pause_after_card = True
        pygame.display.flip()
    if game.check_winner() == game.players[0]:
        display_final_screen(screen, width, height, "You Win!", "Congratulations! Press any key to exit.", (0, 128, 0))
        pygame.quit()
    else:
        display_final_screen(screen, width, height, "You Lose!", "Better luck next time! Press any key to exit.", (128, 0, 0))
        pygame.quit()

if __name__ == "__main__":
    run()
