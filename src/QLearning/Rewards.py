import random
import itertools
import csv

def actions():
    colors = ["Red", "Green", "Blue", "Yellow"]
    possible_actions = []
    for color in colors:
        possible_actions.append(f"Play {color}")
    for color in colors:
        possible_actions.append(f"Play {color} Skip")
        possible_actions.append(f"Play {color} Draw Two")
    possible_actions.append("Play All Wild")
    possible_actions.append("Play All Wild Draw Four")
    possible_actions.append("Draw Card")
    return possible_actions

def states(sample_size=None):
    basic_cards = {"Red Card": 2, "Green Card": 2, "Blue Card": 2, "Yellow Card": 2}
    special_cards = {
        "Red Skip": 1, "Green Skip": 1, "Blue Skip": 1, "Yellow Skip": 1,
        "Red Draw Two": 1, "Green Draw Two": 1, "Blue Draw Two": 1, "Yellow Draw Two": 1
    }
    wild_cards = {"Wild": 1, "Wild Draw Four": 1}
    opponent_cards = {"Opponent cards": 4}
    colors = ["Red", "Green", "Blue", "Yellow"]
    values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Draw Two", "Wild", "Wild Draw Four"]
    states_dict = {
        **basic_cards,
        **special_cards,
        **wild_cards,
        "Top Card Color": len(colors) - 1,
        "Top Card Value": len(values) - 1,
        **opponent_cards
    }
    ranges = [range(0, val + 1) for val in states_dict.values()]
    possible_states = list(itertools.product(*ranges))
    valid_states = [
        state for state in possible_states
        if state[-1] > 0 and sum(state[:-3]) > 0
    ]
    if sample_size:
        sampled_states = random.sample(valid_states, min(sample_size, len(valid_states)))
        return sampled_states, states_dict
    return valid_states, states_dict

if __name__ == "__main__":
    filename = "test_possible_states.csv"
    all_states, states_dict = states()
    first_50_states = all_states[:50]
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=" ")
        headers = list(states_dict.keys())
        writer.writerow(headers)
        writer.writerows(first_50_states)

    print(f"Liczba wygenerowanych stanów: {len(all_states)}")
    print(f"Stany zapisano do pliku: {filename}")