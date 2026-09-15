from warehouse.domain.repositories.category_repository import CategoryRepository
from warehouse.domain.category import Category

class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self):
        self._categories = []
        self._next_id = 1

    def save(self, category: Category) -> Category:
        category._assign_id(self._next_id)

        self._categories.append(category)
        self._next_id += 1

        return category


    def find_by_id(self, category_id: int) -> Category | None:
        for category in self._categories:
            if category.id == category_id:
                return category

        return None