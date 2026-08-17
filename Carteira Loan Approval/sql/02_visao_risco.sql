-- Visão de Risco: Taxa de Rejeição por Faixa de Score e Garantia
SELECT 
    faixa_score AS risco_credit_score,
    loan_type AS tipo_garantia,
    COUNT(*) AS qtd_propostas,
    ROUND(AVG(interest_rate), 2) AS taxa_juros_media,
    ROUND(SUM(CASE WHEN loan_approval_status = 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_rejeicao_pct
FROM carteira_credito
WHERE faixa_score IS NOT NULL
GROUP BY 
    faixa_score, 
    loan_type
ORDER BY 
    risco_credit_score ASC,
    tipo_garantia ASC;