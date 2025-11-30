import random
from typing import List, Tuple, Dict, Any


# ==========================================
# ЧАСТЬ 1: Базовая реализация (Задания 1-4)
# ==========================================

class VacuumWorld2:
    """
    Моделирует мир пылесоса с двумя клетками (A и B).
    """

    def __init__(self, initial_dirty: Tuple[bool, bool], agent_pos: int = 0):
        # Преобразуем в список, чтобы можно было менять значения
        self.cells = [bool(initial_dirty[0]), bool(initial_dirty[1])]
        self.agent_pos = agent_pos  # 0=A, 1=B

    def get_percept(self) -> Tuple[str, str]:
        """ Возвращает текущее восприятие агента (локация, статус). """
        loc = 'A' if self.agent_pos == 0 else 'B'
        status = 'Dirty' if self.cells[self.agent_pos] else 'Clean'
        return loc, status

    def apply_action(self, action: str):
        """ Реализация действий агента. """
        if action == 'Suck':
            # Убрать грязь в текущей клетке
            self.cells[self.agent_pos] = False
        elif action == 'Right' and self.agent_pos == 0:
            # Переход A -> B
            self.agent_pos = 1
        elif action == 'Left' and self.agent_pos == 1:
            # Переход B -> A
            self.agent_pos = 0
        else:
            # NoOp или некорректное действие
            pass

    def get_state(self) -> Dict[str, str]:
        """ Возвращает состояние для логов. """
        return {
            'A': 'Dirty' if self.cells[0] else 'Clean',
            'B': 'Dirty' if self.cells[1] else 'Clean',
            'agent_pos': 'A' if self.agent_pos == 0 else 'B'
        }

    def reward(self, mode='per_cell') -> float:
        """ Подсчет награды. """
        if mode == 'both_clean':
            # +1 если обе клетки чистые
            return 1.0 if (not self.cells[0] and not self.cells[1]) else 0.0
        elif mode == 'per_cell':
            # +1 за каждую чистую клетку
            score = 0
            if not self.cells[0]: score += 1
            if not self.cells[1]: score += 1
            return float(score)
        else:
            raise ValueError("Unknown reward mode")


class ReflexAgent2:
    """ Простой рефлексный агент. """

    def act(self, percept: Tuple[str, str]) -> str:
        loc, status = percept
        if status == 'Dirty':
            return 'Suck'
        else:
            return 'Right' if loc == 'A' else 'Left'


# ==========================================
# ЧАСТЬ 2: Расширенная версия (3 клетки, Random)
# ==========================================

class VacuumWorld3(VacuumWorld2):
    """
    Мир с тремя клетками (A, B, C).
    """
    LOCATIONS = ['A', 'B', 'C']

    def __init__(self, initial_dirty: Tuple[bool, bool, bool], agent_pos: int = 0, p_dirty: float = 0.2):
        # Инициализируем родителя, но перезапишем cells, так как тут их 3
        # Передаем заглушку (False, False), чтобы родительский __init__ не ругался
        super().__init__((False, False), agent_pos)

        self.cells = list(initial_dirty)
        self.agent_pos = agent_pos
        self.p_dirty = p_dirty

    def get_percept(self) -> Tuple[str, str]:
        # Переопределяем, так как теперь есть локация 'C'
        loc = self.LOCATIONS[self.agent_pos]
        status = 'Dirty' if self.cells[self.agent_pos] else 'Clean'
        return loc, status

    def _introduce_new_dirt(self):
        """ Случайное появление грязи. """
        for i in range(len(self.cells)):
            if random.random() < self.p_dirty:
                self.cells[i] = True

    def apply_action(self, action: str):
        if action == 'Suck':
            self.cells[self.agent_pos] = False
        elif action == 'Right':
            # Циклическое движение: 0->1->2->0
            self.agent_pos = (self.agent_pos + 1) % len(self.cells)
        elif action == 'Left':
            # Циклическое движение: 0->2->1->0
            self.agent_pos = (self.agent_pos - 1) % len(self.cells)
        elif action == 'NoOp':
            pass

        self._introduce_new_dirt()

    def get_state(self) -> Dict[str, str]:
        state = {self.LOCATIONS[i]: 'Dirty' if self.cells[i] else 'Clean' for i in range(len(self.cells))}
        state['agent_pos'] = self.LOCATIONS[self.agent_pos]
        return state

    def reward(self, mode='per_cell') -> float:
        return float(sum(1 for dirty in self.cells if not dirty))


class RandomAgent:
    """ Случайный агент. """

    def __init__(self, actions: List[str]):
        self.actions = actions

    def act(self, percept: Tuple[str, str]) -> str:
        loc, status = percept
        if status == 'Dirty':
            return 'Suck'

        # Фильтруем действия, чтобы не делать Suck на чистой клетке
        safe_actions = [a for a in self.actions if a != 'Suck']
        return random.choice(safe_actions)


# ==========================================
# ЧАСТЬ 3: Симуляция
# ==========================================

def simulate(world: Any, agent: Any, steps: int = 10, reward_mode='per_cell') -> Tuple[List[Dict[str, Any]], float]:
    log = []
    total_reward = 0.0

    for t in range(steps):
        percept = world.get_percept()
        action = agent.act(percept)

        # Применяем действие
        world.apply_action(action)

        # Считаем награду
        r = world.reward(mode=reward_mode)
        total_reward += r

        log.append({
            'step': t,
            'percept': percept,
            'action': action,
            'state': world.get_state(),
            'reward': r
        })

    return log, total_reward


if __name__ == "__main__":
    print("## Лабораторная работа №2 ##\n")

    # Конфигурации для задания 4
    # (Dirty A, Dirty B), Agent Pos (0=A, 1=B)
    configs = [
        ((True, False), 0),
        ((True, True), 0),
        ((False, False), 1)
    ]

    for init_dirty, pos in configs:
        start_loc = 'A' if pos == 0 else 'B'
        print(f"--- Старт: Грязь={init_dirty}, Агент={start_loc} ---")

        w = VacuumWorld2(init_dirty, agent_pos=pos)
        a = ReflexAgent2()

        # Запуск симуляции
        # reward_mode='both_clean' (+1 только если ВСЁ чисто)
        log_data, total_score = simulate(w, a, steps=10, reward_mode='both_clean')

        for entry in log_data:
            s = entry['state']
            state_str = f"A={s['A']}, B={s['B']} @ {s['agent_pos']}"
            print(f"Шаг {entry['step']}: {entry['percept']} -> {entry['action']} | {state_str} | R={entry['reward']}")

        print(f"Итоговый Reward: {total_score}\n")

    # Тест дополнительных заданий (VacuumWorld3 + RandomAgent)
    print("--- Тест: Мир 3 клетки + Случайный агент ---")
    w3 = VacuumWorld3((True, True, True), agent_pos=0, p_dirty=0.2)
    ra = RandomAgent(['Suck', 'Left', 'Right', 'NoOp'])

    log3, total3 = simulate(w3, ra, steps=5, reward_mode='per_cell')
    print(f"Случайный агент (5 шагов), Reward: {total3}")
