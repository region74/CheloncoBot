from data.place import departments


def get_department_name(department_number: int) -> str:
    return departments.get(department_number, "Undefined")
