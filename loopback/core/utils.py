from typing import Optional, Type

from pydantic import BaseModel, create_model


def creating_model_with_optional_fields(model_name: str, base_model: Type[BaseModel]) -> Type[BaseModel]:
    result = create_model(
        model_name,
        **{field: (Optional[annotation], None) for field, annotation in base_model.__annotations__.items()}
    )
    return result