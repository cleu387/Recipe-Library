from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import registry, relationship

from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.nutrition import Nutrition

from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.author import Author
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
    Column("category_id", ForeignKey("categories.id"))
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
        '_Recipe__author': relationship(Author, back_populates='_Author__recipes'),
        '_Recipe__nutrition': relationship(Nutrition, back_populates='_Nutrition__recipe'),
        '_Recipe__category': relationship(Category, back_populates='_Category__recipes')
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
        '_RecipeImage__position': recipe_images_table.c.position
    })

