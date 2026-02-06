from typing import List, Optional, Tuple
from shoes_model import ShoesModel, Shoe, ShoeType, ShoeCategory


class ShoesController:
    USER_ROLES = {
        "admin": ["add", "remove", "view_all", "view_stats", "edit"],
        "manager": ["add", "view_all", "view_stats"],
        "customer": ["view_all", "filter"]
    }

    def __init__(self, model: ShoesModel):
        self.model = model

    def add_shoe(self, shoe_type: ShoeType, category: ShoeCategory, color: str,
                 price: float, manufacturer: str, size: float, user_role: str = "customer") -> Tuple[bool, str]:
        """Добавляет новую пару обуви"""
        if user_role not in ["admin", "manager"]:
            return False, "Доступ запрещен: недостаточно прав"

        try:
            shoe = Shoe(shoe_type, category, color, price, manufacturer, size)
            self.model.add_shoe(shoe)
            return True, "Обувь успешно добавлена"
        except ValueError as e:
            return False, f"Ошибка при добавлении: {str(e)}"

    def remove_shoe(self, index: int, user_role: str = "customer") -> Tuple[bool, str]:
        """Удаляет обувь по индексу"""
        if user_role != "admin":
            return False, "Доступ запрещен: только администратор может удалять"

        removed_shoe = self.model.remove_shoe(index)
        if removed_shoe:
            return True, f"Обувь удалена: {removed_shoe}"
        return False, "Обувь с таким индексом не найдена"

    def get_all_shoes(self, user_role: str = "customer") -> Tuple[bool, List[Shoe] | str]:
        """Получает весь список обуви"""
        if user_role not in self.USER_ROLES:
            return False, "Доступ запрещен: неизвестная роль"

        if "view_all" not in self.USER_ROLES[user_role]:
            return False, "Доступ запрещен: недостаточно прав"

        shoes = self.model.shoes
        if not shoes:
            return True, []
        return True, shoes

    def get_shoes_by_type(self, shoe_type: ShoeType) -> List[Shoe]:
        """Получает обувь по типу"""
        return self.model.get_shoes_by_type(shoe_type)

    def get_shoes_by_category(self, category: ShoeCategory) -> List[Shoe]:
        """Получает обувь по категории"""
        return self.model.get_shoes_by_category(category)

    def get_shoes_by_manufacturer(self, manufacturer: str) -> List[Shoe]:
        """Получает обувь по производителю"""
        return self.model.get_shoes_by_manufacturer(manufacturer)

    def get_shoes_in_price_range(self, min_price: float, max_price: float) -> List[Shoe]:
        """Получает обувь в диапазоне цен"""
        return self.model.get_shoes_in_price_range(min_price, max_price)

    def get_statistics(self, user_role: str = "customer") -> Tuple[bool, dict | str]:
        """Получает статистику по обуви"""
        if user_role not in ["admin", "manager"]:
            return False, "Доступ запрещен: недостаточно прав"

        stats = {
            "total_count": self.model.get_total_count(),
            "average_price": self.model.get_average_price(),
            "men_shoes_count": len(self.model.get_shoes_by_type(ShoeType.MEN)),
            "women_shoes_count": len(self.model.get_shoes_by_type(ShoeType.WOMEN))
        }
        return True, stats

    def get_shoe_details(self, index: int) -> Tuple[bool, Optional[Shoe] | str]:
        """Получает детали обуви по индексу"""
        shoe = self.model.get_shoe_at_index(index)
        if shoe:
            return True, shoe
        return False, "Обувь с таким индексом не найдена"