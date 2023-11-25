class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories) -> str:
        self.training_type: str = training_type #имя класса тренировки
        self.duration: float = duration #длительность тренировки в часах
        self.distance: float = distance #дистанция в километрах, которую преодолел пользователь за время тренировки
        self.speed: float = speed #средняя скорость, с которой двигался пользователь
        self.calories: float = calories #количество килокалорий, которое израсходовал пользователь за время тренировки
        print(self)
 
    def get_message(self):
        return (f"Тип тренировки: {self.training_type}; " 
                f"Длительность: {self.duration:.3f} ч.; " 
                f"Дистанция: {self.distance:.3f} км; " 
                f"Ср. скорость: {self.speed:.3f} км/ч; " 
                f"Потрачено ккал: {self.calories:.3f}.")
    

class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MINUTES_IN_HOUR = 60
    def __init__(self,
                 action: int,     #количество совершённых действий (число шагов при ходьбе и беге либо гребков — при плавании);
                 duration: float, #длительность тренировки;
                 weight: float,   #вес спортсмена.
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight


    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return(self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        dist = Training.get_distance(self)
        return(dist / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass
    
    #def get_training_type(self):
       # return type(self).__name__


    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message_to_return = InfoMessage(
                            type(self).__name__,
                            self.duration,
                            self.get_distance(),
                            self.get_mean_speed(),
                            self.get_spent_calories())
        return message_to_return
    """Вернуть информационное сообщение о выполненной тренировке."""


class Running(Training):
    """Тренировка: бег."""
    #def __init__(self, action: int, duration: float, weight: float) -> None:
       # super().__init__(action, duration, weight)
        #LEN_STEP = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    def get_spent_calories(self) -> float:
        return (((self.CALORIES_MEAN_SPEED_MULTIPLIER 
                  * self.get_mean_speed() 
                  + self.CALORIES_MEAN_SPEED_SHIFT)
                  * self.action / self.M_IN_KM 
                  * (self.duration * 60)))

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, 
                 action: int, 
                 duration: float, 
                 weight: float, 
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    LEN_STEP = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029
    def get_spent_calories(self) -> float:
        return((self.CALORIES_MEAN_SPEED_MULTIPLIER 
                * self.weight 
                + (self.get_mean_speed()**2 / self.height)
                * self.CALORIES_MEAN_SPEED_SHIFT 
                * self.weight) * self.duration) 


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self, 
                 action: int, 
                 duration: float, 
                 weight: float, 
                 length_pool: float, 
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    LEN_STEP = 1.38
    FIGURE_OF_FORMULA_1: float = 1.1
    FIGURE_OF_FORMULA_2: float = 2
    M_IN_KM: float = 1000
    
    def get_mean_speed(self) -> float:
        return(self.length_pool * self.count_pool 
               / self.M_IN_KM / self.duration)
    
    def get_spent_calories(self) -> float:
        return((self.get_mean_speed() + 1.1) * 2 
               * self.weight * self.duration)
   


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout[workout_type](*data)
 
 
def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    #info_message = training.show_training_info()
   # info = info_message.get_message()
    #print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

