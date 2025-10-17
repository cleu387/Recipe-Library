from recipe.domainmodel.nutrition import Nutrition
from recipe.browse.services import calculate_health_rating

def test_very_healthy_recipe():
    nutrition = Nutrition(
        nutrition_id=1,
        calories=600,
        fat=15,
        saturated_fat=5,
        cholesterol=50,
        sodium=500,
        carbohydrates=70,
        fiber=20,
        sugar=20,
        protein=32
    )
    rating = calculate_health_rating(nutrition)
    assert rating == 5

def test_unhealthy_recipe():
    nutrition = Nutrition(
        nutrition_id=2,
        calories=999,
        fat=999,
        saturated_fat=999,
        cholesterol=999,
        sodium=999,
        carbohydrates=999,
        fiber=0,
        sugar=999,
        protein=0
    )
    rating = calculate_health_rating(nutrition)

    assert rating == 0

def test_average_recipe():
    nutrition = Nutrition(
        nutrition_id=3,
        calories=999,
        fat=16,
        saturated_fat=999,
        cholesterol=22,
        sodium=111,
        carbohydrates=70,
        fiber=0,
        sugar=11,
        protein=0
    )
    rating = calculate_health_rating(nutrition)
    assert rating == 3

def test_missing_nutrition():
    assert calculate_health_rating(None) is None