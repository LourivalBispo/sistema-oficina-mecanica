```python
import os

# Configurações do sistema
DATABASE_PATH = os.path.join('database', 'oficina.db')
SERVICOS_PADRAO = [
    ('Troca de Óleo', 'Troca de óleo e filtro', 120.0, 60),
    ('Alinhamento', 'Alinhamento e balanceamento', 80.0, 90),
    ('Revisão de Freios', 'Verificação e reparo no sistema de freios', 250.0, 120),
    ('Suspensão', 'Revisão do sistema de suspensão', 180.0, 120),
    ('Diagnóstico Eletrônico', 'Leitura de códigos de erro e diagnóstico', 100.0, 60),
    ('Troca de Correia', 'Troca de correia dentada', 300.0, 180),
    ('Revisão Elétrica', 'Verificação do sistema elétrico', 150.0, 120)
]
