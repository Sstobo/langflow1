from typing import TYPE_CHECKING
from langflow.services.store.service import StoreService
from langflow.services.factory import ServiceFactory

if TYPE_CHECKING:
    from langflow.services.settings.service import SettingsService


class StoreServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(StoreService)

    def create(self, settings_service: "SettingsService"):
        return StoreService(settings_service)
