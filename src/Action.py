from src.GameState import GameState

class Action:
    def __init__(self, state):
        self.game_state = state
        self.n_actions = self.game_state.player_cards_count

    def permorm_action(self, game, action, state):
        reward = 0
        prev_state = state
        if action >= game.players[1].count_cards_in_hand():
            game.draw_card(1)
            reward = -1
        elif game.play_card(1, action):
            card_played = game.deck.get_top_discarded_card()
            if card_played.value == "Draw Two":
                reward += 2
            elif card_played.value == "Wild Draw Four":
                reward += 4
            elif card_played.value == "Skip":
                reward += 1
            elif card_played.value == "Wild":
                reward += 3
            if game.is_color_changed:
                game.change_color(state.most_common_color)
            reward = +10
        else:
            reward = -10
        if game.check_winner() == game.players[1]:

            reward += 10
        elif game.check_winner() == game.players[0]:
            reward -= 10
        else:
            game.track_turn()
            game.random_move(0)
        next_game_state = GameState(game)
        next_state = next_game_state
        action_effectiveness = self.calculate_action_effectiveness(prev_state, next_state)
        reward += action_effectiveness
        return reward
    
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