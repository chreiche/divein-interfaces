from dataclasses import dataclass, field


@dataclass
class Employee:
    id: int
    name: str
    age: int


@dataclass
class EmployeeDB:
    db: list[Employee] = field(default_factory=list)
    index: int = 0

    def create(self, name: str, age: int) -> dict:
        self.index += 1
        self.db.append(Employee(self.index, name, age))

        res = {
            "id": self.index,
            "name": name,
            "age": age
        }

        return res

    def read(self, id: int) -> dict:
        for item in self.db:
            if item.id == id:
                return {
                    "id": item.id,
                    "name": item.name,
                    "age": item.age
                }

        return None

    def update(self, id: int, name: str, age: int) -> dict:
        for item in self.db:
            if item.id == id:
                item.name = name
                item.age = age
                return {
                    "id": item.id,
                    "name": item.name,
                    "age": item.age
                }
        return None

    def delete(self, id: int) -> dict:
        for item in self.db:
            if item.id == id:
                res = {
                    "id": item.id,
                    "name": item.name,
                    "age": item.age
                }

                self.db.remove(item)

                return res

        return None

    def get_all(self):
        res = {}
        for item in self.db:
            res[item.id] = {"name":item.name, "age":item.age}

        return res

