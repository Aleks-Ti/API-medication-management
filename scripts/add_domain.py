import re
import sys
from pathlib import Path

BASE_DIR_PROJECT: Path = Path(__file__).resolve().parent.parent


class NotDomainNameException(ValueError):
    pass


class MoreArgsException(Exception):
    pass


class ExistsDomenException(Exception):
    pass


class NotArgsException(ValueError):
    pass


file_names: list[str] = [
    "__init__.py",
    "dependencies.py",
    "models.py",
    "repository.py",
    "exceptions.py",
    "routers.py",
    "schemas.py",
    "service.py",
]


def generate_routers(name: str, path: Path) -> None:
    TitleName = name.title()
    with open(path / "routers.py", "w") as file:
        file.write(
            "import logging\n"
            "from typing import Annotated\n\n"
            "from fastapi import APIRouter, Depends, HTTPException\n\n"
            f"from src.{name}.dependencies import {name}_service as _{name}_service\n"
            f"from src.{name}.schemas import Create{TitleName}Schema, Update{TitleName}Schema, Get{TitleName}Schema, {TitleName}QueryParams\n"
            f"from src.{name}.service import {TitleName}Service\n\n"
            f"{name}_router = APIRouter(\n"
            f'    prefix="/{name}",\n'
            f'    tags=["{name} api"],\n'
            f'    responses={{404: {{"description": "Page not found"}}}}\n'
            ")\n\n\n"
            f'@{name}_router.get("", response_model=list[Get{TitleName}Schema])\n'
            f"async def get_{name}s(\n"
            f"    {name}_service: Annotated[{TitleName}Service, Depends(_{name}_service)],\n"
            f"    __query_params: {TitleName}QueryParams,\n"
            f") -> list[Get{TitleName}Schema]:\n"
            "    try:\n"
            f"        return await {name}_service.{name}_repository.find_all()\n"
            f"    except Exception as err:\n"
            f'        logging.exception(f"Error get a {name} - {{err}}")\n'
            f'        raise HTTPException(status_code=400, detail="Error get a {name}.")\n\n\n'
            f'@{name}_router.post("", response_model=Get{TitleName}Schema)\n'
            f"async def create_{name}(\n"
            f"    {name}_service: Annotated[{TitleName}Service, Depends(_{name}_service)],\n"
            f"    {name}_data: Create{TitleName}Schema,\n"
            f") -> Get{TitleName}Schema:\n"
            "    try:\n"
            f"        return await {name}_service.{name}_repository.add_one({name}_data.model_dump())\n"
            "    except Exception as err:\n"
            f'        logging.exception(f"Error create {name} - {{err}}")\n'
            f'        raise HTTPException(status_code=400, detail="Error create {name}.")\n\n\n'
            f'@{name}_router.put("/{name}_id", response_model=Get{TitleName}Schema)\n'
            f"async def update_{name}(\n"
            f"    {name}_id: int,\n"
            f"    {name}_service: Annotated[{TitleName}Service, Depends(_{name}_service)],\n"
            f"    {name}_data: Update{TitleName}Schema,\n"
            f") -> Get{TitleName}Schema:\n"
            "    try:\n"
            f"        return await {name}_service.{name}_repository.update_one({name}_id, {name}_data.model_dump({name}_id))\n"
            "    except Exception as err:\n"
            f'        logging.exception(f"Error update {name} - {{err}}")\n'
            f'        raise HTTPException(status_code=400, detail="Error update {name}.")\n\n\n'
            f'@{name}_router.get("/{name}_id", response_model=Get{TitleName}Schema)\n'
            f"async def get_{name}(\n"
            f"    {name}_id: int,\n"
            f"    {name}_service: Annotated[{TitleName}Service, Depends(_{name}_service)],\n"
            f") -> Get{TitleName}Schema:\n"
            "    try:\n"
            f"        return await {name}_service.{name}_repository.find_one({name}_id)\n"
            "    except Exception as err:\n"
            f'        logging.exception(f"Error get {name} by {{{name}_id}} - {{err}}")\n'
            f'        raise HTTPException(status_code=400, detail="Error get {name} by id.")\n\n\n'
            f'@{name}_router.delete("/{name}_id", response_model=dict)\n'
            f"async def delete_{name}(\n"
            f"    {name}_id: int,\n"
            f"    {name}_service: Annotated[{TitleName}Service, Depends(_{name}_service)],\n"
            f") -> Get{TitleName}Schema:\n"
            "    try:\n"
            f"        await {name}_service.{name}_repository.delete_one({name}_id)\n"
            f'        return {{"message": "{TitleName} deleted successfully"}}\n'
            "    except Exception as err:\n"
            f'        logging.exception(f"Error deleted {name} by {{{name}_id}} - {{err}}")\n'
            f'        raise HTTPException(status_code=400, detail="Error deleted {name} by id.")\n',
        )


