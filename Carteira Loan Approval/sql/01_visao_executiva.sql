-- Visão Executiva: Volume e Saúde da Carteira por Finalidade
SELECT 
    loan_purpose AS finalidade_emprestimo,
    COUNT(*) AS qtd_propostas,
    SUM(loan_amount_requested) AS volume_total_solicitado,
    ROUND(AVG(loan_amount_requested), 2) AS ticket_medio,
    ROUND(SUM(CASE WHEN loan_approval_status = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS taxa_aprovacao_pct
FROM carteira_credito
GROUP BY 
    loan_purpose
ORDER BY 
    volume_total_solicitado DESC;