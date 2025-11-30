import random
from typing import List, Tuple, Dict, Any

# --- Базовая реализация для 2-х клеток (Задание 1-4) ---

class VacuumWorld2:
    """Моделирует мир пылесоса с двумя клетками (A и B)."""
    
    def __init__(self, initial_dirty: Tuple[bool, bool], agent_pos: int = 0):
        """
        initial_dirty: кортеж (dirty_A, dirty_B) - True, если грязно[cite: 28].
        agent_pos: 0 для A, 1 для B[cite: 29].
        """
        # self.cells: [A, B], True = Dirty, False = Clean [cite: 31]
        self.cells = [bool(initial_dirty[0]), bool(initial_dirty[1])]
        self.agent_pos = agent_pos # 0=A, 1=B [cite: 33]

    def get_percept(self) -> Tuple[str, str]:
        """Возвращает текущее восприятие агента (локация, статус)[cite: 34]."""
        loc = 'A' if self.agent_pos == 0 else 'B' [cite: 35]
        status = 'Dirty' if self.cells[self.agent_pos] else 'Clean' [cite: 36]
        return loc, status

    def apply_action(self, action: str):
        """Реализует действие агента в среде."""
        if action == 'Suck':
            # Убрать грязь в текущей клетке [cite: 20]
            self.cells[self.agent_pos] = False
        elif action == 'Right' and self.agent_pos == 0:
            # Переместиться из A в B [cite: 11]
            self.agent_pos = 1
        elif action == 'Left' and self.agent_pos == 1:
            # Переместиться из B в A [cite: 12]
            self.agent_pos = 0
        # NoOp или невалидное действие - состояние не меняется

    def get_state(self) -> Dict[str, str]:
        """Возвращает текущее состояние мира[cite: 38]."""
        return {
            'A': 'Dirty' if self.cells[0] else 'Clean', [cite: 39]
            'B': 'Dirty' if self.cells[1] else 'Clean', [cite: 40]
            'agent_pos': 'A' if self.agent_pos == 0 else 'B' [cite: 41]
        }

    def reward(self, mode='both_clean') -> float:
        """
        Подсчет показателя производительности[cite: 13, 42].
        'both_clean': +1.0, если оба чистые, иначе 0.0[cite: 44, 47].
        'per_cell': +1 за каждую чистую клетку (0..2)[cite: 43, 46].
        """
        if mode == 'both_clean':
            # +1 за каждый шаг, когда оба квадрата чистые [cite: 13]
            return 1.0 if (not self.cells[0] and not self.cells[1]) else 0.0
        elif mode == 'per_cell':
            return (0 if self.cells[0] else 1) + (0 if self.cells[1] else 1) [cite: 46]
        else:
            raise ValueError("Unknown reward mode") [cite: 48]


class ReflexAgent2:
    """Простой рефлексный агент для 2-х клеток."""

    def act(self, percept: Tuple[str, str]) -> str:
        """Таблица правил[cite: 19]."""
        loc, status = percept [cite: 51]
        if status == 'Dirty':
            return 'Suck' # если квадрат грязный -> Suck [cite: 10, 20, 52, 53]
        else: # статус 'Clean'
            # иначе: если в А -> Right, если в В -> Left [cite: 21, 54, 55]
            return 'Right' if loc == 'A' else 'Left'


# --- Расширенная реализация для 3-х клеток и Случайного агента (Задания) ---

