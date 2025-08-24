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

    def __hash__(self) -> int:
        return hash(self.__nutrition_id)

    @property
    def id(self) -> int:
        return self.__nutrition_id

    @property
    def calories(self) -> float:
        return self.__calories

    @property
    def fat(self) -> float:
        return self.__fat

    @property
    def saturated_fat(self):
        return self.__saturated_fat

    @property
    def cholesterol(self):
        return self.__cholesterol

    @property
    def sodium(self):
        return self.__sodium

    @property
    def carbohydrates(self):
        return self.__carbohydrates

    @property
    def fiber(self):
        return self.__fiber

    @property
    def sugar(self):
        return self.__sugar

    @property
    def protein(self):
        return self.__protein

