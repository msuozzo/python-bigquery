#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def run_natality_tutorial(override_values={}):
    # [START bigquery_query_natality_tutorial]
    """Create a Google BigQuery linear regression input table.

    In the code below, the following actions are taken:
    * A new dataset is created "natality_regression."
    * A query is run against the public dataset,
        bigquery-public-data.samples.natality, selecting only the data of
        interest to the regression, the output of which is stored in a new
        "regression_input" table.
    * The output table is moved over the wire to the user's default project via
        the built-in BigQuery Connector for Spark that bridges BigQuery and
        Cloud Dataproc.
    """

    from google.cloud import bigquery

    # Create a new Google BigQuery client using Google Cloud Platform project
    # defaults.
    client = bigquery.Client()

    # Prepare a reference to a new dataset for storing the query results.
    dataset_id = "natality_regression"
    dataset_id_full = f"{client.project}.{dataset_id}"
    # [END bigquery_query_natality_tutorial]
    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    dataset_id = override_values.get("dataset_id", dataset_id)
    dataset_id_full = f"{client.project}.{dataset_id}"
    # [START bigquery_query_natality_tutorial]

    dataset = bigquery.Dataset(dataset_id_full)

    # Create the new BigQuery dataset.
    dataset = client.create_dataset(dataset)

    # Configure the query job.
    job_config = bigquery.QueryJobConfig()

    # Set the destination table to where you want to store query results.
    # As of google-cloud-bigquery 1.11.0, a fully qualified table ID can be
    # used in place of a TableReference.
    job_config.destination = f"{dataset_id_full}.regression_input"

    # Set up a query in Standard SQL, which is the default for the BigQuery
    # Python client library.
    # The query selects the fields of interest.
    query = """
        SELECT
            weight_pounds, mother_age, father_age, gestation_weeks,
            weight_gain_pounds, apgar_5min
        FROM
            `bigquery-public-data.samples.natality`
        WHERE
            weight_pounds IS NOT NULL
            AND mother_age IS NOT NULL
            AND father_age IS NOT NULL
            AND gestation_weeks IS NOT NULL
            AND weight_gain_pounds IS NOT NULL
            AND apgar_5min IS NOT NULL
    """

    # Run the query.
    query_job = client.query(query, job_config=job_config)
    query_job.result()  # Waits for the query to finish
    # [END bigquery_query_natality_tutorial]


if __name__ == "__main__":
    run_natality_tutorial()
