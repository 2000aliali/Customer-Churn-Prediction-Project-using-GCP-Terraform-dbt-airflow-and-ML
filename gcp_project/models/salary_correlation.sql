WITH churn_modelling AS (
    SELECT * FROM {{ source('dataset_bank', 'raw_data_from_postgresql_and_xml_files') }}
)

SELECT
    SUM(exited) AS exited,
    SUM(CASE WHEN estimatedsalary > (SELECT AVG(estimatedsalary) FROM churn_modelling) THEN 1 ELSE 0 END) AS is_greater,
    COUNT(*) AS correlation
FROM
    churn_modelling
GROUP BY
    estimatedsalary
