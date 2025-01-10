from src.GameState import GameState

class Action:
    def __init__(self, state):
        self.game_state = state
        self.n_actions = self.game_state.player_cards_count

    def permorm_action(self, game, action, state):
        reward = 0
        prev_state = state
        has_valid_move = any(
            game.is_valid_move(game.players[1].cards_in_hand[i], game.deck.get_top_discarded_card())
            for i in range(game.players[1].count_cards_in_hand())
        )

        if action >= game.players[1].count_cards_in_hand():
            game.draw_card(1)
            if has_valid_move:
                reward = -2
            return state, reward, False
        if game.play_card(1, action):
            card_played = game.deck.get_top_discarded_card()
            if card_played.value == "Skip":
                reward += 5
            if game.is_color_changed:
                game.change_color(state.most_common_color)
                reward += 4
        else:
            reward -= 1
            card_played = None
        if game.check_winner() == game.players[1]:
            reward += 50
        elif game.check_winner() == game.players[0]:
            reward -= 10
        else:
            game.track_turn()
            game.random_move(0)
        total_cards_in_hand = game.players[1].count_cards_in_hand()
        opponent_cards = game.players[0].count_cards_in_hand()
        if card_played and opponent_cards == 1:
            reward += 3 if card_played.value in ["Draw Two", "Wild Draw Four"] else -1
        elif card_played and opponent_cards <= 2:
            reward += 2 if card_played.value in ["Draw Two", "Wild Draw Four"] else 0
        if total_cards_in_hand == 1:
            reward += 3
        reward += max(0, 5 - total_cards_in_hand)
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
        special_cards_count = state.special_cards_count
        score = (opponent_cards_count - player_cards_count) + (2 * special_cards_count)
        return score