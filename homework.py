"""
Фитнес-трекер, который обрабатывает данные для трёх видов тренировок:
бега, спортивной ходьбы и плавания.
"""


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type}; "
                f"Длительность: {self.duration:.3f} ч.; "
                f"Дистанция: {self.distance:.3f} км; "
                f"Ср. скорость: {self.speed:.3f} км/ч; "
                f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration, self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    MINUTES = 60

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:  # Переопределение метода базового класса
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * super().get_mean_speed() +
                 self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM * (self.MINUTES * self.duration))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1 = 0.035  # Коэффициент для расчёта калорий
    K_2 = 0.029
    MINUTES = 60
    M_IN_KM = 100

    def __init__(self, action: int, duration: float, weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        # Числовым коэффициентам тоже нужны имена, не стоит забывать про это.
        # Но это не касается, например, значения степени.
        # ms = 16.263
        ms = super().get_mean_speed() * (1000 / 3600)
        return ((self.K_1 * self.weight + (ms ** 2 / self.height)
                 * self.K_2 * self.weight) * self.MINUTES * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    M_IN_KM = Training.M_IN_KM

    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:  # Переопределение метода базового класса
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + 1.1) * 2 * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    commands = {
        'SWM': Swimming,  # Плавание
        'RUN': Running,  # Бег
        'WLK': SportsWalking  # Спортивная ходьба
    }

    return commands[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = InfoMessage
    print(info.get_message(training.show_training_info()))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
