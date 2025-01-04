from unittest.mock import MagicMock, Mock

import pytest

from src.drug_regimen.repository import ManagerRepository, RegimenRepository
from src.drug_regimen.schemas import AddRegimenSchema, UpdateRegimenSchema
from src.drug_regimen.service import RegimenService
from src.utils.time_conversion import conversion_reception_time_to_GMT


@pytest.fixture
def regimen_service():
    regimen_repository = Mock(spec=RegimenRepository)
    manager_repository = Mock(spec=ManagerRepository)
    return RegimenService(regimen_repository, manager_repository)


def test_regimen_service_init(regimen_service):
    assert regimen_service.regimen_repository is not None
    assert regimen_service.manager_repository is not None
    assert regimen_service.conversion_time is conversion_reception_time_to_GMT


@pytest.mark.asyncio
async def test_add_one_complex(regimen_service):
    regimen_data = AddRegimenSchema(manager_id=1, reception_time="10:00", supplement="test", is_active=True)
    manager_obj = Mock()
    regimen_service.manager_repository.find_one.return_value = manager_obj
    regimen_service.regimen_repository.add_one.return_value = Mock()

    await regimen_service.add_one_complex(regimen_data)

    regimen_service.manager_repository.find_one.assert_called_once_with(regimen_data.manager_id)
    regimen_service.regimen_repository.add_one.assert_called_once()


@pytest.mark.asyncio
async def test_update_regmen(regimen_service):
    regimen_data = UpdateRegimenSchema(reception_time="11:00", supplement="test2", is_active=False)
    regimen_id = 1
    regimen_obj = Mock()
    regimen_service.regimen_repository.find_one_ON_manager.return_value = regimen_obj
    regimen_service.regimen_repository.update_one.return_value = Mock()

    await regimen_service.update_regmen(regimen_data, regimen_id)

    regimen_service.regimen_repository.find_one_ON_manager.assert_called_once_with(regimen_id)
    regimen_service.regimen_repository.update_one.assert_called_once_with(
        regimen_obj.id,
        regimen_data.model_dump(exclude_none=True),
    )
