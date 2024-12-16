import pygame
from Deck import Card, Deck
from Player import Player
from Game import Game

pygame.init()

WIDTH, HEIGHT = 1000, 800
CARD_WIDTH, CARD_HEIGHT = 100, 150
POP_OUT_OFFSET = CARD_HEIGHT*5/8

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("UNO Card Interface")

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

def display_start_menu():
    screen.fill(WHITE)
    title_text = FONT.render("UNO Game", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title_text, title_rect)
    start_button_text = FONT.render("Start Game!", True, WHITE)
    start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
    pygame.draw.rect(screen, BLACK, start_button_rect)
    screen.blit(start_button_text, start_button_text.get_rect(center=start_button_rect.center))
    pygame.display.flip()
    return start_button_rect

def start_menu():
    running = True
    while running:
        start_button_rect = display_start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    running = False

def draw_card(card, x, y, disable_highlight, is_mouse_over=False, draw_pile=False):
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

def display_player_hand(y, player, is_visible=True, disable_highlight=False):
    num_cards = len(player.cards_in_hand)
    if num_cards == 0:
        return None
    max_width = WIDTH - AVATAR_SIZE - AVATAR_MARGIN - 20
    card_spacing = CARD_WIDTH
    if (num_cards - 1) * CARD_WIDTH + CARD_WIDTH > max_width:
        card_spacing = (max_width - CARD_WIDTH) / (num_cards - 1)
    total_width = (num_cards - 1) * card_spacing + CARD_WIDTH
    starting_x = (WIDTH - total_width - (AVATAR_SIZE + AVATAR_MARGIN)) // 2
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
            draw_card(player.cards_in_hand[i], x, draw_y, disable_highlight, is_highlighted)
        else:
            draw_card(None, x, y, disable_highlight, draw_pile=True)
    return highlighted_card

def display_and_check_deck(deck, disable_highlight=False):
    x = (WIDTH - CARD_WIDTH) // 2
    y = (HEIGHT - CARD_HEIGHT - 20) // 2
    mouse_pos = pygame.mouse.get_pos()
    card_rect = pygame.Rect(x - CARD_WIDTH , y, CARD_WIDTH, CARD_HEIGHT)
    is_mouse_over = card_rect.collidepoint(mouse_pos)
    draw_card(None, x - CARD_WIDTH, y, disable_highlight, is_mouse_over, True)
    first_card = deck.get_top_discarded_card()
    draw_card(first_card, x, y, disable_highlight)
    return is_mouse_over

def draw_player_avatar(player_num, y_position):
    background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    if player_num == 1:
        avatar_image = pygame.image.load('../assets/avatar1.jpg')
    else:
        avatar_image = pygame.image.load('../assets/avatar2.jpg')
    avatar_image = pygame.transform.scale(avatar_image, (AVATAR_SIZE, AVATAR_SIZE))
    avatar_rect = pygame.Rect(WIDTH - AVATAR_MARGIN - AVATAR_SIZE, y_position, AVATAR_SIZE, AVATAR_SIZE)
    background.blit(avatar_image, avatar_rect)
    player_text = FONT.render(f"Player {player_num + 1}", True, WHITE)
    text_rect = player_text.get_rect(center=(WIDTH - AVATAR_SIZE, y_position + AVATAR_SIZE + 10))
    background.blit(player_text, text_rect)
    return background

def display_victory_screen():
    screen.fill((0, 128, 0))
    victory_text = FONT.render("You Win!", True, WHITE)
    sub_text = FONT.render("Congratulations! Press any key to exit.", True, WHITE)
    victory_text_rect = victory_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    sub_text_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(victory_text, victory_text_rect)
    screen.blit(sub_text, sub_text_rect)
    pygame.display.flip()
    wait_for_exit()

def display_loss_screen():
    screen.fill((128, 0, 0))
    loss_text = FONT.render("You Lose!", True, WHITE)
    sub_text = FONT.render("Better luck next time! Press any key to exit.", True, WHITE)
    loss_text_rect = loss_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    sub_text_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(loss_text, loss_text_rect)
    screen.blit(sub_text, sub_text_rect)
    pygame.display.flip()
    wait_for_exit()

