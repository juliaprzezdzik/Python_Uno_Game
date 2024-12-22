import pandas as pd
import numpy as np
import itertools

def actions():
    possible_actions = [
        "Play Red",
        "Play Green",
        "Play Blue",
        "Play Yellow",
        "Play Skip",
        "Play Draw Two",
        "Play Wild",
        "Play Wild Draw Four",
        "Draw Card"]
    return possible_actions

def states():
    basic_cards = {"Red": 2, "Green": 2, "Blue": 2, "Yellow": 2}
    special_cards = {"Skip": 1, "Draw Two": 1}
    wild_cards = {"Wild": 1, "Wild Draw Four": 1}
    basic_cards_discarded = {"Red discarded": 2, "Green discarded": 2, "Blue discarded": 2, "Yellow discarded": 2}
    special_cards_discarded = {"Skip discarded": 1, "Draw Two discarded": 1}
    states_dict = {
        **basic_cards,
        **special_cards,
        **wild_cards,
        **basic_cards_discarded,
        **special_cards_discarded
    }
    all_states = [range(0, val + 1) for val in states_dict.values()]
    all_states = list(itertools.product(*all_states))

    def is_valid_state(state):
        num_basic_cards = len(basic_cards)
        offset = len(basic_cards) + len(special_cards) + len(wild_cards)
        for i in range(num_basic_cards):
            if state[i] < state[offset + i]:
                return False
        for i in range(len(special_cards)):
            if state[num_basic_cards + i] < state[offset + num_basic_cards + i]:
                return False
        return True

    possible_states = [state for state in all_states if is_valid_state(state)]
    return possible_states, states_dict


def rewards(states, actions):
    R = np.zeros((len(states), len(actions)))
    basic_cards_indices = slice(0, 4)
    special_cards_indices = slice(4, 6)
    states_t = [
        min(sum(state[basic_cards_indices]) + sum(state[special_cards_indices]), 1)
        for state in states
    ]
    for i in range(len(states)):
        if states_t[i] == 0:
            R[i, :] = 1
        else:
            R[i, actions.index("Draw Card")] -= 0.2
            R[i, actions.index("Play Wild")] += 0.7
    R = pd.DataFrame(
        data=R,
        columns=actions,
        index=states
    )
    return R

if __name__ == "__main__":
    possible_states, states_dict = states()
    possible_actions = actions()
    reward_matrix = rewards(possible_states, possible_actions)
    print(reward_matrix.head())
    reward_matrix.to_csv("reward_matrix.csv")