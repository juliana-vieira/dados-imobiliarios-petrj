-- Query que explode a coluna "precos", que contém um json aninhado, em colunas individuais
-- Além disso, transforma as colunas com listas em arrays de strings

SELECT *,
       get_json_object(precos, '$.Aluguel') as aluguel, 
       get_json_object(precos, '$.Condomínio') as condominio,
       get_json_object(precos, '$.IPTU') as iptu,
       from_json(carac_cond, 'array<string>') AS array_carac_cond,
       from_json(carac_imovel, 'array<string>') AS array_carac_imovel,
       from_json(endereco, 'array<string>') AS array_endereco
FROM {table}