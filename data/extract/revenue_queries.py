REVENUE_QUERY = """
WITH revenue_data AS (

    SELECT 
        d.Annee,
        d.Mois,
        'B2C' AS Source,
        SUM(f.Montant_total_de_la_commande) AS Revenue
    FROM Fact_V_B2C f
    JOIN Dim_Date d ON f.Date_Key = d.Date_Key
    GROUP BY d.Annee, d.Mois

    UNION ALL

    SELECT 
        d.Annee,
        d.Mois,
        'B2B' AS Source,
        SUM(f.Total_TTC) AS Revenue
    FROM Fact_V_B2B f
    JOIN Dim_Date d ON f.Date_Key = d.Date_Key
    GROUP BY d.Annee, d.Mois
)

SELECT 
    Annee,
    Mois,
    Source,
    SUM(Revenue) AS Total_Revenue
FROM revenue_data
GROUP BY Annee, Mois, Source
ORDER BY Annee, Mois
"""