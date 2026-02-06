from shoes_model import ShoesModel
from shoes_controller import ShoesController
from shoes_view import ShoesView


def initialize_sample_data(model: ShoesModel):
    """Инициализирует тестовые данные"""
    from shoes_model import Shoe, ShoeType, ShoeCategory

    sample_shoes = [
        Shoe(ShoeType.MEN, ShoeCategory.SNEAKERS, "черный", 4999.99, "Nike", 42.5),
        Shoe(ShoeType.WOMEN, ShoeCategory.SHOES, "красный", 8999.99, "Gucci", 38.0),
        Shoe(ShoeType.MEN, ShoeCategory.BOOTS, "коричневый", 7999.99, "Timberland", 43.0),
        Shoe(ShoeType.WOMEN, ShoeCategory.SANDALS, "бежевый", 2999.99, "Zara", 37.5),
        Shoe(ShoeType.MEN, ShoeCategory.LOAFERS, "синий", 5999.99, "Geox", 44.0),
        Shoe(ShoeType.WOMEN, ShoeCategory.SLIPPERS, "розовый", 1999.99, "HomeWear", 36.0),
    ]

    # Очищаем текущие данные и добавляем тестовые
    model.shoes = sample_shoes
    model.save_to_file()


if __name__ == "__main__":
    # Инициализация компонентов MVC
    model = ShoesModel("shoes_data.json")
    controller = ShoesController(model)
    view = ShoesView(controller)

    # Инициализация тестовых данных (можно закомментировать после первого запуска)
    # initialize_sample_data(model)

    # Запуск приложения
    print("Загрузка данных об обуви...")
    print(f"Загружено {model.get_total_count()} пар обуви")

    # Запуск главного меню
    view.display_main_menu()
# main.py
from shoes_model import ShoesModel
from shoes_controller import ShoesController
from shoes_view import ShoesView


def initialize_sample_data(model: ShoesModel):
    """Инициализирует тестовые данные"""
    from shoes_model import Shoe, ShoeType, ShoeCategory

    sample_shoes = [
        Shoe(ShoeType.MEN, ShoeCategory.SNEAKERS, "черный", 4999.99, "Nike", 42.5),
        Shoe(ShoeType.WOMEN, ShoeCategory.SHOES, "красный", 8999.99, "Gucci", 38.0),
        Shoe(ShoeType.MEN, ShoeCategory.BOOTS, "коричневый", 7999.99, "Timberland", 43.0),
        Shoe(ShoeType.WOMEN, ShoeCategory.SANDALS, "бежевый", 2999.99, "Zara", 37.5),
        Shoe(ShoeType.MEN, ShoeCategory.LOAFERS, "синий", 5999.99, "Geox", 44.0),
        Shoe(ShoeType.WOMEN, ShoeCategory.SLIPPERS, "розовый", 1999.99, "HomeWear", 36.0),
    ]

    # Очищаем текущие данные и добавляем тестовые
    model.shoes = sample_shoes
    model.save_to_file()

if __name__ == "__main__":
    # Инициализация компонентов MVC
    model = ShoesModel("shoes_data.json")
    controller = ShoesController(model)
    view = ShoesView(controller)

    # Инициализация тестовых данных (можно закомментировать после первого запуска)
    # initialize_sample_data(model)

    # Запуск приложения
    print("Загрузка данных об обуви...")
    print(f"Загружено {model.get_total_count()} пар обуви")

    # Запуск главного меню
    view.display_main_menu()