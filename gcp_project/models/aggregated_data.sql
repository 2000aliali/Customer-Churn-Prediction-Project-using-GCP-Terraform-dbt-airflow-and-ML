WITH churn_modelling AS (
    SELECT * FROM {{ source('dataset_bank', 'raw_data_from_postgresql_and_xml_files') }}
)

SELECT
    geography,
    gender,
    AVG(creditscore) AS avg_credit_score,
    SUM(exited) AS total_exited
FROM
    churn_modelling
GROUP BY
    geography, gender
