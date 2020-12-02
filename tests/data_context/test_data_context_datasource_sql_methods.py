import json
from typing import List, Union

import pytest
from ruamel.yaml import YAML

from great_expectations.core.batch import Batch, BatchRequest, PartitionRequest
from great_expectations.datasource.new_datasource import Datasource
from great_expectations.exceptions.exceptions import DataContextError
from great_expectations.execution_engine.sqlalchemy_execution_engine import (
    SqlAlchemyBatchData,
)
from great_expectations.marshmallow__shade.exceptions import ValidationError

yaml = YAML()


def test_get_batch(data_context_with_sql_datasource_for_testing_get_batch):
    context = data_context_with_sql_datasource_for_testing_get_batch

    print(
        json.dumps(
            context.datasources["my_sqlite_db"].get_available_data_asset_names(),
            indent=4,
        )
    )

    # Successful specification using a typed BatchRequest
    context.get_batch(
        batch_request=BatchRequest(
            datasource_name="my_sqlite_db",
            data_connector_name="daily",
            data_asset_name="table_partitioned_by_date_column__A",
            partition_request=PartitionRequest(
                partition_identifiers={"date": "2020-01-15"}
            ),
        )
    )

    # Failed specification using an untyped BatchRequest
    with pytest.raises(TypeError):
        context.get_batch(
            batch_request={
                "datasource_name": "my_sqlite_db",
                "data_connector_name": "daily",
                "data_asset_name": "table_partitioned_by_date_column__A",
                "partition_request": {"partition_identifiers": {"date": "2020-01-15"}},
            }
        )

    # Failed specification using an incomplete BatchRequest
    with pytest.raises(ValueError):
        context.get_batch(
            batch_request=BatchRequest(
                datasource_name="my_sqlite_db",
                data_connector_name="daily",
                data_asset_name="table_partitioned_by_date_column__A",
                partition_request=PartitionRequest(partition_identifiers={}),
            )
        )

    # Failed specification using an incomplete BatchRequest
    with pytest.raises(ValueError):
        context.get_batch(
            batch_request=BatchRequest(
                datasource_name="my_sqlite_db",
                data_connector_name="daily",
                data_asset_name="table_partitioned_by_date_column__A",
            )
        )

    # Failed specification using an incomplete BatchRequest
    with pytest.raises(KeyError):
        context.get_batch(
            batch_request=BatchRequest(
                datasource_name="my_sqlite_db", data_connector_name="daily",
            )
        )

    # Failed specification using an incomplete BatchRequest
    # with pytest.raises(ValueError):
    with pytest.raises(KeyError):
        context.get_batch(
            batch_request=BatchRequest(
                # datasource_name=MISSING
                data_connector_name="daily",
                data_asset_name="table_partitioned_by_date_column__A",
                partition_request=PartitionRequest(partition_identifiers={}),
            )
        )

    # Successful specification using parameters
    context.get_batch(
        datasource_name="my_sqlite_db",
        data_connector_name="daily",
        data_asset_name="table_partitioned_by_date_column__A",
        date="2020-01-15",
    )

    # Successful specification using parameters without parameter names for the identifying triple
    # This is the thinnest this can plausibly get.
    context.get_batch(
        "my_sqlite_db",
        "daily",
        "table_partitioned_by_date_column__A",
        date="2020-01-15",
    )

    # Successful specification using parameters without parameter names for the identifying triple
    # In the case of a data_asset containing a single Batch, we don't even need parameters
    context.get_batch(
        "my_sqlite_db", "whole_table", "table_partitioned_by_date_column__A",
    )

    # Successful specification using parameters and partition_request
    context.get_batch(
        "my_sqlite_db",
        "daily",
        "table_partitioned_by_date_column__A",
        partition_request=PartitionRequest(
            {"partition_identifiers": {"date": "2020-01-15"}}
        ),
    )

    # Successful specification using parameters and partition_identifiers
    context.get_batch(
        "my_sqlite_db",
        "daily",
        "table_partitioned_by_date_column__A",
        partition_identifiers={"date": "2020-01-15"},
    )


