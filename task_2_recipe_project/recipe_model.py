import json
from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass, asdict


class RecipeType(Enum):
    """Типы рецептов"""
    APPETIZER = "закуска"
    SOUP = "суп"
    MAIN_DISH = "основное блюдо"
    DESSERT = "десерт"
    DRINK = "напиток"
    SAUCE = "соус"
    BAKERY = "выпечка"


class CuisineType(Enum):
    """Типы кухонь"""
    ITALIAN = "итальянская"
    FRENCH = "французская"
    UKRAINIAN = "украинская"
    RUSSIAN = "русская"
    JAPANESE = "японская"
    CHINESE = "китайская"
    MEXICAN = "мексиканская"
    GEORGIAN = "грузинская"
    AMERICAN = "американская"
    MEDITERRANEAN = "средиземноморская"


@dataclass
class Ingredient:
    """Ингредиент рецепта"""
    name: str
    quantity: str  # Например: "200 г", "1 шт", "по вкусу"
    optional: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Ingredient':
        return cls(**data)


@dataclass
class Recipe:
    """Модель рецепта"""
    name: str
    author: str
    recipe_type: RecipeType
    description: str
    ingredients: List[Ingredient]
    cuisine: CuisineType
    youtube_url: Optional[str] = None
    google_url: Optional[str] = None
    cooking_time: Optional[int] = None  # В минутах
    difficulty: Optional[str] = None  # Легкий, Средний, Сложный

    def to_dict(self) -> Dict:
        """Преобразует объект рецепта в словарь"""
        return {
            "name": self.name,
            "author": self.author,
            "recipe_type": self.recipe_type.value,
            "description": self.description,
            "ingredients": [ing.to_dict() for ing in self.ingredients],
            "cuisine": self.cuisine.value,
            "youtube_url": self.youtube_url,
            "google_url": self.google_url,
            "cooking_time": self.cooking_time,
            "difficulty": self.difficulty
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Recipe':
        """Создает объект рецепта из словаря"""
        return cls(
            name=data["name"],
            author=data["author"],
            recipe_type=RecipeType(data["recipe_type"]),
            description=data["description"],
            ingredients=[Ingredient.from_dict(ing) for ing in data["ingredients"]],
            cuisine=CuisineType(data["cuisine"]),
            youtube_url=data.get("youtube_url"),
            google_url=data.get("google_url"),
            cooking_time=data.get("cooking_time"),
            difficulty=data.get("difficulty")
        )

    def get_ingredients_text(self) -> str:
        """Возвращает текстовое представление ингредиентов"""
        ingredients_text = []
        for i, ingredient in enumerate(self.ingredients, 1):
            optional = " (по желанию)" if ingredient.optional else ""
            ingredients_text.append(f"{i}. {ingredient.name} - {ingredient.quantity}{optional}")
        return "\n".join(ingredients_text)

    def __str__(self) -> str:
        return (f"📖 {self.name}\n"
                f"👨‍🍳 Автор: {self.author}\n"
                f"🏷️ Тип: {self.recipe_type.value}\n"
                f"🌍 Кухня: {self.cuisine.value}\n"
                f"⏱️ Время готовки: {self.cooking_time or 'Не указано'} мин\n"
                f"⚡ Сложность: {self.difficulty or 'Не указана'}")


class RecipeModel:
    """Модель для работы с коллекцией рецептов"""

    def __init__(self, filename: str = "recipes_data.json"):
        self.filename = filename
        self.recipes: List[Recipe] = []
        self.load_from_file()

    def load_from_file(self) -> None:
        """Загружает рецепты из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.recipes = [Recipe.from_dict(recipe_data) for recipe_data in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.recipes = []

    def save_to_file(self) -> None:
        """Сохраняет рецепты в файл"""
        recipes_data = [recipe.to_dict() for recipe in self.recipes]
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(recipes_data, file, ensure_ascii=False, indent=2)

    def add_recipe(self, recipe: Recipe) -> bool:
        """Добавляет новый рецепт"""
        # Проверяем, нет ли рецепта с таким же названием и автором
        for existing_recipe in self.recipes:
            if (existing_recipe.name.lower() == recipe.name.lower() and
                    existing_recipe.author.lower() == recipe.author.lower()):
                return False

        self.recipes.append(recipe)
        self.save_to_file()
        return True

    def remove_recipe(self, index: int) -> Optional[Recipe]:
        """Удаляет рецепт по индексу"""
        if 0 <= index < len(self.recipes):
            removed_recipe = self.recipes.pop(index)
            self.save_to_file()
            return removed_recipe
        return None

    def update_recipe(self, index: int, recipe: Recipe) -> bool:
        """Обновляет рецепт по индексу"""
        if 0 <= index < len(self.recipes):
            self.recipes[index] = recipe
            self.save_to_file()
            return True
        return False

    def get_recipe_by_index(self, index: int) -> Optional[Recipe]:
        """Получает рецепт по индексу"""
        if 0 <= index < len(self.recipes):
            return self.recipes[index]
        return None

    def search_recipes(self, query: str) -> List[Recipe]:
        """Поиск рецептов по названию или ингредиентам"""
        query = query.lower()
        results = []

        for recipe in self.recipes:
            # Поиск по названию
            if query in recipe.name.lower():
                results.append(recipe)
                continue

            # Поиск по автору
            if query in recipe.author.lower():
                results.append(recipe)
                continue

            # Поиск по ингредиентам
            for ingredient in recipe.ingredients:
                if query in ingredient.name.lower():
                    results.append(recipe)
                    break

            # Поиск по описанию
            if query in recipe.description.lower():
                results.append(recipe)

        return results

    def filter_by_cuisine(self, cuisine: CuisineType) -> List[Recipe]:
        """Фильтрует рецепты по кухне"""
        return [recipe for recipe in self.recipes if recipe.cuisine == cuisine]

    def filter_by_type(self, recipe_type: RecipeType) -> List[Recipe]:
        """Фильтрует рецепты по типу"""
        return [recipe for recipe in self.recipes if recipe.recipe_type == recipe_type]

    def filter_by_author(self, author: str) -> List[Recipe]:
        """Фильтрует рецепты по автору"""
        author = author.lower()
        return [recipe for recipe in self.recipes if author in recipe.author.lower()]

    def filter_by_cooking_time(self, max_time: int) -> List[Recipe]:
        """Фильтрует рецепты по времени приготовления"""
        return [recipe for recipe in self.recipes
                if recipe.cooking_time and recipe.cooking_time <= max_time]

    def get_all_authors(self) -> List[str]:
        """Получает список всех авторов"""
        authors = set(recipe.author for recipe in self.recipes)
        return sorted(authors)

    def get_all_cuisines(self) -> List[str]:
        """Получает список всех кухонь"""
        cuisines = set(recipe.cuisine.value for recipe in self.recipes)
        return sorted(cuisines)

    def get_statistics(self) -> Dict:
        """Получает статистику по рецептам"""
        total_recipes = len(self.recipes)

        # Статистика по кухням
        cuisine_stats = {}
        for recipe in self.recipes:
            cuisine_name = recipe.cuisine.value
            cuisine_stats[cuisine_name] = cuisine_stats.get(cuisine_name, 0) + 1

        # Статистика по типам
        type_stats = {}
        for recipe in self.recipes:
            type_name = recipe.recipe_type.value
            type_stats[type_name] = type_stats.get(type_name, 0) + 1

        # Среднее время приготовления
        cooking_times = [recipe.cooking_time for recipe in self.recipes if recipe.cooking_time]
        avg_cooking_time = sum(cooking_times) / len(cooking_times) if cooking_times else 0

        return {
            "total_recipes": total_recipes,
            "cuisine_stats": cuisine_stats,
            "type_stats": type_stats,
            "avg_cooking_time": round(avg_cooking_time, 1),
            "unique_authors": len(set(recipe.author for recipe in self.recipes))
        }

    def get_total_count(self) -> int:
        """Возвращает общее количество рецептов"""
        return len(self.recipes)