def generate_schemas(name: str, path: Path) -> None:
    TitleName = name.title()
    with open(path / "schemas.py", "w") as file:
        file.write(
            "from src.settings.schemas import PreBase\n\n\n"
            f"class Get{TitleName}Schema(PreBase):\n"
            "    pass\n\n\n"
            f"class Create{TitleName}Schema(PreBase):\n"
            "    pass\n\n\n"
            f"class Update{TitleName}Schema(PreBase):\n"
            "    pass\n\n\n"
            f"class {TitleName}QueryParams(PreBase):\n"
            "    pass\n",
        )


def generate_model(name: str, path: Path) -> None:
    TitleName = name.title()
    with open(path / "models.py", "w") as file:
        file.write(
            "import sqlalchemy as sa\n"
            "from sqlalchemy.orm import Mapped, mapped_column\n\n"
            "from src.settings.base_model import Base\n\n\n"
            f"class {TitleName}(Base):\n"
            f'    __tablename__ = "{name}"\n\n'
            "    id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True, nullable=False, unique=True)\n",
        )


def generate_repository(name: str, path: Path) -> None:
    TitleName = name.title()
    with open(path / "repository.py", "w") as file:
        file.write(
            "from src.settings.database import async_session_maker\n"
            "from src.settings.repository import SQLAlchemyRepository\n"
            f"from src.{name}.models import {TitleName}\n\n\n"
            f"class {TitleName}Repository(SQLAlchemyRepository):\n"
            f"    model: type[{TitleName}] = {TitleName}\n",
        )


def generate_services(name: str, path: Path) -> None:
    TitleName = name.title()
    with open(path / "service.py", "w") as file:
        file.write(
            f"from src.settings.repository import AbstractRepository\n"
            f"from src.{name}.repository import {TitleName}Repository\n"
            f"from src.{name}.schemas import Create{TitleName}Schema, Update{TitleName}Schema, Get{TitleName}Schema, {TitleName}QueryParams\n\n\n"  # noqa
            f"class {TitleName}Service:\n"
            f"    def __init__(self, {name}_repository: AbstractRepository) -> None:\n"
            f"        self.{name}_repository: {TitleName}Repository = {name}_repository()\n",
        )


def generate_dependencies(name: str, path: Path):
    TitleName = name.title()
    with open(path / "dependencies.py", "w") as file:
        file.write(
            f"from src.{name}.repository import {TitleName}Repository\n"
            f"from src.{name}.service import {TitleName}Service\n\n\n"
            f"def {name}_service():\n"
            f"    return {TitleName}Service({TitleName}Repository)\n",
        )


def create_domen(name: str, path: Path) -> None:
    Path.mkdir(path)
    for file_name in file_names:
        Path.touch(path / file_name)


def main(name_domen) -> None:
    path = Path(BASE_DIR_PROJECT / "src" / name_domen)
    if path.exists():
        raise ExistsDomenException("Домен с таким именем уже существует.")
    else:
        create_domen(name_domen, path)
        generate_dependencies(name_domen, path)
        generate_repository(name_domen, path)
        generate_services(name_domen, path)
        generate_model(name_domen, path)
        generate_schemas(name_domen, path)
        generate_routers(name_domen, path)


if __name__ == "__main__":
    args: list[str] = sys.argv
    if len(args) <= 1:
        raise NotArgsException("You cannot call a script without arguments")
    if len(args) > 2:
        raise MoreArgsException("Script принимает только один аргумент >> --domain-name где name имя вашего домена.")
    for arg in sys.argv[1:]:
        pattern = r"--domain-[\x20-\x7E]+"
        if not re.match(pattern, arg):
            raise NotDomainNameException("Используй аргумент --domain-name где name имя вашего домена.")
    domain_name = args[-1].split("-")[-1]
    main(domain_name)
