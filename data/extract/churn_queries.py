CHURN_QUERY = """
SELECT 
    f.Client_Key,
    COUNT(*) AS Frequency,
    SUM(f.Montant_total_de_la_commande) AS Total_Spent,
    MAX(d.Full_Date) AS Last_Purchase_Date
FROM Fact_V_B2C f
JOIN Dim_Date d ON f.Date_Key = d.Date_Key
WHERE f.Etat_de_la_commande = 'Terminée'
GROUP BY f.Client_Key
"""