class VacuumWorld3(VacuumWorld2):
    """Моделирует мир с тремя клетками (A, B, C) и вероятностью появления грязи."""
    
    LOCATIONS = ['A', 'B', 'C']

    def __init__(self, initial_dirty: Tuple[bool, bool, bool], agent_pos: int = 0, p_dirty: float = 0.2):
        # self.cells: [A, B, C], True = Dirty, False = Clean
        self.cells = list(initial_dirty)
        self.agent_pos = agent_pos # 0=A, 1=B, 2=C
        self.p_dirty = p_dirty # Вероятность появления грязи на каждом шаге 

    def get_percept(self) -> Tuple[str, str]:
        loc = self.LOCATIONS[self.agent_pos]
        status = 'Dirty' if self.cells[self.agent_pos] else 'Clean'
        return loc, status

    def _introduce_new_dirt(self):
        """Вводит грязь в каждую клетку с вероятностью p_dirty."""
        for i in range(len(self.cells)):
            if random.random() < self.p_dirty:
                self.cells[i] = True

    def apply_action(self, action: str):
        # Применить действие как в 2-х клеточном мире (Suck, Left, Right)
        if action == 'Suck':
            self.cells[self.agent_pos] = False
        elif action == 'Right':
            self.agent_pos = (self.agent_pos + 1) % len(self.cells) # A->B->C->A
        elif action == 'Left':
            self.agent_pos = (self.agent_pos - 1) % len(self.cells) # A->C->B->A
        elif action == 'NoOp':
            pass # Разрешить агенту делать «NoOp» (ничего не делать) [cite: 95]
        
        # После действия, вводим новую грязь
        self._introduce_new_dirt()

    def get_state(self) -> Dict[str, str]:
        state = {self.LOCATIONS[i]: 'Dirty' if self.cells[i] else 'Clean' for i in range(len(self.cells))}
        state['agent_pos'] = self.LOCATIONS[self.agent_pos]
        return state

    def reward(self, mode='both_clean') -> float:
        """Награда: количество чистых клеток."""
        if mode == 'per_cell':
            return sum(1 for dirty in self.cells if not dirty)
        else: # both_clean теперь означает "все чистые"
            return 1.0 if all(not dirty for dirty in self.cells) else 0.0


class RandomAgent:
    """Случайный агент."""
    
    def __init__(self, actions: List[str]):
        self.actions = actions # Например: ['Suck', 'Left', 'Right', 'NoOp']

    def act(self, percept: Tuple[str, str]) -> str:
        loc, status = percept
        if status == 'Dirty':
            return 'Suck'
        else:
            # Выбирает случайное направление/действие, если клетка чистая 
            return random.choice([a for a in self.actions if a != 'Suck'])


# --- Общая функция симуляции ---

def simulate(world: Any, agent: Any, steps: int = 10, reward_mode='both_clean') -> Tuple[List[Dict[str, Any]], float]:
    """
    Запускает симуляцию для мира и агента.
    Возвращает лог и суммарную награду[cite: 74].
    """
    log = [] [cite: 58]
    total_reward = 0.0 [cite: 59]
    for t in range(steps): [cite: 60]
        percept = world.get_percept() [cite: 61]
        action = agent.act(percept) [cite: 62]
        
        # Сохраняем состояние до действия для корректного лога
        state_before_action = world.get_state()

        world.apply_action(action) [cite: 63]
        
        r = world.reward(mode=reward_mode) [cite: 64]
        total_reward += r [cite: 65]
        
        log.append({
            'step': t, [cite: 67]
            'percept': percept, [cite: 68]
            'action': action, [cite: 71]
            'state (post-action)': world.get_state(),
            'reward': r [cite: 73]
        })
    return log, total_reward


# --- Запуск симуляции ---

