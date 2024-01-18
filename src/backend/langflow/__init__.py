from importlib import metadata

from langflow.interface.custom.custom_component import CustomComponent

# Deactivate cache manager for now
# from langflow.services.cache import cache_service
from langflow.processing.load import load_flow_from_json

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = ["load_flow_from_json", "CustomComponent"]
