from typing import Optional

from data.place import departments


def get_department_name(department_number: int) -> str:
    return departments.get(department_number, "Undefined")


def get_department_id(department_name: str) -> Optional[int]:
    for number, name in departments.items():
        if name == department_name:
            return int(number)
    return 60
