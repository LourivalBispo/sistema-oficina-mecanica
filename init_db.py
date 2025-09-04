import sqlite3
import os
from config import DATABASE_PATH, SERVICOS_PADRAO

def init_database():
    """Inicializar o banco de dados com tabelas e dados padrão"""
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Criar tabelas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            email TEXT,
            endereco TEXT,
            data_cadastro DATE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ano INTEGER,
            placa TEXT UNIQUE,
            quilometragem INTEGER,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL,
            tempo_estimado INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            veiculo_id INTEGER,
            servico_id INTEGER,
            data_agendamento DATE,
            horario TIME,
            status TEXT DEFAULT 'Agendado',
            observacoes TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id),
            FOREIGN KEY (veiculo_id) REFERENCES veiculos (id),
            FOREIGN KEY (servico_id) REFERENCES servicos (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agendamento_id INTEGER,
            tecnico TEXT,
            data_inicio DATE,
            data_conclusao DATE,
            custo_total REAL,
            observacoes TEXT,
            FOREIGN KEY (agendamento_id) REFERENCES agendamentos (id)
        )
    ''')
    
    # Inserir serviços padrão se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM servicos")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO servicos (nome, descricao, preco, tempo_estimado) VALUES (?, ?, ?, ?)",
            SERVICOS_PADRAO
        )
    
    # Commit e fechar conexão
    conn.commit()
    conn.close()
    
    print(f"Banco de dados inicializado em: {DATABASE_PATH}")
    print("Tabelas criadas: clientes, veiculos, servicos, agendamentos, ordens_servico")
    print("Serviços padrão inseridos na tabela servicos")

if __name__ == "__main__":
    init_database()
