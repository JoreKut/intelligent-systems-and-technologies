import numpy as np
import matplotlib.pyplot as plt
import random

# Параметры среды
NUM_GLASSES = 5
MAX_STEPS = 1000  # Максимальное количество шагов в одном эпизоде
EPISODES = 1000  # Количество эпизодов обучения
ALPHA = 0.1  # Скорость обучения
GAMMA = 0.9  # Коэффициент дисконтирования
EPSILON = 0.1  # Вероятность случайного действия (ε-грейди)

# Создаем среду
class GlassEnvironment:
    def __init__(self):
        self.reset()

    def reset(self):
        """Сбрасывает состояние стаканов."""
        while True:
            state = np.random.randint(0, 250, NUM_GLASSES)
            if sum(state) % 5 == 0:
                self.state = state
                break
        # self.state = np.random.randint(0, 250, NUM_GLASSES)
        # self.state = [1,19,5,10,5]
        return self.state

    def step(self, action):
        """Выполняет действие и возвращает новую ситуацию."""
        from_glass, to_glass = action
        diff = float(self.state[from_glass] - self.state[to_glass]) // 2.0
        self.state[from_glass] -= diff
        self.state[to_glass] += diff
        
        # Награда за выравнивание
        std_before = np.std(self.state) + diff
        std_after = np.std(self.state)
        reward = std_before - std_after  # Положительная награда за уменьшение разброса
        
        # Дополнительная награда за достижение цели
        done = std_after < 1e-2
        if done:
            reward += 100
        
        return self.state, reward, done

    def get_all_possible_actions(self):
        """Возвращает все возможные действия (переливания)."""
        return [(i, j) for i in range(NUM_GLASSES) for j in range(NUM_GLASSES) if i != j]

# Создаем обучающегося агента
class QLearningAgent:
    def __init__(self, actions):
        self.q_table = {}  # Q-таблица
        self.actions = actions  # Возможные действия

    def choose_action(self, state, epsilon):
        """Выбор действия: либо случайно, либо на основе Q-таблицы."""
        state_key = tuple(state)
        if random.uniform(0, 1) < epsilon or state_key not in self.q_table:
            return random.choice(self.actions)  # Случайное действие
        return max(self.q_table[state_key], key=self.q_table[state_key].get)  # Наилучшее действие

    def learn(self, state, action, reward, next_state):
        """Обновление Q-таблицы."""
        state_key = tuple(state)
        next_state_key = tuple(next_state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0 for a in self.actions}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {a: 0 for a in self.actions}
        q_predict = self.q_table[state_key][action]
        q_target = reward + GAMMA * max(self.q_table[next_state_key].values())
        self.q_table[state_key][action] += ALPHA * (q_target - q_predict)

# Основной цикл обучения
def train():
    env = GlassEnvironment()
    actions = env.get_all_possible_actions()
    q_agent = QLearningAgent(actions)
    rewards = []
    final_states = []  # Для хранения итоговых состояний стаканов

    for episode in range(EPISODES):
        state = env.reset()
        # print(f"Начало: {state}")
        total_reward = 0
        for step in range(MAX_STEPS):
            # Агент выбирает действие
            action = q_agent.choose_action(state, EPSILON)
            # Выполняем шаг
            next_state, reward, done = env.step(action)
            # Агент обучается
            q_agent.learn(state, action, reward, next_state)
            state = next_state
            total_reward += reward
            # print(f"\t {state}")
            if done:
                break

        rewards.append(total_reward)
        final_states.append(state.copy())  # Сохраняем состояние стаканов после эпизода

        # Периодически выводим результаты
        # if episode % 500 == 0:
        print(f"Эпизод {episode}: Награда = {total_reward:.2f}, Финальное состояние стаканов = {state}")

    return rewards, final_states

# Построение графика и вывод результатов
rewards, final_states = train()

# График наград
plt.plot(rewards)
plt.xlabel("Эпизоды обучения")
plt.ylabel("Награда")
plt.title("Зависимость награды от количества шагов обучения")
plt.show()

# Вывод итоговых состояний стаканов для первых и последних эпизодов
print("\nПримеры финальных состояний стаканов:")
print(f"После первого эпизода: {final_states[0]}")
print(f"После последнего эпизода: {final_states[-1]}")