def wait_for_exit():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

def draw_color(color, x, y, disable_highlight = False):
    mouse_pos = pygame.mouse.get_pos()
    color_rect = pygame.Rect(x, y, CP_WIDTH//2, CP_HEIGHT//2)
    is_mouse_over = color_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, color, color_rect, border_radius=10)
    if is_mouse_over:
        pygame.draw.rect(screen, HIGHLIGHT, color_rect, 5, border_radius=10)
    return is_mouse_over

def draw_player_turn(count_turn):
    if count_turn == 0:
        avatar_rect = pygame.Rect(WIDTH - 150, HEIGHT - 120, 100, 100)
    else:
        avatar_rect = pygame.Rect(WIDTH - 150, 20, 100, 100)
    pygame.draw.rect(screen, HIGHLIGHT, avatar_rect, 5)

def display_color_picker():
    mid_x = WIDTH // 2
    mid_y = HEIGHT // 2
    color = None
    picker_rect = pygame.Rect(mid_x - CP_WIDTH//2 - 15 , mid_y - CP_HEIGHT//2 - 15, CP_WIDTH + 30, CP_HEIGHT + 30)
    pygame.draw.rect(screen, BLACK, picker_rect, border_radius=15)  
    red = draw_color(COLORS["Red"], mid_x - CP_WIDTH//2 - 5, mid_y - CP_HEIGHT//2 - 5)
    blue = draw_color(COLORS["Blue"], mid_x + 5, mid_y - CP_HEIGHT//2 - 5)
    yellow = draw_color(COLORS["Yellow"], mid_x - CP_WIDTH//2 - 5, mid_y + 5)
    green = draw_color(COLORS["Green"], mid_x + 5, mid_y + 5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if red:
                color = "Red"
            if blue:
                color = "Blue"
            if yellow:
                color = "Yellow"
            if green:
                color = "Green"
    return color

def run():
    start_menu()
    game = Game()
    game.start_game()
    selected_card = None
    is_running = True
    pause_after_card = False
    color = None
    background_surface = pygame.Surface((WIDTH, HEIGHT))
    background_surface.blit(pygame.transform.scale(background_image, (WIDTH, HEIGHT)), (0, 0))
    avatar1 = draw_player_avatar(1, 20)
    avatar2 = draw_player_avatar(0, HEIGHT - 120)
    while game.check_winner() is None and is_running:
        screen.blit(background_surface, (0, 0))
        screen.blit(avatar1, (0, 0)) 
        screen.blit(avatar2, (0, 0))
        draw_player_turn(game.count_turn)       
        display_player_hand(20, game.players[1], is_visible=False)
        highlighted_card = display_player_hand(HEIGHT - CARD_HEIGHT - 20, game.players[0])
        is_draw_pile_clicked = display_and_check_deck(game.deck)
        if pause_after_card:
            is_draw_pile_clicked = display_and_check_deck(game.deck, True)
            highlighted_card = display_player_hand(HEIGHT - CARD_HEIGHT - 20, game.players[0], True)
            pygame.display.flip()
            pygame.time.wait(500)
            pygame.event.clear()
            pause_after_card = False
            game.track_turn()
        if game.count_turn == 0 and not pause_after_card:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if highlighted_card is not None:
                        selected_card = highlighted_card
                    if event.button == 1:
                        if selected_card is not None and game.play_card(0, selected_card):
                            selected_card = None
                            pause_after_card = True
                        if is_draw_pile_clicked:
                            game.draw_card(0)
                            pause_after_card = True
                        if game.is_color_changed:
                            pause_after_card = False
                            while color is None:
                                color = display_color_picker()
                                pygame.display.flip()
                            game.change_color(color)
                            pause_after_card = True
                            color = None
        else:
            game.random_move()
            pause_after_card = True
        pygame.display.flip()
    if game.check_winner() == game.players[0]:
        display_victory_screen()
        pygame.quit()
    else:
        display_loss_screen()
        pygame.quit()

if __name__ == "__main__":
    start_menu()
    run()
