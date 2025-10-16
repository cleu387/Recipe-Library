from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import registry, relationship

from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.nutrition import Nutrition

from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.author import Author
from recipe.domainmodel.recipe_instruction import RecipeInstruction
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User
from recipe.domainmodel.recipe_ingredient import RecipeIngredient

# Global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()

# Author table
author_table = Table(
    "author", mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
)

# Recipes table
recipes_table = Table(
    'recipes', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('description', Text, nullable=False),
    Column('nutrition_id', Integer, ForeignKey('nutrition.id'), unique=True),
    Column("author_id", ForeignKey("author.id")),
    Column("category_id", ForeignKey("categories.id")),
    Column('rating', Float),
)

# Category table
categories_table = Table(
    'categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False),
)

# Nutrition table
nutrition_table = Table(
    'nutrition', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('calories', Float, nullable=False),
    Column('fat', Float, nullable=False),
    Column('saturated_fat', Float, nullable=False),
    Column('cholesterol', Float, nullable=False),
    Column('sodium', Float, nullable=False),
    Column('carbohydrates', Float, nullable=False),
    Column('fiber', Float, nullable=False),
    Column('sugar', Float, nullable=False),
    Column('protein', Float, nullable=False)
)

# Recipe images table
recipe_images_table = Table(
    'recipe_images', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), nullable=False),
    Column('url', String(500), nullable=False),
    Column('position', Integer, nullable=False)
)

# Recipe ingredient table
recipe_ingredients_table = Table(
    'recipe_ingredients', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), nullable=False),
    Column('quantity', String(255), nullable=False),
    Column('ingredient', String(255), nullable=False),
    Column('position', Integer, nullable=False)
)

# Recipe instruction table
recipe_instructions_table = Table(
    'recipe_instructions', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), nullable=False),
    Column('step', String(255), nullable=False),
    Column('position', Integer, nullable=False)
)

# Review table
review_table = Table(
    'review', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('rating', Float, nullable=False),
    Column('text', Text),
    Column('date', DateTime, nullable=False),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
)

# User table
user_table = Table(
    'user', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), nullable=False),
    Column('password', String(255), nullable=False),
)

# Favourite table
favourite_table = Table(
    'favourite', mapper_registry.metadata,
Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), nullable=False),
)



# ORM Mappings
def map_model_to_tables():

    # Author mapping
    mapper_registry.map_imperatively(Author, author_table, properties={
        '_Author__id': author_table.c.id,
        '_Author__name': author_table.c.name,
        '_Author__recipes': relationship(Recipe, back_populates="_Recipe__author")
    })

    # Recipe mapping
    mapper_registry.map_imperatively(Recipe, recipes_table, properties={
        '_Recipe__id': recipes_table.c.id,
        '_Recipe__name': recipes_table.c.name,
        '_Recipe__description': recipes_table.c.description,
        '_Recipe__nutrition': relationship(Nutrition, back_populates='_Nutrition__recipe'),
        '_Recipe__author': relationship(Author, back_populates='_Author__recipes'),
        '_Recipe__category': relationship(Category, back_populates='_Category__recipes', foreign_keys=[recipes_table.c.category_id]),
        '_Recipe__favourites': relationship(Favourite, back_populates='_Favourite__recipe'),
        '_Recipe__reviews': relationship(Review, back_populates='_Review__recipe'),
        '_Recipe__rating': recipes_table.c.rating,
    })

    # Category mapping
    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_Category__id': categories_table.c.id,
        '_Category__name': categories_table.c.name,
        '_Category__recipes': relationship(Recipe, back_populates='_Recipe__category')
    })

    # Nutrition mapping
    mapper_registry.map_imperatively(Nutrition, nutrition_table, properties={
        '_Nutrition__id': nutrition_table.c.id,
        '_Nutrition__calories': nutrition_table.c.calories,
        '_Nutrition__fat': nutrition_table.c.fat,
        '_Nutrition__saturated_fat': nutrition_table.c.saturated_fat,
        '_Nutrition__cholesterol': nutrition_table.c.cholesterol,
        '_Nutrition__sodium': nutrition_table.c.sodium,
        '_Nutrition__carbohydrates': nutrition_table.c.carbohydrates,
        '_Nutrition__fiber': nutrition_table.c.fiber,
        '_Nutrition__sugar': nutrition_table.c.sugar,
        '_Nutrition__protein': nutrition_table.c.protein,
        '_Nutrition__recipe': relationship(Recipe, back_populates='_Recipe__nutrition', uselist=False)
    })

    # RecipeImage mapping
    mapper_registry.map_imperatively(RecipeImage, recipe_images_table, properties={
        '_RecipeImage__id': recipe_images_table.c.id,
        '_RecipeImage__recipe_id': recipe_images_table.c.recipe_id,
        '_RecipeImage__url': recipe_images_table.c.url,
        '_RecipeImage__position': recipe_images_table.c.position,
    })

    # RecipeIngredient mapping
    mapper_registry.map_imperatively(RecipeIngredient, recipe_ingredients_table, properties={
        '_RecipeIngredient__id': recipe_ingredients_table.c.id,
        '_RecipeIngredient__recipe_id': recipe_ingredients_table.c.recipe_id,
        '_RecipeIngredient__quantity': recipe_ingredients_table.c.quantity,
        '_RecipeIngredient__ingredient': recipe_ingredients_table.c.ingredient,
        '_RecipeIngredient__position': recipe_ingredients_table.c.position
    })

    # RecipeInstruction mapping
    mapper_registry.map_imperatively(RecipeInstruction, recipe_instructions_table, properties={
        '_RecipeInstruction__id': recipe_instructions_table.c.id,
        '_RecipeInstruction__recipe_id': recipe_instructions_table.c.recipe_id,
        '_RecipeInstruction__step': recipe_instructions_table.c.step,
        '_RecipeInstruction__position': recipe_instructions_table.c.position,
    })

    # Review Mapping
    mapper_registry.map_imperatively(Review, review_table, properties={
        '_Review__id': review_table.c.id,
        '_Review__rating': review_table.c.rating,
        '_Review__text': review_table.c.text,
        '_Review__date': review_table.c.date,
        '_Review__user': relationship(User, back_populates='_User__reviews'),
        '_Review__recipe': relationship(Recipe, back_populates='_Recipe__reviews')
    })

    # User Mapping
    mapper_registry.map_imperatively(User, user_table, properties={
        '_User__id': user_table.c.id,
        '_User__username': user_table.c.username,
        '_User__password': user_table.c.password,
        '_User__reviews': relationship(Review, back_populates='_Review__user'),
        '_User__favourites': relationship(Favourite, back_populates='_Favourite__user'),
    })

    # Favourite Mapping
    mapper_registry.map_imperatively(Favourite, favourite_table, properties={
        '_Favourite__id': favourite_table.c.id,
        '_Favourite__user': relationship(User, back_populates='_User__favourites'),
        '_Favourite__recipe': relationship(Recipe, back_populates='_Recipe__favourites'),
    })

