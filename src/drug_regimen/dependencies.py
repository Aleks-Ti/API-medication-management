from src.drug_regimen.repository import ManagerRepository, RegimenRepository
from src.drug_regimen.service import ManagerService, RegimenService
from src.settings.fabric_dependency import DependsFactory


def manager_service():
    return ManagerService(ManagerRepository())


class RegimenFactory(DependsFactory):
    def __init__(self, modes) -> None:
        super().__init__(modes, "manager")

    def get_service(self) -> RegimenService:
        if self.modes:
            for mode in self.modes:
                if mode == "manager":
                    self.authorised_mode["manager"] = ManagerRepository()

        contest_service = RegimenService(
            regimen_repository=RegimenRepository(),
            manager_repository=self.authorised_mode["manager"],
        )

        return contest_service


def regimen_service(*modes: str):
    factory = RegimenFactory(modes)
    return factory.get_service()
