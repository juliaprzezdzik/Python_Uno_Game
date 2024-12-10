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
FONT = pygame.font.SysFont("Arial", 20)

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
    total_width = num_cards * CARD_WIDTH + (num_cards - 1)
    starting_x = (WIDTH - total_width) // 2
    mouse_pos = pygame.mouse.get_pos()
    highlighted_card = None
    for i in range(num_cards):
        card_rect = pygame.Rect(starting_x + i * CARD_WIDTH , y, CARD_WIDTH, CARD_HEIGHT)
        if card_rect.collidepoint(mouse_pos):
            highlighted_card = i
            break
    for i in range(num_cards):
        x = starting_x + i * CARD_WIDTH
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

def draw_player_avatar(player_num, is_turn, y_position):
    if player_num == 1:
        avatar_image = pygame.image.load('../assets/avatar1.jpg')
    else:
        avatar_image = pygame.image.load('../assets/avatar2.jpg')
    avatar_image = pygame.transform.scale(avatar_image, (100, 100))
    avatar_rect = pygame.Rect(WIDTH - 150, y_position, 100, 100)
    screen.blit(avatar_image, avatar_rect)
    if is_turn:
        pygame.draw.rect(screen, HIGHLIGHT, avatar_rect, 5)
    player_text = FONT.render(f"Player {player_num + 1}", True, WHITE)
    text_rect = player_text.get_rect(center=(WIDTH - 100, y_position + 110))
    screen.blit(player_text, text_rect)

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


def run():
    game = Game()
    game.start_game(initial_hand_size=7)
    selected_card = None
    is_running = True
    pause_after_card = False
    while game.check_winner() is None and is_running:
        global WIDTH, HEIGHT
        WIDTH, HEIGHT = screen.get_size()
        screen.fill(WHITE)
        background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))
        draw_player_avatar(1, game.count_turn == 1, 20)
        display_player_hand(20, game.players[1], is_visible=False)
        draw_player_avatar(0, game.count_turn == 0, HEIGHT - 120)
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
        else:
            game.random_move()
            pause_after_card = True
        pygame.display.flip()
    if game.check_winner == game.players[0]:
        display_victory_screen()
        pygame.quit()
    else:
        display_loss_screen()
        pygame.quit()

if __name__ == "__main__":
    run()
