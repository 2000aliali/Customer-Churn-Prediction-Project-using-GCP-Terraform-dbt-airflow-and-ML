WITH churn_modelling AS (
    SELECT * FROM {{ source('dataset_bank', 'raw_data_from_postgresql_and_xml_files') }}
)

SELECT
    geography,
    gender,
    SUM(exited) AS exited,
    AVG(age) AS avg_age,
    AVG(estimatedsalary) AS avg_salary,
    COUNT(*) AS number_of_exited_or_not
FROM
    churn_modelling
GROUP BY
    geography, gender
