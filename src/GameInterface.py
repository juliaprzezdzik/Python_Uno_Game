import pygame
from Deck import Card, Deck
from Player import Player
from Game import Game

pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UNO Card Interface")

background_image = pygame.image.load('../assets/table.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (200,200,0)
COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "All": (128, 128, 128),
}

FONT = pygame.font.SysFont("Arial", 20)

CARD_WIDTH, CARD_HEIGHT = 80, 120
CARD_SPACING = 5

def draw_card(card, x, y, disable_highlight, is_mouse_over=False, draw_pile=False):
    if draw_pile:
        color = (0, 0, 0)
        text = FONT.render("UNO", True, WHITE)
    else:
        color = COLORS[card.color]
        text = FONT.render(card.value, True, BLACK)

    pygame.draw.rect(screen, color, (x, y, CARD_WIDTH, CARD_HEIGHT))
    if is_mouse_over and not disable_highlight:
        pygame.draw.rect(screen, HIGHLIGHT, (x, y, CARD_WIDTH, CARD_HEIGHT), 5)
    text_rect = text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
    screen.blit(text, text_rect)


def display_player_hand(y, player, disable_highlight=False, hide_cards=False):
    x = CARD_SPACING
    mouse_pos = pygame.mouse.get_pos()
    highlighted_card = None

    for i, card in enumerate(player.cards_in_hand):
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

        if hide_cards:
            pygame.draw.rect(screen, BLACK, card_rect)
            text = FONT.render("UNO", True, WHITE)
            text_rect = text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
            screen.blit(text, text_rect)
        else:
            highlight = card_rect.collidepoint(mouse_pos)
            draw_card(card, x, y, disable_highlight, highlight)

            if highlight:
                highlighted_card = i

        x += CARD_WIDTH + CARD_SPACING
    return highlighted_card



def display_and_check_deck(deck, disable_highlight=False):
    x = (WIDTH - CARD_WIDTH) // 2
    y = (HEIGHT - CARD_HEIGHT - 20) // 2
    mouse_pos = pygame.mouse.get_pos()
    card_rect = pygame.Rect(x - CARD_WIDTH - 4 * CARD_SPACING, y, CARD_WIDTH, CARD_HEIGHT)
    is_mouse_over = card_rect.collidepoint(mouse_pos)

    draw_card(None, x - CARD_WIDTH - 4 * CARD_SPACING, y, disable_highlight, is_mouse_over, True)
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


def run():
    game = Game()
    game.start_game(initial_hand_size=7)
    selected_card = None
    is_running = True
    pause_after_card = False

    while game.check_winner() is None and is_running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        if game.count_turn == 0 and not pause_after_card:
            turn_text = FONT.render("Your Turn!", True, WHITE)
            text_rect = turn_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
            screen.blit(turn_text, text_rect)

        draw_player_avatar(0, game.count_turn == 0, 20)
        display_player_hand(20, game.players[1], hide_cards=True)

        draw_player_avatar(1, game.count_turn == 1, HEIGHT - 120)
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
                if event.type == pygame.MOUSEBUTTONDOWN:
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

    pygame.quit()

if __name__ == "__main__":
    run()
