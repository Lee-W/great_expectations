from typing import List, Optional
from pathlib import Path

import logging

from great_expectations.execution_engine import ExecutionEngine
from great_expectations.execution_environment.data_connector import InferredAssetFilePathDataConnector
from great_expectations.execution_environment.data_connector.util import (
    normalize_directory_path,
    get_filesystem_one_level_directory_glob_path_list,
)

logger = logging.getLogger(__name__)


# TODO: <Alex>Clean up order of arguments.</Alex>
class InferredAssetFilesystemDataConnector(InferredAssetFilePathDataConnector):
    def __init__(
        self,
        name: str,
        execution_environment_name: str,
        base_directory: str,
        default_regex: dict,
        glob_directive: str = "*",
        execution_engine: ExecutionEngine = None,
        sorters: list = None,
    ):
        logger.debug(f'Constructing InferredAssetFilesystemDataConnector "{name}".')

        super().__init__(
            name=name,
            execution_environment_name=execution_environment_name,
            execution_engine=execution_engine,
            default_regex=default_regex,
            sorters=sorters,
        )

        self._base_directory = base_directory
        self._glob_directive = glob_directive

    def _get_data_reference_list(self, data_asset_name: Optional[str] = None) -> List[str]:
        """List objects in the underlying data store to create a list of data_references.

        This method is used to refresh the cache.
        """
        path_list: List[str] = get_filesystem_one_level_directory_glob_path_list(
            base_directory_path=self.base_directory,
            glob_directive=self._glob_directive
        )
        return path_list

    def _get_full_file_path(self, path: str, data_asset_name: Optional[str] = None) -> str:
        return str(Path(self.base_directory).joinpath(path))

    @property
    def base_directory(self):
        return normalize_directory_path(
            dir_path=self._base_directory,
            root_directory_path=self.data_context_root_directory
        )
