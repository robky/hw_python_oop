class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: 'Training',
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        """
        Установить атрибуты для объекта.

        Параметры
        ---------
        training_type - тип тренировки;
        duration — длительность тренировки;
        distance — дистанция, преодолённая за тренировку;
        speed — средняя скорость движения;
        calories — потраченные за время тренировки килокалории.
        """
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть расчитанные значения в нужном формате с округлением."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    """Константа для перевода значений из метров в километры."""
    MIN_IN_HOUR = 60
    """Константа для перевода значений из часов в минуты."""
    LEN_STEP = 0.65
    """Расстояние, которое спортсмен преодолевает за один шаг в метрах."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        """
        Установить атрибуты для объекта.

        Параметры
        ---------
        action — основное считываемое действие во время тренировки (шаг — бег,
        ходьба; гребок — плавание);
        duration — длительность тренировки;
        weight — вес спортсмена.
        """
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
        return InfoMessage(self,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((18 * self.get_mean_speed() - 20)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)

    def __str__(self) -> str:
        """Получить тип тренировки"""
        return 'Running'


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        """
        Установить атрибуты для объекта.

        Параметры
        ---------
        action — основное считываемое действие во время тренировки (шаг — бег,
        ходьба; гребок — плавание);
        duration — длительность тренировки;
        weight — вес спортсмена;
        height — рост спортсмена.
        """
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((0.035 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * 0.029 * self.weight) * self.duration * self.MIN_IN_HOUR)

    def __str__(self) -> str:
        """Получить тип тренировки"""
        return 'SportsWalking'


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    """Расстояние, которое спортсмен преодолевает за один гребок в метрах."""

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        """
        Установить атрибуты для объекта.

        Параметры
        ---------
        action — основное считываемое действие во время тренировки (шаг — бег,
        ходьба; гребок — плавание);
        duration — длительность тренировки;
        weight — вес спортсмена;
        length_pool — длина бассейна;
        count_pool — количество проплытых бассейнов.
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + 1.1) * 2 * self.weight

    def __str__(self) -> str:
        """Получить тип тренировки"""
        return 'Swimming'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'RUN':
        return Running(*data)
    elif workout_type == 'WLK':
        return SportsWalking(*data)
    else:
        return Swimming(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
