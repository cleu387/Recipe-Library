class Nutrition:
    def __init__(self, nutrition_id: int, calories: float, fat: float, saturated_fat: float, cholesterol: float, sodium: float, carbohydrates: float, fiber: float, sugar: float, protein: float):
        self.__nutrition_id = nutrition_id
        self.__calories = calories
        self.__fat = fat
        self.__saturated_fat = saturated_fat
        self.__cholesterol = cholesterol
        self.__sodium = sodium
        self.__carbohydrates = carbohydrates
        self.__fiber = fiber
        self.__sugar = sugar
        self.__protein = protein


    def __repr__(self):
        return f"Calories: {self.calories}, Fat: {self.fat}, Saturated fat: {self.saturated_fat}, Cholesterol: {self.cholesterol}, Sodium: {self.sodium}, Carbohydrates: {self.carbohydrates}, Fiber: {self.fiber}, Sugar: {self.sugar}, Protein: {self.protein}"

    def __eq__(self, other):
        if isinstance(other, Nutrition):
            return self.calories == other.calories and self.fat == other.fat and self.cholesterol == other.cholesterol and self.sodium == other.sodium and self.carbohydrates == other.carbohydrates and self.fiber == other.fiber and self.sugar == other.sugar and self.protein == other.protein
        return False

    def __lt__(self, other):
        if isinstance(other, Nutrition):
            return self.calories < other.calories
        return None

    @property
    def id(self) -> int:
        return self.__nutrition_id

    @property
    def calories(self) -> float:
        return self.__calories

    @calories.setter
    def calories(self, value: float):
        if value < 0:
            raise ValueError("Calories cannot be negative.")
        self.__calories = value

    @property
    def fat(self) -> float:
        return self.__fat

    @fat.setter
    def fat(self, value: float):
        if value < 0:
            raise ValueError("Fat cannot be negative.")
        self.__fat = value

    @property
    def saturated_fat(self):
        return self.__saturated_fat

    @saturated_fat.setter
    def saturated_fat(self, value: float):
        if value < 0:
            raise ValueError("Saturated fat cannot be negative.")
        self.__saturated_fat = value

    @property
    def cholesterol(self):
        return self.__cholesterol

    @cholesterol.setter
    def cholesterol(self, value: float):
        if value < 0:
            raise ValueError("Cholesterol cannot be negative.")
        self.__cholesterol = value

    @property
    def sodium(self):
        return self.__sodium

    @sodium.setter
    def sodium(self, value: float):
        if value < 0:
            raise ValueError("Sodium cannot be negative.")
        self.__sodium = value

    @property
    def carbohydrates(self):
        return self.__carbohydrates

    @carbohydrates.setter
    def carbohydrates(self, value: float):
        if value < 0:
            raise ValueError("Carbohydrates cannot be negative.")
        self.__carbohydrates = value

    @property
    def fiber(self):
        return self.__fiber

    @fiber.setter
    def fiber(self, value: float):
        if value < 0:
            raise ValueError("Fiber cannot be negative.")
        self.__fiber = value

    @property
    def sugar(self):
        return self.__sugar

    @sugar.setter
    def sugar(self, value: float):
        if value < 0:
            raise ValueError("Sugar cannot be negative.")
        self.__sugar = value

    @property
    def protein(self):
        return self.__protein

    @protein.setter
    def protein(self, value: float):
        if value < 0:
            raise ValueError("Protein cannot be negative.")
        self.__protein = value