def test_get_validator(data_context_with_sql_datasource_for_testing_get_batch):
    context = data_context_with_sql_datasource_for_testing_get_batch
    context.create_expectation_suite("my_expectations")

    print(
        json.dumps(
            context.datasources["my_sqlite_db"].get_available_data_asset_names(),
            indent=4,
        )
    )

    # Successful specification using a typed BatchRequest
    context.get_validator(
        batch_request=BatchRequest(
            datasource_name="my_sqlite_db",
            data_connector_name="daily",
            data_asset_name="table_partitioned_by_date_column__A",
            partition_request=PartitionRequest(
                partition_identifiers={"date": "2020-01-15"}
            ),
        ),
        expectation_suite_name="my_expectations",
    )

    # Failed specification using an untyped BatchRequest
    with pytest.raises(TypeError):
        context.get_validator(
            batch_request={
                "datasource_name": "my_sqlite_db",
                "data_connector_name": "daily",
                "data_asset_name": "table_partitioned_by_date_column__A",
                "partition_request": {"partition_identifiers": {"date": "2020-01-15"}},
            },
            expectation_suite_name="my_expectations",
        )

    # Failed specification using an incomplete BatchRequest
    with pytest.raises(ValueError):
        context.get_validator(
            batch_request=BatchRequest(
                datasource_name="my_sqlite_db",
                data_connector_name="daily",
                data_asset_name="table_partitioned_by_date_column__A",
                partition_request=PartitionRequest(partition_identifiers={}),
            ),
            expectation_suite_name="my_expectations",
        )

    # Failed specification using an incomplete BatchRequest
    with pytest.raises(ValueError):
        context.get_validator(
            batch_request=BatchRequest(
                datasource_name="my_sqlite_db",
                data_connector_name="daily",
                data_asset_name="table_partitioned_by_date_column__A",
            ),
            expectation_suite_name="my_expectations",
        )

    # Failed specification using an incomplete BatchRequest
    with pytest.raises(KeyError):
        context.get_validator(
            batch_request=BatchRequest(
                datasource_name="my_sqlite_db", data_connector_name="daily",
            ),
            expectation_suite_name="my_expectations",
        )

    # Failed specification using an incomplete BatchRequest
    # with pytest.raises(ValueError):
    with pytest.raises(KeyError):
        context.get_validator(
            batch_request=BatchRequest(
                # datasource_name=MISSING
                data_connector_name="daily",
                data_asset_name="table_partitioned_by_date_column__A",
                partition_request=PartitionRequest(partition_identifiers={}),
            ),
            expectation_suite_name="my_expectations",
        )

    # Successful specification using parameters
    context.get_validator(
        datasource_name="my_sqlite_db",
        data_connector_name="daily",
        data_asset_name="table_partitioned_by_date_column__A",
        date="2020-01-15",
        expectation_suite_name="my_expectations",
    )

    # Successful specification using parameters without parameter names for the identifying triple
    # This is the thinnest this can plausibly get.
    context.get_validator(
        "my_sqlite_db",
        "daily",
        "table_partitioned_by_date_column__A",
        date="2020-01-15",
        expectation_suite_name="my_expectations",
    )

    # Successful specification using parameters without parameter names for the identifying triple
    # In the case of a data_asset containing a single Batch, we don't even need parameters
    context.get_validator(
        "my_sqlite_db",
        "whole_table",
        "table_partitioned_by_date_column__A",
        expectation_suite_name="my_expectations",
    )

    # Successful specification using parameters and partition_request
    context.get_validator(
        "my_sqlite_db",
        "daily",
        "table_partitioned_by_date_column__A",
        partition_request=PartitionRequest(
            {"partition_identifiers": {"date": "2020-01-15"}}
        ),
        expectation_suite_name="my_expectations",
    )

    # Successful specification using parameters and partition_identifiers
    context.get_validator(
        "my_sqlite_db",
        "daily",
        "table_partitioned_by_date_column__A",
        partition_identifiers={"date": "2020-01-15"},
        expectation_suite_name="my_expectations",
    )


