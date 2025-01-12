import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.stats import gaussian_kde
from ReplayBuffer import CustomReplayBuffer

def get_reward_statistics(storage):
    rewards = [transition['reward'].item() for transition in storage]
    return {
        'mean': np.mean(rewards),
        'std': np.std(rewards),
        'min': np.min(rewards),
        'max': np.max(rewards)
    }

def plot_reward_distribution(storage):
    if len(storage) == 0:
        return
    rewards = [transition['reward'].item() for transition in storage]
    plt.figure(figsize=(10, 6))
    plt.hist(rewards, bins=30, alpha=0.7, edgecolor='black', density=False)
    kde = gaussian_kde(rewards)
    x_vals = np.linspace(min(rewards), max(rewards), 1000)
    plt.plot(x_vals, kde(x_vals) * len(rewards) * (max(rewards) - min(rewards)) / 30,color='red', linewidth=2, label='KDE')
    plt.title('Distribution of rewards')
    plt.xlabel('Reward')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

def plot_action_distribution(storage):
    if len(storage) == 0:
        return
    actions = [transition['action'].item() for transition in storage]
    action_counts = {}
    for action in actions:
        action_counts[action] = action_counts.get(action, 0) + 1
    actions_sorted = sorted(action_counts.keys())
    counts_sorted = [action_counts[a] for a in actions_sorted]
    plt.figure(figsize=(10, 6))
    plt.bar(actions_sorted, counts_sorted, color='skyblue', edgecolor='black')
    plt.title('Distribution of actions')
    plt.xlabel('Action')
    plt.ylabel('Number')
    plt.xticks(actions_sorted)
    plt.show()

def visualize_rewards_distribution(storage):
    if len(storage) == 0:
        return
    rewards = [transition['reward'].item() for transition in storage]
    plt.figure(figsize=(8, 5))
    plt.hist(rewards, bins=20, color='blue', edgecolor='black', alpha=0.7)
    plt.title("Histogram of rewards")
    plt.xlabel("Reward")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()

def visualize_transitions(storage, state_dim, num_samples=3):
    if len(storage) == 0 or state_dim <= 1:
        return
    sample_indices = random.sample(range(len(storage)), min(num_samples, len(storage)))
    transitions = [storage[idx] for idx in sample_indices]
    plt.figure(figsize=(10, 6))
    for i, t in enumerate(transitions):
        state = t["state"].tolist()
        next_state = t["next_state"].tolist()
        action = t["action"].item()
        plt.plot(state, label=f"State {i + 1}", marker='o')
        plt.plot(next_state, label=f"Next State {i + 1}", marker='x')
        if len(state) > 0:
            plt.annotate(f"Action: {action}", (len(state) - 1, state[-1]))
    plt.title("Sampled Transitions Visualization")
    plt.xlabel("Dimension index")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    buffer = CustomReplayBuffer(max_size=10000, state_dim=4, n_actions=2)
    for _ in range(1000):
        state = np.random.randn(4)
        action = np.random.randint(0, 2)
        reward = np.random.randn()
        next_state = np.random.randn(4)
        done = np.random.choice([True, False])
        buffer.store_transition(state, action, reward, next_state, done, priority=1.0)

    stats = get_reward_statistics(buffer.storage)
    print(f"Rewards statistics: {stats}")
    plot_reward_distribution(buffer.storage)
    plot_action_distribution(buffer.storage)
    visualize_rewards_distribution(buffer.storage)
    visualize_transitions(buffer.storage, state_dim=4, num_samples=3)
    batch_size = 5
    samples_priority = buffer.sample_with_priority(batch_size=batch_size, alpha=0.6)
    print("Sampled transitions (priority-based): ")
    for i in range(batch_size):
        print(f"Transition {i + 1}, Reward = {samples_priority['rewards'][i].item():.2f}, "
              f"Priority = {buffer.storage[samples_priority['indices'][i]]['priority'].item():.2f}")
    new_priorities = [abs(samples_priority['rewards'][i].item()) + 0.01 for i in range(batch_size)]
    buffer.update_priorities(samples_priority['indices'], new_priorities)
    print("\nUpdated priorities based on absolute reward + 0.01")
    for i, idx in enumerate(samples_priority['indices']):
        print(f"Index {idx}, new priority = {buffer.storage[idx]['priority'].item():.2f}")
