from recipe.domainmodel.nutrition import Nutrition
from recipe.browse.services import calculate_health_rating

def test_very_healthy_recipe():
    nutrition = Nutrition(
        nutrition_id=1,
        calories=300,
        fat=10,
        saturated_fat=2,
        cholesterol=50,
        sodium=300,
        carbohydrates=40,
        fiber=6,
        sugar=10,
        protein=12
    )
    rating = calculate_health_rating(nutrition)
    assert rating == 5

def test_unhealthy_recipe():
    nutrition = Nutrition(
        nutrition_id=2,
        calories=600,
        fat=25,
        saturated_fat=6,
        cholesterol=150,
        sodium=800,
        carbohydrates=70,
        fiber=2,
        sugar=30,
        protein=5
    )
    rating = calculate_health_rating(nutrition)

    assert rating == 0

def test_average_recipe():
    nutrition = Nutrition(
        nutrition_id=3,
        calories=450,
        fat=18,
        saturated_fat=4,
        cholesterol=90,
        sodium=550,
        carbohydrates=55,
        fiber=5,
        sugar=20,
        protein=10
    )
    rating = calculate_health_rating(nutrition)
    assert rating == 5

def test_missing_nutrition():
    assert calculate_health_rating(None) is None
