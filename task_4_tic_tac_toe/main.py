import random


class Agent:
    def __init__(self, action_space):
        self.action_space = action_space
        self.epsilon = 0.1  # Начальное значение epsilon-greedy стратегии
        self.discount_factor = 0.9  # Дисконтирование будущего вознаграждения
        self.learning_rate = 0.1  # Скорость обучения модели
        self.exploration_steps = 1000  # Количество шагов для исследования
        self.q_table = {}  # Таблица Q-значений

    def play_game(self, opponent):
        game_history = []
        is_player_turn = True
        while True:
            current_state = self.observe_state()
            if is_player_turn:
                action = self.choose_action(current_state)
                reward, next_state, is_player_turn = opponent.play(action)
                game_history.append((current_state, action, reward, next_state, is_player_turn))
            else:
                _, _, _, _, _ = self.play_game(opponent)

        return game_history

    def observe_state(self):
        return 0  # Предполагаем, что начальное состояние всегда равно 0

    def choose_action(self, state):
        if random.random() > self.epsilon:
            best_action = max(self.q_table[state])
        else:
            best_action = random.choice(list(self.q_table[state]))
        return best_action

    def update_q_table(self, state, action, reward, next_state, is_player_turn):
        if state not in self.q_table:
            self.q_table[state] = {}

        max_next_q = max(self.q_table.get(next_state, {})) if is_player_turn else 0
        self.q_table[state][action] = reward + self.discount_factor * max_next_q

    def train(self, num_episodes=1000):
        game_history = []
        for episode in range(num_episodes):
            opponent = Opponent()
            history = self.play_game(opponent)
            game_history.extend(history)

        for state, actions, rewards, next_states, is_player_turns in game_history:
            for state, action, reward, next_state, is_player_turn in zip(state, actions, rewards, next_states,
                                                                         is_player_turns):
                self.update_q_table(state, action, reward, next_state, is_player_turn)

        return self.q_table


class Opponent:
    def __init__(self):
        pass

    def play(self, action):
        if action == 0:
            return 1, 0, False
        elif action == 1:
            return 0, 0, False

    def observe_state(self):
        return 0  # Предполагаем, что начальное состояние всегда равно 0


if __name__ == '__main__':

    # Создание агентов
    agent = Agent(action_space=[0, 1])
    opponent = Opponent()

    # Игра
    history = agent.play_game(opponent)

    # Печать истории игр
    for h in history:
        print(h)
