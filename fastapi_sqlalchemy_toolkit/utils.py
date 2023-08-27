from typing import Annotated, Any, Optional, Type

import pydantic
from fastapi import Query


class AllOptional(pydantic._internal._model_construction.ModelMetaclass):
    """
    Метакласс, который делает все поля модели Pydantic необязательными.
    Полезно для схем PATCH запросов.
    """

    def __new__(
        self, name: str, bases: tuple[type], namespaces: dict[str, Any], **kwargs
    ):
        annotations: dict = namespaces.get("__annotations__", {})

        for base in bases:
            for base_ in base.__mro__:
                if base_ is pydantic.BaseModel:
                    break

                annotations.update(base_.__annotations__)

        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = Optional[annotations[field]]

        namespaces["__annotations__"] = annotations

        return super().__new__(self, name, bases, namespaces, **kwargs)


# Утилиты для передачи нескольких значений для фильтрации в одном
# квери параметре через запятую
comma_list_query = Annotated[
    str | None, Query(description="Несколько значений можно передать через запятую")
]


def get_comma_list_values(query: str | None, type_: Type) -> list | None:
    """
    :param query: Значение квери параметра
    :param type_: Тип значений в списке
    """
    if query:
        return [type_(query_value) for query_value in query.split(",")]
    return None