if __name__ == "__main__":
    
    # ----------------------------------------------------
    # А. Симуляция с Simple Reflex Agent в 2-х клеточном мире (Задание 1-4)
    # ----------------------------------------------------
    print("## Часть A: Simple Reflex Agent в мире 2-х клеток ##")

    # Примеры начальных состояний [cite: 77]
    # (initial_dirty, agent_pos)
    inits_2_cell = [
        ((True, False), 0), # A=Dirty, B=Clean, agent in A [cite: 78]
        ((True, True), 0),  # Оба грязные, агент в A [cite: 79]
        ((False, False), 1) # Оба чистые, агент в B [cite: 81]
    ]

    for initial_dirty, pos in inits_2_cell: [cite: 82]
        # Используем режим награды 'both_clean' (+1 только когда обе чистые)
        REWARD_MODE = 'both_clean' 
        
        W = VacuumWorld2(initial_dirty, agent_pos=pos) [cite: 83]
        A = ReflexAgent2() [cite: 85]
        
        log, total = simulate(W, A, steps=10, reward_mode=REWARD_MODE) [cite: 86]
        
        print(f"\nInit: {initial_dirty}, start: {'A' if pos == 0 else 'B'}") [cite: 86]
        print(f"Конфигурация (Dirty=True): A={initial_dirty[0]}, B={initial_dirty[1]}")

        for entry in log: [cite: 87]
            # Выводим только ключевую информацию для краткости
            print(f"Шаг {entry['step']}: P={entry['percept']}, A={entry['action']}, S={entry['state (post-action)']['A']}-{entry['state (post-action)']['B']} @ {entry['state (post-action)']['agent_pos']}, R={entry['reward']}")
        
        print(f"Суммарная reward: {total}") [cite: 89]
        print(f"Средняя reward: {total / len(log):.2f}")
        print("="*40) [cite: 90]


    # ----------------------------------------------------
    # Б. Сравнение агентов в расширенном 3-х клеточном мире (Задания 1-4)
    # ----------------------------------------------------
    print("\n## Часть Б: Сравнение агентов в мире 3-х клеток с новой грязью (p=0.2) ##")
    
    STEPS = 100 # Больше шагов для лучшего среднего показателя
    NUM_RUNS = 5 # Количество запусков для усреднения
    REWARD_MODE = 'per_cell' # Лучше использовать 'per_cell' для сравнения в динамическом мире

    # Начальная конфигурация: все грязные, агент в A
    initial_dirty_3_cell = (True, True, True) 
    start_pos = 0 # Агент в A
    
    # 1. Сравнение Простого Рефлексного Агента (3 клетки)
    print("\n--- Простой Рефлексный Агент (3 клетки) ---")
    
    class ReflexAgent3(ReflexAgent2):
        """Агент для 3-х клеток. Добавлено действие NoOp[cite: 95]."""
        def act(self, percept: Tuple[str, str]) -> str:
            loc, status = percept
            if status == 'Dirty':
                return 'Suck'
            else:
                # В мире 3-х клеток, если чисто, двигаемся вправо (A->B->C->A)
                return 'Right'


    total_rewards_reflex = []
    for _ in range(NUM_RUNS):
        W = VacuumWorld3(initial_dirty_3_cell, agent_pos=start_pos)
        A = ReflexAgent3()
        _, total = simulate(W, A, steps=STEPS, reward_mode=REWARD_MODE)
        total_rewards_reflex.append(total)

    avg_reward_reflex = sum(total_rewards_reflex) / NUM_RUNS / STEPS
    print(f"Средний Total Reward (за {NUM_RUNS} запусков, {STEPS} шагов): {sum(total_rewards_reflex) / NUM_RUNS:.2f}")
    print(f"Средний Reward за шаг: {avg_reward_reflex:.3f}")
    
    
    # 2. Сравнение Случайного Агента (3 клетки)
    print("\n--- Случайный Агент (3 клетки) ---")
    
    # Случайный агент выбирает из Suck, Left, Right, NoOp
    random_agent_actions = ['Suck', 'Left', 'Right', 'NoOp'] [cite: 95]
    
    total_rewards_random = []
    for _ in range(NUM_RUNS):
        W = VacuumWorld3(initial_dirty_3_cell, agent_pos=start_pos)
        # Случайный агент выбирает из всех действий, если не Dirty
        A = RandomAgent(random_agent_actions)
        _, total = simulate(W, A, steps=STEPS, reward_mode=REWARD_MODE)
        total_rewards_random.append(total)

    avg_reward_random = sum(total_rewards_random) / NUM_RUNS / STEPS
    print(f"Средний Total Reward (за {NUM_RUNS} запусков, {STEPS} шагов): {sum(total_rewards_random) / NUM_RUNS:.2f}")
    print(f"Средний Reward за шаг: {avg_reward_random:.3f}")
    
    print("\n--- Сводка сравнения ---")
    print(f"Простой Рефлексный Агент (средний R/шаг): {avg_reward_reflex:.3f}")
    print(f"Случайный Агент (средний R/шаг): {avg_reward_random:.3f}")
    print("="*40)
