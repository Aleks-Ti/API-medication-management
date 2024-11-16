from abc import abstractmethod
from collections import defaultdict
from typing import Any


class DependsFactory:
    """
    Фабрика по сборке зависимостей(доп параметров определенных в конструкторе __init__) к сервису других сервисов \
          или репозиториев (могут быть как и другие модули, вспомогательные функции, интерфейсы или структуры).<br>

    Params:
        authorised_mode (dict[str, Any]): Обязательный параметр authorised_mode.
            Нужно объявлять заранее, какие флаги существуют для вашей фабрики.
            Пример:
            ```
            def __init__(self, modes) -> None:
                super().__init__(modes, "metrics", "user")
            ...
            ```
        modes (tuple[str]): флаги для присоединения зависимостей к сервису.
            Пример:
            ```
            # получаем modes и инициализируем с ним экземпляр класса.
            factory = ContestFactory(modes)

            # далее передаем флаги в конструктор __init__ в классе потомке.
            class ContestFactory(DependsFactory):
                def __init__(self, modes) -> None:
                    super().__init__(modes, "metrics", "user")
            ...
            ```
    """

    def __init__(self, modes: tuple[str | None], *authorised_mode: str) -> None:
        self.authorised_mode: defaultdict = self.set_authorised_mode(*authorised_mode)
        self.modes: tuple[str | None] = modes
        self.validate()

    def validate(self) -> None:
        self.validate_authorised_mode()
        self.validate_modes_type_hint()
        self.validate_values_modes()

    def validate_modes_type_hint(self) -> None:
        if self.modes:
            if not isinstance(self.modes, tuple):
                raise ValueError(
                    f"Было передано {type(self.modes)}, когда ожидает кортеж строк >> tuple(str) | None\n"
                    "`mode` передаваемые поля, должны быть строкового типа.\n"
                    'Пример: `service = name_service("metrics", "user", ...))`\n'
                    "Пример в FastApi:\n"
                    '`service: ContestService: Annotated[ContestService, Depends(lambda: *_service("metrics", "user", ...))]`\n',  # noqa
                )

    def validate_values_modes(self) -> None:
        if self.modes:
            if not all(isinstance(mode, str) for mode in self.modes):
                raise ValueError(
                    "`mode` передаваемые поля, должны быть строкового типа.\n"
                    'Пример: `service = name_service("metrics", "user", ...))`\n'
                    "Пример в FastApi:\n"
                    '`service: ContestService: Annotated[ContestService, Depends(lambda: *_service("metrics", "user", ...))]`\n',  # noqa
                )
            for mode in self.modes:
                if mode not in self.authorised_mode:
                    raise ValueError(
                        f"mode >> {mode}, не объявлен в разрешенных значениях `authorised_mode`, если mode `{mode}` "
                        "является валидным флагом для фабрики зависимостей, просто объявите его в authorised_mode,"
                        f"либо устраните опечатку флага или не валидный флаг {mode}\n"
                        "Пример:\n"
                        "class ContestFactory(DependsFactory):\n"
                        "    def __init__(self, modes: tuple) -> None:\n"
                        '        super().__init__(modes, "metrics", "user")',
                    )

    def validate_authorised_mode(self) -> None:
        if not self.authorised_mode:
            raise ValueError(
                f"Error {self.__class__.__name__}\n"
                "Отсутствует флаги authorised_mode.\n"
                "Определите к authorised_mode ключи, в классе потомке.\n"
                "Пример:\n"
                "class ContestFactory(DependsFactory):\n"
                "    def __init__(self, modes: tuple) -> None:\n"
                '        super().__init__(modes, "metrics", "user")',
            )
        if not isinstance(self.authorised_mode, defaultdict):
            raise ValueError(
                f"Error {self.__class__.__name__}\n"
                f"Нельзя переопределять: `authorised_mode`, тогда как ожидалось authorised_mode: defaultdict\n"
                "`authorised_mode` должен быть  defaultdict со строковыми ключами и дефолтными значениями None.\n"
                "Пример:\n"
                "class ContestFactory(DependsFactory):\n"
                "    def __init__(self, modes: tuple) -> None:\n"
                '        super().__init__(modes, "metrics", "user")',
            )

    def set_authorised_mode(self, *args: str) -> defaultdict:
        default_dict = defaultdict(None)
        for flag in args:
            if not isinstance(flag, str):
                raise ValueError(
                    f"Error {self.__class__.__name__}\n"
                    f"Было передано для `authorised_mode({type(flag)})`,"
                    f' тогда как ожидалось authorised_mode("string", "string", ...)\n'
                    "Пример:\n"
                    "class ContestFactory(DependsFactory):\n"
                    "    def __init__(self, modes: tuple) -> None:\n"
                    '        super().__init__(modes, "metrics", "user")',
                )
            default_dict.setdefault(flag)
        return default_dict

    @abstractmethod
    def get_service(self) -> Any:
        """
        Для опционального добавления N количество сервисов или репозиториев,
        используйте паттерн декоратор через self.additional_services: list.<br>
        `self.additional_services` объявлен в наследуемом классе DependsFactory:
        ```
        def __init__(self, authorised_mode: set, modes: tuple[str] | None = None):
            ...
            self.additional_services: list = []
            ...
        ```

        Пример реализации:

        ```
        class ContestFactory(DependsFactory):
            def __init__(self, modes) -> None:
                super().__init__(modes, "metrics", "user")

            def get_service(self) -> ContestsService:
                if self.modes:
                    for mode in self.modes:
                        if mode == "metrics":
                            self.authorised_mode["metrics"] = main_metrics_service()
                        if mode == "user":
                            self.authorised_mode["user"] = UserRepository()

                contest_service = ContestsService(
                    contest_repo=ContestRepository(),
                    user_repo=self.authorised_mode["user"],
                    metrics_service=self.authorised_mode["metrics"]
                )
                return contest_service
        ```
        """
        raise NotImplementedError(
            f"Вы обязаны реализовать метод get_service в классе наследнике {self.__class__.__name__}",
        )
