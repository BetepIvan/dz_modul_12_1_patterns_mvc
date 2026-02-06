from typing import List
from recipe_controller import RecipeController
from recipe_model import Recipe, RecipeType, CuisineType, Ingredient


class RecipeView:
    """Представление для взаимодействия с пользователем"""

    def __init__(self, controller: RecipeController):
        self.controller = controller
        self.current_user_role = "guest"

    def set_user_role(self, role: str):
        """Устанавливает роль текущего пользователя"""
        valid_roles = ["admin", "editor", "viewer", "guest"]
        if role in valid_roles:
            self.current_user_role = role
            print(f"✅ Роль пользователя установлена: {role}")
        else:
            print(f"❌ Неверная роль. Доступные роли: {', '.join(valid_roles)}")

    def display_welcome_message(self):
        """Отображает приветственное сообщение"""
        print("\n" + "=" * 60)
        print("📚 КУЛИНАРНАЯ КНИГА - Управление рецептами")
        print("=" * 60)
        print(f"👤 Текущая роль: {self.current_user_role}")

    # ========== Основные операции ==========

    def display_all_recipes(self):
        """Отображает все рецепты"""
        print("\n" + "-" * 60)
        print("📋 ВСЕ РЕЦЕПТЫ")
        print("-" * 60)

        success, result = self.controller.get_all_recipes(self.current_user_role)

        if not success:
            print(f"❌ Ошибка: {result}")
            return

        recipes = result
        if not recipes:
            print("📭 Рецептов пока нет. Добавьте первый рецепт!")
            return

        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe}")
            print()

    def display_recipe_details(self, index: int):
        """Отображает детальную информацию о рецепте"""
        success, result = self.controller.get_recipe_details(index - 1)  # Для пользователя индексы с 1

        if not success:
            print(f"❌ {result}")
            return

        recipe = result
        print("\n" + "=" * 60)
        print("📖 ПОДРОБНОСТИ РЕЦЕПТА")
        print("=" * 60)
        print(f"Название: {recipe.name}")
        print(f"Автор: {recipe.author}")
        print(f"Тип: {recipe.recipe_type.value}")
        print(f"Кухня: {recipe.cuisine.value}")

        if recipe.cooking_time:
            print(f"⏱️ Время приготовления: {recipe.cooking_time} минут")

        if recipe.difficulty:
            print(f"⚡ Сложность: {recipe.difficulty}")

        print(f"\n📝 Ингредиенты:")
        print(recipe.get_ingredients_text())

        print(f"\n📄 Описание:")
        print(recipe.description)

        if recipe.youtube_url:
            print(f"\n🎬 Видео рецепт: {recipe.youtube_url}")

        if recipe.google_url:
            print(f"🔗 Дополнительно: {recipe.google_url}")

        print("=" * 60)

    def display_add_recipe_form(self):
        """Отображает форму добавления нового рецепта"""
        print("\n" + "=" * 60)
        print("➕ ДОБАВЛЕНИЕ НОВОГО РЕЦЕПТА")
        print("=" * 60)

        try:
            # Основная информация
            name = input("Название рецепта: ").strip()
            author = input("Автор рецепта: ").strip()

            # Тип рецепта
            print("\nВыберите тип рецепта:")
            for i, recipe_type in enumerate(RecipeType, 1):
                print(f"{i}. {recipe_type.value}")
            type_choice = int(input("Ваш выбор (1-7): ")) - 1
            recipe_type = list(RecipeType)[type_choice]

            # Кухня
            print("\nВыберите кухню:")
            for i, cuisine in enumerate(CuisineType, 1):
                print(f"{i}. {cuisine.value}")
            cuisine_choice = int(input("Ваш выбор (1-10): ")) - 1
            cuisine = list(CuisineType)[cuisine_choice]

            # Время приготовления
            cooking_time_input = input("\nВремя приготовления (в минутах, Enter чтобы пропустить): ").strip()
            cooking_time = int(cooking_time_input) if cooking_time_input else None

            # Сложность
            if cooking_time:
                print("\nУровень сложности:")
                print("1. Легкий")
                print("2. Средний")
                print("3. Сложный")
                print("4. Пропустить")
                difficulty_choice = input("Ваш выбор (1-4): ").strip()
                difficulty_map = {"1": "Легкий", "2": "Средний", "3": "Сложный"}
                difficulty = difficulty_map.get(difficulty_choice)
            else:
                difficulty = None

            # Ингредиенты
            ingredients = []
            print("\n" + "-" * 30)
            print("ДОБАВЛЕНИЕ ИНГРЕДИЕНТОВ")
            print("(оставьте пустым для завершения)")
            print("-" * 30)

            while True:
                ing_name = input("\nНазвание ингредиента: ").strip()
                if not ing_name:
                    break

                ing_quantity = input("Количество (например: '200 г', '2 шт'): ").strip()
                optional = input("Ингредиент по желанию? (y/n): ").lower() == 'y'

                ingredients.append(Ingredient(name=ing_name, quantity=ing_quantity, optional=optional))
                print(f"✅ Ингредиент '{ing_name}' добавлен")

            if not ingredients:
                print("❌ Нужно добавить хотя бы один ингредиент!")
                return

            # Описание
            print("\n" + "-" * 30)
            print("ОПИСАНИЕ РЕЦЕПТА")
            print("(введите END на новой строке для завершения)")
            print("-" * 30)

            description_lines = []
            while True:
                line = input()
                if line.strip().upper() == "END":
                    break
                description_lines.append(line)

            description = "\n".join(description_lines)

            # Ссылки
            youtube_url = input("\nСсылка на YouTube (Enter чтобы пропустить): ").strip() or None
            google_url = input("Ссылка на Google/сайт (Enter чтобы пропустить): ").strip() or None

            # Добавление рецепта
            success, message = self.controller.add_recipe(
                name=name,
                author=author,
                recipe_type=recipe_type,
                description=description,
                ingredients=ingredients,
                cuisine=cuisine,
                youtube_url=youtube_url,
                google_url=google_url,
                cooking_time=cooking_time,
                difficulty=difficulty,
                user_role=self.current_user_role
            )

            if success:
                print(f"\n✅ {message}")
            else:
                print(f"\n❌ {message}")

        except (ValueError, IndexError) as e:
            print(f"❌ Ошибка ввода данных: {str(e)}")

    def display_search_recipes(self):
        """Отображает поиск рецептов"""
        print("\n" + "=" * 60)
        print("🔍 ПОИСК РЕЦЕПТОВ")
        print("=" * 60)

        query = input("Введите запрос для поиска (название, автор, ингредиент): ").strip()

        if not query:
            print("❌ Введите поисковый запрос")
            return

        recipes = self.controller.search_recipes(query)

        if recipes:
            print(f"\n✅ Найдено {len(recipes)} рецептов:")
            for i, recipe in enumerate(recipes, 1):
                print(f"{i}. {recipe.name} (автор: {recipe.author}, кухня: {recipe.cuisine.value})")
        else:
            print("❌ Рецепты по вашему запросу не найдены")

    def display_filter_menu(self):
        """Отображает меню фильтрации"""
        while True:
            print("\n" + "=" * 60)
            print("🎯 ФИЛЬТРАЦИЯ РЕЦЕПТОВ")
            print("=" * 60)
            print("1. По кухне")
            print("2. По типу блюда")
            print("3. По автору")
            print("4. По времени приготовления")
            print("5. Назад в главное меню")

            choice = input("\nВыберите вариант фильтрации (1-5): ").strip()

            if choice == "1":
                self.display_filter_by_cuisine()
            elif choice == "2":
                self.display_filter_by_type()
            elif choice == "3":
                self.display_filter_by_author()
            elif choice == "4":
                self.display_filter_by_cooking_time()
            elif choice == "5":
                break
            else:
                print("❌ Неверный выбор")

    def display_filter_by_cuisine(self):
        """Фильтрует рецепты по кухне"""
        cuisines = self.controller.get_all_cuisines()

        if not cuisines:
            print("❌ В базе нет рецептов")
            return

        print("\nДоступные кухни:")
        for i, cuisine_name in enumerate(cuisines, 1):
            print(f"{i}. {cuisine_name}")

        try:
            choice = int(input("Выберите кухню: ")) - 1
            if 0 <= choice < len(cuisines):
                # Находим соответствующий Enum
                cuisine_enum = None
                for cuisine in CuisineType:
                    if cuisine.value == cuisines[choice]:
                        cuisine_enum = cuisine
                        break

                if cuisine_enum:
                    recipes = self.controller.filter_by_cuisine(cuisine_enum)
                    self._display_filtered_recipes(recipes, f"кухня: {cuisines[choice]}")
                else:
                    print("❌ Ошибка при выборе кухни")
            else:
                print("❌ Неверный выбор")
        except ValueError:
            print("❌ Введите число")

    def display_filter_by_type(self):
        """Фильтрует рецепты по типу"""
        print("\nТипы рецептов:")
        for i, recipe_type in enumerate(RecipeType, 1):
            print(f"{i}. {recipe_type.value}")

        try:
            choice = int(input("Выберите тип: ")) - 1
            if 0 <= choice < len(RecipeType):
                recipe_type = list(RecipeType)[choice]
                recipes = self.controller.filter_by_type(recipe_type)
                self._display_filtered_recipes(recipes, f"тип: {recipe_type.value}")
            else:
                print("❌ Неверный выбор")
        except ValueError:
            print("❌ Введите число")

    def display_filter_by_author(self):
        """Фильтрует рецепты по автору"""
        authors = self.controller.get_all_authors()

        if not authors:
            print("❌ В базе нет рецептов")
            return

        print("\nДоступные авторы:")
        for i, author in enumerate(authors, 1):
            print(f"{i}. {author}")

        try:
            choice = int(input("Выберите автора: ")) - 1
            if 0 <= choice < len(authors):
                recipes = self.controller.filter_by_author(authors[choice])
                self._display_filtered_recipes(recipes, f"автор: {authors[choice]}")
            else:
                print("❌ Неверный выбор")
        except ValueError:
            print("❌ Введите число")

    def display_filter_by_cooking_time(self):
        """Фильтрует рецепты по времени приготовления"""
        try:
            max_time = int(input("\nМаксимальное время приготовления (в минутах): "))
            recipes = self.controller.filter_by_cooking_time(max_time)
            self._display_filtered_recipes(recipes, f"время до {max_time} минут")
        except ValueError:
            print("❌ Введите число")

    def _display_filtered_recipes(self, recipes: List[Recipe], filter_name: str):
        """Отображает отфильтрованные рецепты"""
        if recipes:
            print(f"\n✅ Найдено {len(recipes)} рецептов (фильтр: {filter_name}):")
            for i, recipe in enumerate(recipes, 1):
                print(f"{i}. {recipe.name} - {recipe.author}")
                if recipe.cooking_time:
                    print(f"   ⏱️ {recipe.cooking_time} мин")
                print()
        else:
            print(f"❌ Рецептов с фильтром '{filter_name}' не найдено")

    # ========== Управление рецептами ==========

    def display_remove_recipe(self):
        """Удаляет рецепт"""
        print("\n" + "=" * 60)
        print("🗑️ УДАЛЕНИЕ РЕЦЕПТА")
        print("=" * 60)

        success, result = self.controller.get_all_recipes(self.current_user_role)
        if not success:
            print(f"❌ {result}")
            return

        recipes = result
        if not recipes:
            print("❌ Рецептов для удаления нет")
            return

        print("Доступные рецепты:")
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe.name} - {recipe.author}")

        try:
            index = int(input("\nВведите номер рецепта для удаления: ")) - 1
            success, message = self.controller.remove_recipe(index, self.current_user_role)
            print(message)
        except ValueError:
            print("❌ Введите число")

    def display_statistics(self):
        """Отображает статистику"""
        success, result = self.controller.get_statistics(self.current_user_role)

        if not success:
            print(f"❌ {result}")
            return

        stats = result
        print("\n" + "=" * 60)
        print("📊 СТАТИСТИКА КУЛИНАРНОЙ КНИГИ")
        print("=" * 60)
        print(f"📚 Всего рецептов: {stats['total_recipes']}")
        print(f"👨‍🍳 Уникальных авторов: {stats['unique_authors']}")
        print(f"⏱️ Среднее время приготовления: {stats['avg_cooking_time']} мин")

        print(f"\n🌍 РАСПРЕДЕЛЕНИЕ ПО КУХНЯМ:")
        for cuisine, count in sorted(stats['cuisine_stats'].items()):
            print(f"  • {cuisine}: {count} рецептов")

        print(f"\n🍽️ РАСПРЕДЕЛЕНИЕ ПО ТИПАМ:")
        for recipe_type, count in sorted(stats['type_stats'].items()):
            print(f"  • {recipe_type}: {count} рецептов")

    def display_export_recipes(self):
        """Экспортирует рецепты в файл"""
        print("\n" + "=" * 60)
        print("💾 ЭКСПОРТ РЕЦЕПТОВ")
        print("=" * 60)

        filename = input("Введите имя файла для экспорта (например: recipes_export.txt): ").strip()

        if not filename.endswith('.txt'):
            filename += '.txt'

        success, message = self.controller.export_recipes_to_text(filename, self.current_user_role)
        print(message)

    # ========== Главное меню ==========

    def display_main_menu(self):
        """Отображает главное меню"""
        while True:
            self.display_welcome_message()

            print("\n🏠 ГЛАВНОЕ МЕНЮ:")
            print("1. 📋 Просмотреть все рецепты")
            print("2. 🔍 Поиск рецептов")
            print("3. 🎯 Фильтровать рецепты")
            print("4. 📖 Просмотреть детали рецепта")

            if self.current_user_role in ["admin", "editor"]:
                print("5. ➕ Добавить новый рецепт")
                print("6. 📊 Просмотреть статистику")

            if self.current_user_role == "admin":
                print("7. 🗑️ Удалить рецепт")
                print("8. 💾 Экспортировать рецепты")

            print("9. 👤 Сменить роль пользователя")
            print("0. 🚪 Выйти")

            choice = input("\n📝 Выберите действие: ").strip()

            if choice == "1":
                self.display_all_recipes()
            elif choice == "2":
                self.display_search_recipes()
            elif choice == "3":
                self.display_filter_menu()
            elif choice == "4":
                try:
                    index = int(input("Введите номер рецепта: "))
                    self.display_recipe_details(index)
                except ValueError:
                    print("❌ Введите число")
            elif choice == "5" and self.current_user_role in ["admin", "editor"]:
                self.display_add_recipe_form()
            elif choice == "6" and self.current_user_role in ["admin", "editor"]:
                self.display_statistics()
            elif choice == "7" and self.current_user_role == "admin":
                self.display_remove_recipe()
            elif choice == "8" and self.current_user_role == "admin":
                self.display_export_recipes()
            elif choice == "9":
                self._display_change_role()
            elif choice == "0":
                print("\n👋 До свидания! Приятного аппетита! 🍽️")
                break
            else:
                print("❌ Неверный выбор или недостаточно прав")

            input("\n⏎ Нажмите Enter для продолжения...")

    def _display_change_role(self):
        """Меняет роль пользователя"""
        print("\nДоступные роли:")
        print("1. admin - полный доступ (добавление, редактирование, удаление, экспорт)")
        print("2. editor - добавление и редактирование")
        print("3. viewer - только просмотр и поиск")
        print("4. guest - базовый просмотр")

        role_choice = input("Выберите роль (1-4): ").strip()
        roles_map = {"1": "admin", "2": "editor", "3": "viewer", "4": "guest"}

        if role_choice in roles_map:
            self.set_user_role(roles_map[role_choice])
        else:
            print("❌ Неверный выбор")