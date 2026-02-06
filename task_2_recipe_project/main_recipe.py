from recipe_model import RecipeModel, Recipe, RecipeType, CuisineType, Ingredient
from recipe_controller import RecipeController
from recipe_view import RecipeView


def initialize_sample_recipes(model: RecipeModel):
    """Инициализирует тестовые рецепты"""

    # Рецепт 1: Борщ
    borscht_ingredients = [
        Ingredient("Свекла", "2 шт"),
        Ingredient("Картофель", "3 шт"),
        Ingredient("Капуста белокочанная", "200 г"),
        Ingredient("Морковь", "1 шт"),
        Ingredient("Лук репчатый", "1 шт"),
        Ingredient("Томатная паста", "2 ст. ложки"),
        Ingredient("Говядина", "400 г"),
        Ingredient("Сметана", "для подачи", optional=True),
        Ingredient("Укроп", "для подачи", optional=True)
    ]

    borscht = Recipe(
        name="Борщ украинский",
        author="Баба Галя",
        recipe_type=RecipeType.SOUP,
        description="Классический украинский борщ с говядиной. Готовится на мясном бульоне с добавлением свеклы, капусты и овощей. Подается со сметаной и свежей зеленью.",
        ingredients=borscht_ingredients,
        cuisine=CuisineType.UKRAINIAN,
        cooking_time=120,
        difficulty="Средний",
        youtube_url="https://youtube.com/watch?v=example_borscht"
    )

    # Рецепт 2: Паста Карбонара
    carbonara_ingredients = [
        Ingredient("Спагетти", "400 г"),
        Ingredient("Панчетта или грудинка", "200 г"),
        Ingredient("Яйца", "4 шт"),
        Ingredient("Пармезан", "100 г"),
        Ingredient("Черный перец", "по вкусу"),
        Ingredient("Соль", "по вкусу")
    ]

    carbonara = Recipe(
        name="Паста Карбонара",
        author="Шеф Марко",
        recipe_type=RecipeType.MAIN_DISH,
        description="Классическая итальянская паста с панчеттой, яйцами и пармезаном. Секрет в том, чтобы добавить яичную смесь в горячую пасту, не доводя до кипения.",
        ingredients=carbonara_ingredients,
        cuisine=CuisineType.ITALIAN,
        cooking_time=30,
        difficulty="Легкий",
        google_url="https://www.giallozafferano.it/ricerca-ricette/carbonara/"
    )

    # Рецепт 3: Тирамису
    tiramisu_ingredients = [
        Ingredient("Маскарпоне", "500 г"),
        Ingredient("Яйца", "4 шт"),
        Ingredient("Сахар", "100 г"),
        Ingredient("Печенье савоярди", "250 г"),
        Ingredient("Кофе эспрессо", "300 мл"),
        Ingredient("Какао-порошок", "для посыпки"),
        Ingredient("Марсала", "50 мл", optional=True)
    ]

    tiramisu = Recipe(
        name="Тирамису",
        author="Кондитер Анна",
        recipe_type=RecipeType.DESSERT,
        description="Знаменитый итальянский десерт из маскарпоне, савоярди и кофе. Легкий, воздушный, с нежным вкусом кофе и какао.",
        ingredients=tiramisu_ingredients,
        cuisine=CuisineType.ITALIAN,
        cooking_time=45,
        difficulty="Средний",
        youtube_url="https://youtube.com/watch?v=example_tiramisu"
    )

    # Рецепт 4: Суши Филадельфия
    philadelphia_ingredients = [
        Ingredient("Рис для суши", "300 г"),
        Ingredient("Нори", "5 листов"),
        Ingredient("Сыр Филадельфия", "200 г"),
        Ingredient("Лосось", "300 г"),
        Ingredient("Огурец", "1 шт"),
        Ingredient("Авокадо", "1 шт"),
        Ingredient("Рисовый уксус", "3 ст. ложки"),
        Ingredient("Сахар", "1 ст. ложка"),
        Ingredient("Соль", "1 ч. ложка"),
        Ingredient("Васаби", "по вкусу"),
        Ingredient("Имбирь маринованный", "для подачи")
    ]

    philadelphia = Recipe(
        name="Роллы Филадельфия",
        author="Суши-шеф Такеши",
        recipe_type=RecipeType.MAIN_DISH,
        description="Популярные роллы с лососем, сыром Филадельфия, огурцом и авокадо. Подаются с васаби, имбирем и соевым соусом.",
        ingredients=philadelphia_ingredients,
        cuisine=CuisineType.JAPANESE,
        cooking_time=60,
        difficulty="Сложный"
    )

    # Рецепт 5: Гуакамоле
    guacamole_ingredients = [
        Ingredient("Авокадо", "3 шт"),
        Ingredient("Лимонный сок", "2 ст. ложки"),
        Ingredient("Помидор", "1 шт"),
        Ingredient("Лук красный", "1/4 шт"),
        Ingredient("Кинза", "по вкусу"),
        Ingredient("Соль", "по вкусу"),
        Ingredient("Чили перец", "по вкусу", optional=True)
    ]

    guacamole = Recipe(
        name="Гуакамоле",
        author="Шеф Карлос",
        recipe_type=RecipeType.APPETIZER,
        description="Мексиканская закуска из авокадо с добавлением помидоров, лука и зелени. Подается с чипсами начос или тостадами.",
        ingredients=guacamole_ingredients,
        cuisine=CuisineType.MEXICAN,
        cooking_time=15,
        difficulty="Легкий",
        google_url="https://www.mexicoinmykitchen.com/guacamole-recipe/"
    )

    # Добавляем рецепты в модель
    sample_recipes = [borscht, carbonara, tiramisu, philadelphia, guacamole]

    # Очищаем текущие данные и добавляем тестовые
    model.recipes = sample_recipes
    model.save_to_file()


def main():
    """Точка входа в приложение"""
    print("=" * 60)
    print("🍽️  ЗАГРУЗКА КУЛИНАРНОЙ КНИГИ")
    print("=" * 60)

    # Инициализация MVC компонентов
    model = RecipeModel("recipes_data.json")
    controller = RecipeController(model)
    view = RecipeView(controller)

    # Инициализация тестовых данных (раскомментировать для первого запуска)
    # initialize_sample_recipes(model)

    print(f"📚 Загружено {model.get_total_count()} рецептов")

    # Установка роли по умолчанию
    view.set_user_role("admin")  # Для полного доступа при первом запуске

    # Запуск главного меню
    view.display_main_menu()


if __name__ == "__main__":
    main()