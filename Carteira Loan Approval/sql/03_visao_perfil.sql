-- Visão Demográfica: Perfil Escolar e Profissional
SELECT 
    education AS grau_instrucao,
    employment_status AS status_emprego,
    COUNT(*) AS qtd_clientes,
    ROUND(AVG(annual_income), 2) AS renda_media_anual,
    ROUND(AVG(age), 1) AS idade_media,
    SUM(loan_amount_requested) AS volume_total_solicitado
FROM carteira_credito
GROUP BY 
    education,
    employment_status
ORDER BY 
    volume_total_solicitado DESC;