def test_get_validator_expectation_suite_options(
    data_context_with_sql_datasource_for_testing_get_batch,
):
    context = data_context_with_sql_datasource_for_testing_get_batch
    context.create_expectation_suite("some_expectations")

    # Successful specification with an existing expectation_suite_name
    context.get_validator(
        datasource_name="my_sqlite_db",
        data_connector_name="daily",
        data_asset_name="table_partitioned_by_date_column__A",
        date="2020-01-15",
        expectation_suite_name="some_expectations",
    )

    # Successful specification with a fetched ExpectationSuite object
    some_expectations = context.get_expectation_suite("some_expectations")
    context.get_validator(
        datasource_name="my_sqlite_db",
        data_connector_name="daily",
        data_asset_name="table_partitioned_by_date_column__A",
        date="2020-01-15",
        expectation_suite=some_expectations,
    )

    # Successful specification with a fresh ExpectationSuite object
    some_more_expectations = context.create_expectation_suite(
        expectation_suite_name="some_more_expectations"
    )
    context.get_validator(
        datasource_name="my_sqlite_db",
        data_connector_name="daily",
        data_asset_name="table_partitioned_by_date_column__A",
        date="2020-01-15",
        expectation_suite=some_more_expectations,
    )

    # Successful specification using create_expectation_suite_with_name
    context.get_validator(
        batch_request=BatchRequest(
            datasource_name="my_sqlite_db",
            data_connector_name="daily",
            data_asset_name="table_partitioned_by_date_column__A",
            partition_request=PartitionRequest(
                partition_identifiers={"date": "2020-01-15"}
            ),
        ),
        create_expectation_suite_with_name="yet_more_expectations",
    )

    # Failed specification, because the named expectation suite already exists
    with pytest.raises(DataContextError):
        context.get_validator(
            datasource_name="my_sqlite_db",
            data_connector_name="daily",
            data_asset_name="table_partitioned_by_date_column__A",
            date="2020-01-15",
            create_expectation_suite_with_name="some_expectations",
        )

    # Failed specification: incorrectly typed expectation suite
    with pytest.raises(ValidationError):
        context.get_validator(
            datasource_name="my_sqlite_db",
            data_connector_name="daily",
            data_asset_name="table_partitioned_by_date_column__A",
            date="2020-01-15",
            expectation_suite={
                "im": "a",
                "dictionary": "not a",
                "ExepctationSuite": False,
            },
        )


def test_get_batch_list_from_new_style_datasource_with_sql_datasource(
    sa, data_context_with_sql_datasource_for_testing_get_batch
):
    context = data_context_with_sql_datasource_for_testing_get_batch

    datasource: Datasource = context.datasources["my_sqlite_db"]
    batch_request: Union[dict, BatchRequest] = {
        "datasource_name": "my_sqlite_db",
        "data_connector_name": "daily",
        "data_asset_name": "table_partitioned_by_date_column__A",
        "partition_request": {"partition_identifiers": {"date": "2020-01-15"}},
    }
    batch_request = BatchRequest(**batch_request)
    batch_list: List[Batch] = datasource.get_batch_list_from_batch_request(
        batch_request=batch_request
    )

    assert batch.batch_spec is not None
    assert (
        batch.batch_definition["data_asset_name"]
        == "table_partitioned_by_date_column__A"
    )
    assert batch.batch_definition["partition_definition"] == {"date": "2020-01-15"}
    assert isinstance(batch.data, SqlAlchemyBatchData)
    assert len(batch.data.head(fetch_all=True)) == 4
