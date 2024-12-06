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

def display_player_hand(player):
    x = CARD_SPACING
    y = HEIGHT - CARD_HEIGHT - 20
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

def main():
    game = Game()
    game.start_game()
    running = True
    selected_card = None

    while running:
        screen.fill(WHITE)
        highlighted_card = display_player_hand(game.players[0])
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

        if selected_card is not None:
            x = selected_card * (CARD_WIDTH + CARD_SPACING) + CARD_SPACING
            y = HEIGHT - CARD_HEIGHT - 20
            pygame.draw.rect(screen, HIGHLIGHT, (x, y, CARD_WIDTH, CARD_HEIGHT), 5)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()