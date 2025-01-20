from src.DQN.GameState import GameState
import time

class Action:
    def __init__(self, state):
        self.game_state = state
        self.n_actions = self.game_state.player_cards_count

    def permorm_action(self, game, action, state, index, len_available_actions):
        reward = 0
        prev_state = state
        has_valid_move = any(
            game.is_valid_move(game.players[1].cards_in_hand[i], game.deck.get_top_discarded_card())
            for i in range(game.players[1].count_cards_in_hand())
        )

        if game.count_turn == 1:
            if action >= game.players[1].count_cards_in_hand():
                game.draw_card(1)
                if has_valid_move:
                    reward -= 20
            elif game.play_card(1, action):
                total_cards_in_hand = game.players[1].count_cards_in_hand()
                opponent_cards = game.players[0].count_cards_in_hand()
                card_played = game.deck.get_top_discarded_card()
                skip_count = game.players[1].count_skip_cards()
                wild_count = game.players[1].count_wild_cards()
                value_counts = game.players[1].count_cards_with_same_value()
                most_common_color = game.players[1].get_most_common_color()

                if total_cards_in_hand == skip_count:
                    reward += 15
                if total_cards_in_hand == wild_count:
                    reward += 15
                if card_played.value == "Skip":
                    reward += 5 if len_available_actions < 1 + skip_count else -5
                if game.is_color_changed:
                    game.change_color(most_common_color)
                if opponent_cards == 1:
                    reward += 15 if card_played.value in ["Draw Two", "Wild Draw Four"] else -1
                elif opponent_cards <= 2:
                    reward += 5 if card_played.value in ["Draw Two", "Wild Draw Four"] else -1
                if card_played.value == "Wild" and len_available_actions > 1 + wild_count:
                    reward -= 5
                elif card_played.value == "Wild":
                    reward += 1
                if card_played.color == most_common_color:
                    reward += 2
                if card_played.value == game.deck.discarded[-2].value:
                    reward += 1
                if total_cards_in_hand == 1:
                    reward += 10 if card_played.value in ["Wild", "Wild Draw Four"] else 5
                if card_played.value in value_counts:
                    identical_cards_count = game.players[1].count_identical_cards(card_played)
                    if len_available_actions > 2 + identical_cards_count:
                        reward -= 10
                if game.check_winner() == game.players[1]:
                    reward += 100
            game.track_turn()
                      
        if game.count_turn == 0:
            game.random_move(0)
            if game.check_winner() == game.players[0]:
                reward -= 100
            game.track_turn()

        total_cards_in_hand = game.players[1].count_cards_in_hand()
        opponent_cards = game.players[0].count_cards_in_hand()
        next_game_state = GameState(game)
        next_state = next_game_state
        action_effectiveness = self.calculate_action_effectiveness(prev_state, next_state)
        reward += action_effectiveness
        done = total_cards_in_hand == 0 or opponent_cards == 0
        return next_state, reward, done

    def calculate_action_effectiveness(self, prev_state, next_state):
        prev_score = self.calculate_state_score(prev_state)
        next_score = self.calculate_state_score(next_state)
        effectiveness = next_score - prev_score
        if effectiveness > 0:
            return 1
        elif effectiveness < 0:
            return -1
        else:
            return 0

    def calculate_state_score(self, state):
        player_cards_count = state.player_cards_count
        opponent_cards_count = state.opponent_cards_count
        score = (opponent_cards_count - player_cards_count)
        return score