import unittest
from src.Deck import Card
from Environment import Environment

class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.env = Environment()

    def test_define_actions(self):
        actions = self.env.action_space
        self.assertIn("Draw Card", actions)
        for color in ["Red", "Green", "Blue", "Yellow"]:
            self.assertIn(f"Play Wild {color}", actions)
            self.assertIn(f"Play Wild Draw Four {color}", actions)
        self.assertIn("Play Red 0", actions)
        self.assertIn("Play Red Skip", actions)
        self.assertIn("Play Blue 9", actions)
        self.assertEqual(len(actions), 57,"The number of defined actions should be 57.")

    def test_reset_test_setup(self):
        state = self.env.reset(test_setup=True)
        self.assertEqual(self.env.current_player, 0)
        player0_cards = self.env.game.players[0].cards_in_hand
        expected_p0 = [
            ("Draw Two", "Green"),
            ("5", "Red"),
            ("Wild", "All")
        ]
        actual_p0 = [(c.value, c.color) for c in player0_cards]
        self.assertListEqual(actual_p0, expected_p0,"Player hand 0 is not as expected in test_setup.")
        player1_cards = self.env.game.players[1].cards_in_hand
        expected_p1 = [
            ("3", "Yellow"),
            ("4", "Blue")
        ]
        actual_p1 = [(c.value, c.color) for c in player1_cards]
        self.assertListEqual(actual_p1, expected_p1,"Player 1 hand is not as expected in test_setup.")
        discarded = self.env.game.deck.discarded
        self.assertEqual(len(discarded), 1, "There should be 1 card in the discard pile.")
        top_discard = discarded[-1]
        self.assertEqual((top_discard.value, top_discard.color), ("3", "Green"),"On the pile should lie card (3, Green).")
        expected_state = (3, 2, 1, 3, 0, 1, 1, 0)
        self.assertEqual(state, expected_state,"The game state after reset(test_setup=True) is not as expected.")

    def test_action_to_card(self):
        self.env.reset(test_setup=True)
        player = self.env.game.players[0]
        card, chosen_color = self.env.action_to_card("Play Wild Red", player)
        self.assertIsNotNone(card)
        self.assertEqual(card.value, "Wild")
        self.assertEqual(card.color, "All")
        self.assertEqual(chosen_color, "Red")
        card, chosen_color = self.env.action_to_card("Play Green Draw Two", player)
        self.assertIsNotNone(card)
        self.assertEqual(card.value, "Draw Two")
        self.assertEqual(card.color, "Green")
        self.assertIsNone(chosen_color)
        card, chosen_color = self.env.action_to_card("Play Red 99", player)
        self.assertIsNone(card)
        self.assertIsNone(chosen_color)

    def test_is_valid_action(self):
        self.env.reset(test_setup=True)
        self.assertTrue(self.env.is_valid_action("Play Green Draw Two"))
        self.assertFalse(self.env.is_valid_action("Play Red 5"))
        self.assertTrue(self.env.is_valid_action("Play Wild Blue"))
        self.assertTrue(self.env.is_valid_action("Draw Card"))
        self.assertFalse(self.env.is_valid_action("Play Red Draw Two"))

    def test_step_draw_card(self):
        self.env.reset(test_setup=True)
        initial_hand_size = len(self.env.game.players[0].cards_in_hand)
        next_state, reward, done = self.env.step("Draw Card")
        self.assertEqual(len(self.env.game.players[0].cards_in_hand), initial_hand_size + 1)
        expected_reward = -0.8
        self.assertAlmostEqual(reward, expected_reward, places=5, msg=f"Reward should be around {expected_reward} for 'Draw Card' with 3 cards in hand.")
        self.assertFalse(done, "The game should not end when a card is drawn.")
        self.assertEqual(self.env.current_player, 1,"After player 0 performs the action, it should be player 1 turn.")

    def test_step_play_valid_card(self):
        self.env.reset(test_setup=True)
        player0 = self.env.game.players[0]
        initial_hand_size = len(player0.cards_in_hand)
        next_state, reward, done = self.env.step("Play Green Draw Two")
        self.assertEqual(len(player0.cards_in_hand), initial_hand_size - 1,"Playing a card should reduce the number of cards in a player's hand by 1.")
        self.assertTrue(reward > 0,f"Reward should be positive for playing 'Draw Two'. Received: {reward}")
        self.assertFalse(done)
        self.assertEqual(self.env.current_player, 1)

    def test_step_play_invalid_card(self):
        self.env.reset(test_setup=True)
        next_state, reward, done = self.env.step("Play Red 5")
        expected_reward = -29.8
        self.assertAlmostEqual(reward, expected_reward, places=5, msg=f"Incorrect action should give a penalty close to {expected_reward}.")
        self.assertFalse(done, "The game should not end with an incorrect move.")
        self.assertEqual(self.env.current_player, 0,"After an incorrect move, the turn should remain with player 0.")

    def test_step_game_ends(self):
        self.env.reset(test_setup=True)
        player0 = self.env.game.players[0]
        player0.cards_in_hand = [Card("Wild", "All")]
        next_state, reward, done = self.env.step("Play Wild Red")
        self.assertTrue(done, "The game should end if the player has played the last card.")
        self.assertGreater(reward, 0, "The reward for winning a turn should be positive.")
        self.assertEqual(self.env.current_player, 0,"Current_player does not need to change, because the game ends.")

if __name__ == '__main__':
    unittest.main()