from typing import List, Optional, Tuple, Dict
from recipe_model import RecipeModel, Recipe, RecipeType, CuisineType, Ingredient


class RecipeController:
    """Контроллер для управления рецептами"""

    USER_ROLES = {
        "admin": ["add", "edit", "delete", "view_all", "stats", "export"],
        "editor": ["add", "edit", "view_all", "stats"],
        "viewer": ["view_all", "search", "filter"],
        "guest": ["view_all", "search"]
    }

    def __init__(self, model: RecipeModel):
        self.model = model

    # ========== CRUD операции ==========

    def add_recipe(self, name: str, author: str, recipe_type: RecipeType,
                   description: str, ingredients: List[Ingredient],
                   cuisine: CuisineType, youtube_url: Optional[str] = None,
                   google_url: Optional[str] = None, cooking_time: Optional[int] = None,
                   difficulty: Optional[str] = None, user_role: str = "guest") -> Tuple[bool, str]:
        """Добавляет новый рецепт"""
        if user_role not in ["admin", "editor"]:
            return False, "Доступ запрещен: недостаточно прав для добавления рецептов"

        # Валидация данных
        if not name or not author or not description:
            return False, "Название, автор и описание обязательны"

        if not ingredients:
            return False, "Добавьте хотя бы один ингредиент"

        # Создаем рецепт
        recipe = Recipe(
            name=name,
            author=author,
            recipe_type=recipe_type,
            description=description,
            ingredients=ingredients,
            cuisine=cuisine,
            youtube_url=youtube_url,
            google_url=google_url,
            cooking_time=cooking_time,
            difficulty=difficulty
        )

        # Добавляем в модель
        if self.model.add_recipe(recipe):
            return True, f"Рецепт '{name}' успешно добавлен"
        else:
            return False, f"Рецепт с названием '{name}' от автора '{author}' уже существует"

    def remove_recipe(self, index: int, user_role: str = "guest") -> Tuple[bool, str]:
        """Удаляет рецепт по индексу"""
        if user_role != "admin":
            return False, "Доступ запрещен: только администратор может удалять рецепты"

        recipe = self.model.remove_recipe(index)
        if recipe:
            return True, f"Рецепт '{recipe.name}' удален"
        return False, "Рецепт с таким индексом не найден"

    def update_recipe(self, index: int, **kwargs) -> Tuple[bool, str]:
        """Обновляет рецепт"""
        recipe = self.model.get_recipe_by_index(index)
        if not recipe:
            return False, "Рецепт не найден"

        # Создаем новый объект рецепта с обновленными данными
        updated_data = recipe.to_dict()
        updated_data.update(kwargs)

        # Преобразуем строки обратно в Enum
        if 'recipe_type' in kwargs:
            updated_data['recipe_type'] = RecipeType(kwargs['recipe_type'])
        if 'cuisine' in kwargs:
            updated_data['cuisine'] = CuisineType(kwargs['cuisine'])
        if 'ingredients' in kwargs:
            from recipe_model import Ingredient
            updated_data['ingredients'] = [Ingredient(**ing) for ing in kwargs['ingredients']]

        updated_recipe = Recipe.from_dict(updated_data)

        if self.model.update_recipe(index, updated_recipe):
            return True, f"Рецепт '{updated_recipe.name}' обновлен"
        return False, "Ошибка при обновлении рецепта"

    # ========== Поиск и фильтрация ==========

    def get_all_recipes(self, user_role: str = "guest") -> Tuple[bool, List[Recipe] | str]:
        """Получает все рецепты"""
        if user_role not in self.USER_ROLES:
            return False, "Неизвестная роль пользователя"

        if "view_all" not in self.USER_ROLES[user_role]:
            return False, "Доступ запрещен: недостаточно прав"

        recipes = self.model.recipes
        return True, recipes

    def search_recipes(self, query: str) -> List[Recipe]:
        """Ищет рецепты по запросу"""
        return self.model.search_recipes(query)

    def filter_by_cuisine(self, cuisine: CuisineType) -> List[Recipe]:
        """Фильтрует рецепты по кухне"""
        return self.model.filter_by_cuisine(cuisine)

    def filter_by_type(self, recipe_type: RecipeType) -> List[Recipe]:
        """Фильтрует рецепты по типу"""
        return self.model.filter_by_type(recipe_type)

    def filter_by_author(self, author: str) -> List[Recipe]:
        """Фильтрует рецепты по автору"""
        return self.model.filter_by_author(author)

    def filter_by_cooking_time(self, max_time: int) -> List[Recipe]:
        """Фильтрует рецепты по времени приготовления"""
        return self.model.filter_by_cooking_time(max_time)

    def get_recipe_details(self, index: int) -> Tuple[bool, Recipe | str]:
        """Получает детальную информацию о рецепте"""
        recipe = self.model.get_recipe_by_index(index)
        if recipe:
            return True, recipe
        return False, "Рецепт не найден"

    # ========== Статистика и аналитика ==========

    def get_statistics(self, user_role: str = "guest") -> Tuple[bool, Dict | str]:
        """Получает статистику по рецептам"""
        if user_role not in ["admin", "editor"]:
            return False, "Доступ запрещен: недостаточно прав для просмотра статистики"

        stats = self.model.get_statistics()
        return True, stats

    def get_all_authors(self) -> List[str]:
        """Получает список всех авторов"""
        return self.model.get_all_authors()

    def get_all_cuisines(self) -> List[str]:
        """Получает список всех кухонь"""
        return self.model.get_all_cuisines()

    # ========== Экспорт данных ==========

    def export_recipes_to_text(self, filename: str, user_role: str = "guest") -> Tuple[bool, str]:
        """Экспортирует рецепты в текстовый файл"""
        if user_role != "admin":
            return False, "Доступ запрещен: только администратор может экспортировать данные"

        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("=" * 50 + "\n")
                file.write("КУЛИНАРНАЯ КНИГА\n")
                file.write("=" * 50 + "\n\n")

                for i, recipe in enumerate(self.model.recipes, 1):
                    file.write(f"РЕЦЕПТ #{i}\n")
                    file.write(f"{'=' * 30}\n")
                    file.write(f"Название: {recipe.name}\n")
                    file.write(f"Автор: {recipe.author}\n")
                    file.write(f"Тип: {recipe.recipe_type.value}\n")
                    file.write(f"Кухня: {recipe.cuisine.value}\n")

                    if recipe.cooking_time:
                        file.write(f"Время готовки: {recipe.cooking_time} мин\n")

                    if recipe.difficulty:
                        file.write(f"Сложность: {recipe.difficulty}\n")

                    file.write(f"\nИНГРЕДИЕНТЫ:\n")
                    for ingredient in recipe.ingredients:
                        optional = " (по желанию)" if ingredient.optional else ""
                        file.write(f"- {ingredient.name} - {ingredient.quantity}{optional}\n")

                    file.write(f"\nОПИСАНИЕ:\n{recipe.description}\n")

                    if recipe.youtube_url:
                        file.write(f"\nВидео рецепт: {recipe.youtube_url}\n")

                    if recipe.google_url:
                        file.write(f"Дополнительно: {recipe.google_url}\n")

                    file.write("\n" + "=" * 50 + "\n\n")

            return True, f"Рецепты успешно экспортированы в файл '{filename}'"

        except Exception as e:
            return False, f"Ошибка при экспорте: {str(e)}"