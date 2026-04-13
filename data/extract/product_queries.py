ABC_XYZ_QUERY = """
WITH product_sales AS (

    -- B2C DATA
    SELECT 
        f.Produit_Key AS Product_ID,
        d.Full_Date,
        1 AS Quantity,  -- FIX
        f.Sous_total_de_la_commande AS Revenue
    FROM Fact_V_B2C f
    JOIN Dim_Date d ON f.Date_Key = d.Date_Key

    UNION ALL

    -- B2B DATA
    SELECT 
        f.Id_Produit AS Product_ID,
        d.Full_Date,
        f.Quantite AS Quantity,
        f.Montant_Total_HT AS Revenue
    FROM Fact_V_B2B f
    JOIN Dim_Date d ON f.Date_Key = d.Date_Key
)

SELECT 
    Product_ID,
    Full_Date,
    SUM(Quantity) AS Quantity,
    SUM(Revenue) AS Revenue
FROM product_sales
GROUP BY Product_ID, Full_Date
"""

MARKET_BASKET_QUERY = """
SELECT 
    Numero_de_commande AS Transaction_ID,
    Produit_Key AS Product_ID,
    1 AS Quantite
FROM Fact_V_B2C
WHERE Numero_de_commande IS NOT NULL
"""

PRICE_SENSITIVITY_QUERY = """
SELECT 
    d.Full_Date,
    f.Produit_Key AS Product_ID,

    f.Prix_du_produit AS Prix_du_produit,

    -- B2C has no quantity → simulate
    1 AS Quantite,

    c1.price AS Competitor_Price_1,
    c2.price AS Competitor_Price_2

FROM Fact_V_B2C f
JOIN Dim_Date d ON f.Date_Key = d.Date_Key

LEFT JOIN Fact_Conccurrence fc 
    ON f.Produit_Key = fc.Id_Produit_Sougui

LEFT JOIN Dim_Produit_Concurrence_1 c1
    ON fc.Produit_Ileyckom_Id = c1.Produit_Ileyckom_Id

-- ✅ FIX HERE
LEFT JOIN Dim_Produit_Concurrence_2 c2
    ON fc.Produit_Kalys_Id = c2.Produit_Klays_Id
"""

PRODUCT_DIM_QUERY = """
SELECT 
    Id_Produit,
    Nom,
    Categorie,
    PU_HT,
    Tarif_Regulier,
    Tarif_Promo,
    En_Stock
FROM Dim_Produit_Sougui
"""