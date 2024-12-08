import pygame
from Deck import Card, Deck
from Player import Player
from Game import Game

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UNO Card Interface")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (200, 200, 0)
COLORS = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "All": (128, 128, 128),
}

FONT = pygame.font.SysFont("Arial", 20)

CARD_WIDTH, CARD_HEIGHT = 80, 120
CARD_SPACING = 10

def draw_card(card, x, y, highlight=False):
    color = COLORS[card.color]
    pygame.draw.rect(screen, color, (x, y, CARD_WIDTH, CARD_HEIGHT))
    if highlight:
        pygame.draw.rect(screen, HIGHLIGHT, (x, y, CARD_WIDTH, CARD_HEIGHT), 5)
    text = FONT.render(card.value, True, BLACK)
    text_rect = text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
    screen.blit(text, text_rect)

def display_player_hand(y, player):
    x = CARD_SPACING
    # y = HEIGHT - CARD_HEIGHT - 20
    mouse_pos = pygame.mouse.get_pos()
    highlighted_card = None

    for i, card in enumerate(player.cards_in_hand):
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        highlight = card_rect.collidepoint(mouse_pos)
        draw_card(card, x, y, highlight)

        if highlight:
            highlighted_card = i

        x += CARD_WIDTH + CARD_SPACING
    return highlighted_card

def draw_deck_cards(x, y, highlight=False):
    color = (0,0,0)
    pygame.draw.rect(screen, color, (x, y, CARD_WIDTH, CARD_HEIGHT))
    if highlight:
        pygame.draw.rect(screen, HIGHLIGHT, (x, y, CARD_WIDTH, CARD_HEIGHT), 5)
    text = FONT.render("UNO", True, WHITE)
    text_rect = text.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
    screen.blit(text, text_rect)

def display_deck(deck):
    x = (WIDTH - CARD_WIDTH)// 2
    y = (HEIGHT - CARD_HEIGHT - 20) // 2
    mouse_pos = pygame.mouse.get_pos()

    card_rect = pygame.Rect(x - CARD_WIDTH - 4 * CARD_SPACING, y, CARD_WIDTH, CARD_HEIGHT)
    highlight = card_rect.collidepoint(mouse_pos)
    draw_deck_cards(x - CARD_WIDTH - 4 * CARD_SPACING, y, highlight)

    first_card = deck.get_top_discarded_card()
    draw_card(first_card, x, y)

    return highlight

def run():
    game = Game()
    game.start_game()

    selected_card = None
    running = True
    turn = "player_turn"

    while game.check_winner() == None and running:
        screen.fill(WHITE)
        display_player_hand(20, game.players[1])
        highlighted_card = display_player_hand(HEIGHT - CARD_HEIGHT - 20, game.players[0])

        if turn == "player_turn":   
            uno_card = display_deck(game.deck)       
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if highlighted_card is not None:
                        selected_card = highlighted_card
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and selected_card is not None:
                        if game.play_card(0, selected_card):
                            selected_card = None
                            turn = "opponent_turn"
                    if event.key == pygame.K_SPACE and uno_card is True:
                        game.draw_card(0)
                        turn = "opponent_turn"

            if selected_card is not None:
                x = selected_card * (CARD_WIDTH + CARD_SPACING) + CARD_SPACING
                y = HEIGHT - CARD_HEIGHT - 20
                pygame.draw.rect(screen, HIGHLIGHT, (x, y, CARD_WIDTH, CARD_HEIGHT), 5)
            
        elif turn == "opponent_turn":
            game.random_move()
            turn = "player_turn"

        pygame.display.flip()

    pygame.quit()
