import json
from typing import List, Dict, Optional
from enum import Enum

class ShoeType(Enum):
    MEN = "мужская"
    WOMEN = "женская"


class ShoeCategory(Enum):
    SNEAKERS = "кроссовки"
    BOOTS = "сапоги"
    SANDALS = "сандалии"
    SHOES = "туфли"
    SLIPPERS = "тапочки"
    LOAFERS = "лодочки"


class Shoe:
    def __init__(self, shoe_type: ShoeType, category: ShoeCategory, color: str,
                 price: float, manufacturer: str, size: float):
        self.shoe_type = shoe_type
        self.category = category
        self.color = color
        self.price = price
        self.manufacturer = manufacturer
        self.size = size

    def to_dict(self) -> Dict:
        """Преобразует объект обуви в словарь"""
        return {
            "shoe_type": self.shoe_type.value,
            "category": self.category.value,
            "color": self.color,
            "price": self.price,
            "manufacturer": self.manufacturer,
            "size": self.size
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Shoe':
        """Создает объект обуви из словаря"""
        return cls(
            shoe_type=ShoeType(data["shoe_type"]),
            category=ShoeCategory(data["category"]),
            color=data["color"],
            price=data["price"],
            manufacturer=data["manufacturer"],
            size=data["size"]
        )

    def __str__(self) -> str:
        return (f"{self.shoe_type.value} {self.category.value}, "
                f"цвет: {self.color}, размер: {self.size}, "
                f"производитель: {self.manufacturer}, цена: {self.price}₽")


class ShoesModel:
    def __init__(self, filename: str = "shoes_data.json"):
        self.filename = filename
        self.shoes: List[Shoe] = []
        self.load_from_file()

    def load_from_file(self) -> None:
        """Загружает данные об обуви из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for shoe_data in data:
                    self.shoes.append(Shoe.from_dict(shoe_data))
        except (FileNotFoundError, json.JSONDecodeError):
            self.shoes = []

    def save_to_file(self) -> None:
        """Сохраняет данные об обуви в файл"""
        shoes_data = [shoe.to_dict() for shoe in self.shoes]
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(shoes_data, file, ensure_ascii=False, indent=4)

    def add_shoe(self, shoe: Shoe) -> None:
        """Добавляет новую пару обуви"""
        self.shoes.append(shoe)
        self.save_to_file()

    def remove_shoe(self, index: int) -> Optional[Shoe]:
        """Удаляет обувь по индексу"""
        if 0 <= index < len(self.shoes):
            removed_shoe = self.shoes.pop(index)
            self.save_to_file()
            return removed_shoe
        return None

    def get_shoes_by_type(self, shoe_type: ShoeType) -> List[Shoe]:
        """Получает обувь по типу"""
        return [shoe for shoe in self.shoes if shoe.shoe_type == shoe_type]

    def get_shoes_by_category(self, category: ShoeCategory) -> List[Shoe]:
        """Получает обувь по категории"""
        return [shoe for shoe in self.shoes if shoe.category == category]

    def get_shoes_by_manufacturer(self, manufacturer: str) -> List[Shoe]:
        """Получает обувь по производителю"""
        return [shoe for shoe in self.shoes if shoe.manufacturer.lower() == manufacturer.lower()]

    def get_shoes_in_price_range(self, min_price: float, max_price: float) -> List[Shoe]:
        """Получает обувь в диапазоне цен"""
        return [shoe for shoe in self.shoes if min_price <= shoe.price <= max_price]

    def get_average_price(self) -> float:
        """Вычисляет среднюю цену обуви"""
        if not self.shoes:
            return 0.0
        total_price = sum(shoe.price for shoe in self.shoes)
        return round(total_price / len(self.shoes), 2)

    def get_total_count(self) -> int:
        """Получает общее количество пар обуви"""
        return len(self.shoes)

    def get_shoe_at_index(self, index: int) -> Optional[Shoe]:
        """Получает обувь по индексу"""
        if 0 <= index < len(self.shoes):
            return self.shoes[index]
        return None