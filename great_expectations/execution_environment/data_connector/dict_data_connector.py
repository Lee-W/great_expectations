from pathlib import Path
import itertools
from typing import List, Union, Any

import logging

from great_expectations.execution_engine import ExecutionEngine
from great_expectations.execution_environment.data_connector.partitioner.partitioner import Partitioner
from great_expectations.execution_environment.data_connector.partitioner.partition_query import PartitionQuery
from great_expectations.execution_environment.data_connector.partitioner.partition import Partition
from great_expectations.execution_environment.data_connector.data_connector import DataConnector
from great_expectations.core.batch import BatchRequest
from great_expectations.core.id_dict import (
    PartitionDefinitionSubset,
    BatchSpec
)
from great_expectations.core.batch import (
    BatchMarkers,
    BatchDefinition,
)
from great_expectations.execution_environment.types import PathBatchSpec
import great_expectations.exceptions as ge_exceptions

logger = logging.getLogger(__name__)

class DictDataConnector(DataConnector):
    """This DataConnector is meant to closely mimic the FilesDataConnector, but without requiring an actual filesystem.

    Instead, its data_references are stored in a data_reference_dictionary : {
        "pretend/path/A-100.csv" : pandas_df_A_100,
        "pretend/path/A-101.csv" : pandas_df_A_101,
        "pretend/directory/B-1.csv" : pandas_df_B_1,
        "pretend/directory/B-2.csv" : pandas_df_B_2,
        ...
    }
    """
    def __init__(
        self,
        name: str,
        data_reference_dict: {},
        partitioners: dict = {},
        default_partitioner: str = None,
        assets: dict = None,
        execution_engine: ExecutionEngine = None,
    ):
        logger.debug(f'Constructing DictDataConnector "{name}".')
        super().__init__(
            name=name,
            partitioners=partitioners,
            default_partitioner=default_partitioner,
            assets=assets,
            execution_engine=execution_engine,
        )

        # This simulates the underlying filesystem
        self.data_reference_dict = data_reference_dict

        self._cached_data_reference_to_batch_definition_map = None

    def _get_data_reference_list(self):
        data_reference_keys = list(self.data_reference_dict.keys())
        data_reference_keys.sort()
        return data_reference_keys

    def _map_data_reference_to_batch_request_list(self, data_reference) -> List[BatchDefinition]:
        # Verify that a default_partitioner has been chosen
        try:
            self.default_partitioner
        except ValueError:
            #If not, return None
            return

        partition = self.default_partitioner._find_partitions_for_path(data_reference)
        return BatchRequest(
            execution_environment="FAKE_EXECUTION_ENVIRONMENT_NAME",
            data_connector=self.name,
            data_asset_name="FAKE_DATA_ASSET_NAME",
            partition_request=partition.definition,
        )
