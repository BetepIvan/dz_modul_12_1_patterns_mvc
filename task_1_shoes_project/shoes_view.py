from typing import List
from shoes_controller import ShoesController
from shoes_model import Shoe, ShoeType, ShoeCategory


class ShoesView:
    def __init__(self, controller: ShoesController):
        self.controller = controller
        self.current_user_role = "customer"  # По умолчанию пользователь - покупатель

    def set_user_role(self, role: str):
        """Устанавливает роль текущего пользователя"""
        valid_roles = ["admin", "manager", "customer"]
        if role in valid_roles:
            self.current_user_role = role
            print(f"Роль пользователя установлена: {role}")
        else:
            print(f"Неверная роль. Доступные роли: {', '.join(valid_roles)}")

    def display_welcome_message(self):
        """Отображает приветственное сообщение"""
        print("\n" + "=" * 50)
        print("СИСТЕМА УПРАВЛЕНИЯ КАТАЛОГОМ ОБУВИ")
        print("=" * 50)
        print(f"Текущая роль: {self.current_user_role}")

    def display_all_shoes(self):
        """Отображает весь каталог обуви"""
        print("\n" + "-" * 50)
        print("ВЕСЬ КАТАЛОГ ОБУВИ")
        print("-" * 50)

        success, result = self.controller.get_all_shoes(self.current_user_role)

        if not success:
            print(f"Ошибка: {result}")
            return

        shoes = result
        if not shoes:
            print("Каталог пуст")
            return

        for i, shoe in enumerate(shoes, 1):
            print(f"{i}. {shoe}")

    def display_add_shoe_form(self):
        """Отображает форму добавления новой обуви"""
        print("\n" + "-" * 50)
        print("ДОБАВЛЕНИЕ НОВОЙ ОБУВИ")
        print("-" * 50)

        try:
            print("Тип обуви:")
            for i, shoe_type in enumerate(ShoeType, 1):
                print(f"{i}. {shoe_type.value}")
            type_choice = int(input("Выберите тип (1-2): ")) - 1
            shoe_type = list(ShoeType)[type_choice]

            print("\nКатегория обуви:")
            for i, category in enumerate(ShoeCategory, 1):
                print(f"{i}. {category.value}")
            category_choice = int(input("Выберите категорию (1-6): ")) - 1
            category = list(ShoeCategory)[category_choice]

            color = input("Цвет: ")
            price = float(input("Цена (₽): "))
            manufacturer = input("Производитель: ")
            size = float(input("Размер: "))

            success, message = self.controller.add_shoe(
                shoe_type, category, color, price, manufacturer, size, self.current_user_role
            )

            if success:
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")

        except (ValueError, IndexError):
            print("✗ Ошибка ввода данных")

    def display_filter_options(self):
        """Отображает опции фильтрации"""
        print("\n" + "-" * 50)
        print("ФИЛЬТРАЦИЯ ОБУВИ")
        print("-" * 50)
        print("1. По типу (мужская/женская)")
        print("2. По категории (кроссовки, сапоги и т.д.)")
        print("3. По производителю")
        print("4. По цене (диапазон)")
        print("5. Назад")

        choice = input("Выберите опцию: ")

        if choice == "1":
            self.display_shoes_by_type()
        elif choice == "2":
            self.display_shoes_by_category()
        elif choice == "3":
            self.display_shoes_by_manufacturer()
        elif choice == "4":
            self.display_shoes_by_price_range()

    def display_shoes_by_type(self):
        """Отображает обувь по типу"""
        print("\nВыберите тип обуви:")
        for i, shoe_type in enumerate(ShoeType, 1):
            print(f"{i}. {shoe_type.value}")

        try:
            choice = int(input("Ваш выбор: ")) - 1
            shoe_type = list(ShoeType)[choice]
            shoes = self.controller.get_shoes_by_type(shoe_type)

            if shoes:
                print(f"\n{shoe_type.value} обувь:")
                for i, shoe in enumerate(shoes, 1):
                    print(f"{i}. {shoe}")
            else:
                print(f"{shoe_type.value} обуви нет в наличии")
        except (ValueError, IndexError):
            print("Неверный выбор")

    def display_shoes_by_category(self):
        """Отображает обувь по категории"""
        print("\nВыберите категорию:")
        for i, category in enumerate(ShoeCategory, 1):
            print(f"{i}. {category.value}")

        try:
            choice = int(input("Ваш выбор: ")) - 1
            category = list(ShoeCategory)[choice]
            shoes = self.controller.get_shoes_by_category(category)

            if shoes:
                print(f"\n{category.value}:")
                for i, shoe in enumerate(shoes, 1):
                    print(f"{i}. {shoe}")
            else:
                print(f"{category.value} нет в наличии")
        except (ValueError, IndexError):
            print("Неверный выбор")

    def display_shoes_by_manufacturer(self):
        """Отображает обувь по производителю"""
        manufacturer = input("\nВведите название производителя: ")
        shoes = self.controller.get_shoes_by_manufacturer(manufacturer)

        if shoes:
            print(f"\nОбувь производителя '{manufacturer}':")
            for i, shoe in enumerate(shoes, 1):
                print(f"{i}. {shoe}")
        else:
            print(f"Обуви производителя '{manufacturer}' нет в наличии")

    def display_shoes_by_price_range(self):
        """Отображает обувь по диапазону цен"""
        try:
            min_price = float(input("\nМинимальная цена (₽): "))
            max_price = float(input("Максимальная цена (₽): "))

            if min_price > max_price:
                min_price, max_price = max_price, min_price

            shoes = self.controller.get_shoes_in_price_range(min_price, max_price)

            if shoes:
                print(f"\nОбувь в диапазоне цен {min_price}₽ - {max_price}₽:")
                for i, shoe in enumerate(shoes, 1):
                    print(f"{i}. {shoe}")
            else:
                print(f"Обуви в диапазоне {min_price}₽ - {max_price}₽ нет в наличии")
        except ValueError:
            print("Неверный формат цены")

    def display_statistics(self):
        """Отображает статистику"""
        success, result = self.controller.get_statistics(self.current_user_role)

        if not success:
            print(f"Ошибка: {result}")
            return

        stats = result
        print("\n" + "-" * 50)
        print("СТАТИСТИКА КАТАЛОГА ОБУВИ")
        print("-" * 50)
        print(f"Всего пар обуви: {stats['total_count']}")
        print(f"Средняя цена: {stats['average_price']}₽")
        print(f"Мужской обуви: {stats['men_shoes_count']}")
        print(f"Женской обуви: {stats['women_shoes_count']}")

    def display_remove_shoe_form(self):
        """Отображает форму удаления обуви"""
        print("\n" + "-" * 50)
        print("УДАЛЕНИЕ ОБУВИ")
        print("-" * 50)

        success, result = self.controller.get_all_shoes(self.current_user_role)
        if not success:
            print(f"Ошибка: {result}")
            return

        shoes = result
        if not shoes:
            print("Каталог пуст")
            return

        for i, shoe in enumerate(shoes, 1):
            print(f"{i}. {shoe}")

        try:
            index = int(input("\nВведите номер обуви для удаления: ")) - 1
            success, message = self.controller.remove_shoe(index, self.current_user_role)
            print(message)
        except ValueError:
            print("Неверный номер")

    def display_shoe_details(self):
        """Отображает детали конкретной обуви"""
        try:
            index = int(input("\nВведите номер обуви для просмотра деталей: ")) - 1
            success, result = self.controller.get_shoe_details(index)

            if success:
                shoe = result
                print("\n" + "=" * 50)
                print("ДЕТАЛИ ОБУВИ")
                print("=" * 50)
                print(f"Тип: {shoe.shoe_type.value}")
                print(f"Категория: {shoe.category.value}")
                print(f"Цвет: {shoe.color}")
                print(f"Размер: {shoe.size}")
                print(f"Производитель: {shoe.manufacturer}")
                print(f"Цена: {shoe.price}₽")
                print("=" * 50)
            else:
                print(result)
        except ValueError:
            print("Неверный номер")

    def display_main_menu(self):
        """Отображает главное меню"""
        while True:
            self.display_welcome_message()

            print("\nГЛАВНОЕ МЕНЮ:")
            print("1. Просмотреть весь каталог")
            print("2. Фильтровать каталог")
            print("3. Просмотреть детали обуви")

            if self.current_user_role in ["admin", "manager"]:
                print("4. Добавить обувь")
                print("5. Просмотреть статистику")

            if self.current_user_role == "admin":
                print("6. Удалить обувь")

            print("7. Сменить роль пользователя")
            print("8. Выйти")

            choice = input("\nВыберите действие: ")

            if choice == "1":
                self.display_all_shoes()
            elif choice == "2":
                self.display_filter_options()
            elif choice == "3":
                self.display_shoe_details()
            elif choice == "4" and self.current_user_role in ["admin", "manager"]:
                self.display_add_shoe_form()
            elif choice == "5" and self.current_user_role in ["admin", "manager"]:
                self.display_statistics()
            elif choice == "6" and self.current_user_role == "admin":
                self.display_remove_shoe_form()
            elif choice == "7":
                print("\nДоступные роли:")
                print("1. admin - полный доступ")
                print("2. manager - добавление и просмотр")
                print("3. customer - только просмотр")
                role_choice = input("Выберите роль (1-3): ")
                roles_map = {"1": "admin", "2": "manager", "3": "customer"}
                if role_choice in roles_map:
                    self.set_user_role(roles_map[role_choice])
                else:
                    print("Неверный выбор")
            elif choice == "8":
                print("До свидания!")
                break
            else:
                print("Неверный выбор или недостаточно прав")

            input("\nНажмите Enter для продолжения...")