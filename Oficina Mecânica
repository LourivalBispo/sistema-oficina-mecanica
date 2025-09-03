import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from datetime import datetime, date
import json
import os

class OficinaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento - Oficina Mecânica")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f5f7f9')
        
        # Conexão com o banco de dados
        self.conectar_banco()
        
        # Configurar interface
        self.configurar_interface()
        
        # Carregar dados iniciais
        self.carregar_dados()
    
    def conectar_banco(self):
        """Conectar ao banco de dados SQLite"""
        self.conn = sqlite3.connect('oficina.db', check_same_thread=False)
        self.criar_tabelas()
    
    def criar_tabelas(self):
        """Criar tabelas se não existirem"""
        cursor = self.conn.cursor()
        
        # Tabela de clientes
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
        
        # Tabela de veículos
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
        
        # Tabela de serviços
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS servicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco REAL,
                tempo_estimado INTEGER
            )
        ''')
        
        # Tabela de agendamentos
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
        
        # Inserir serviços padrão se a tabela estiver vazia
        cursor.execute("SELECT COUNT(*) FROM servicos")
        if cursor.fetchone()[0] == 0:
            servicos_padrao = [
                ('Troca de Óleo', 'Troca de óleo e filtro', 120.0, 60),
                ('Alinhamento', 'Alinhamento e balanceamento', 80.0, 90),
                ('Revisão de Freios', 'Verificação e reparo no sistema de freios', 250.0, 120),
                ('Suspensão', 'Revisão do sistema de suspensão', 180.0, 120),
                ('Diagnóstico Eletrônico', 'Leitura de códigos de erro e diagnóstico', 100.0, 60)
            ]
            cursor.executemany(
                "INSERT INTO servicos (nome, descricao, preco, tempo_estimado) VALUES (?, ?, ?, ?)",
                servicos_padrao
            )
            self.conn.commit()
    
    def configurar_interface(self):
        """Configurar a interface gráfica"""
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Barra de título
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Label(
            title_frame, 
            text="Sistema de Gerenciamento - Oficina Mecânica", 
            font=('Helvetica', 16, 'bold'),
            foreground='#2c3e50'
        ).pack(side=tk.LEFT)
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Abas do sistema
        self.criar_aba_dashboard()
        self.criar_aba_clientes()
        self.criar_aba_veiculos()
        self.criar_aba_servicos()
        self.criar_aba_agendamentos()
        self.criar_aba_relatorios()
        
        # Barra de status
        self.status_var = tk.StringVar()
        self.status_var.set("Sistema pronto")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E))
    
    def criar_aba_dashboard(self):
        """Criar aba do dashboard"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Dashboard")
        
        # Configurar grid
        for i in range(4):
            frame.columnconfigure(i, weight=1)
        frame.rowconfigure(1, weight=1)
        
        # Cards de estatísticas
        cards_info = [
            ("Agendamentos Hoje", "12", "calendar", "#2c3e50"),
            ("Serviços em Andamento", "8", "tools", "#f39c12"),
            ("Serviços Concluídos", "15", "check", "#27ae60"),
            ("Faturamento do Dia", "R$ 4.250", "dollar", "#e74c3c")
        ]
        
        for i, (title, value, icon, color) in enumerate(cards_info):
            card = ttk.Frame(frame, relief=tk.RAISED, borderwidth=1)
            card.grid(row=0, column=i, padx=5, pady=5, sticky=(tk.W, tk.E))
            card.columnconfigure(0, weight=1)
            
            # Ícone (usando texto como placeholder)
            ttk.Label(
                card, 
                text=value, 
                font=('Helvetica', 24, 'bold'),
                foreground=color
            ).grid(row=0, column=0, pady=(10, 5))
            
            ttk.Label(
                card, 
                text=title,
                font=('Helvetica', 10)
            ).grid(row=1, column=0, pady=(0, 10))
        
        # Tabela de agendamentos do dia
        agendamentos_frame = ttk.LabelFrame(frame, text="Agendamentos de Hoje", padding="10")
        agendamentos_frame.grid(row=1, column=0, columnspan=4, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        agendamentos_frame.columnconfigure(0, weight=1)
        agendamentos_frame.rowconfigure(0, weight=1)
        
        # Colunas
        columns = ('cliente', 'veiculo', 'servico', 'horario', 'status')
        self.tree_agendamentos = ttk.Treeview(agendamentos_frame, columns=columns, show='headings', height=10)
        
        # Definir cabeçalhos
        self.tree_agendamentos.heading('cliente', text='Cliente')
        self.tree_agendamentos.heading('veiculo', text='Veículo')
        self.tree_agendamentos.heading('servico', text='Serviço')
        self.tree_agendamentos.heading('horario', text='Horário')
        self.tree_agendamentos.heading('status', text='Status')
        
        # Definir largura das colunas
        self.tree_agendamentos.column('cliente', width=200)
        self.tree_agendamentos.column('veiculo', width=150)
        self.tree_agendamentos.column('servico', width=200)
        self.tree_agendamentos.column('horario', width=100)
        self.tree_agendamentos.column('status', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(agendamentos_frame, orient=tk.VERTICAL, command=self.tree_agendamentos.yview)
        self.tree_agendamentos.configure(yscroll=scrollbar.set)
        
        self.tree_agendamentos.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Botões de ação
        btn_frame = ttk.Frame(agendamentos_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.E))
        
        ttk.Button(btn_frame, text="Atualizar", command=self.carregar_agendamentos).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Novo Agendamento", command=self.novo_agendamento).pack(side=tk.RIGHT, padx=5)
    
    def criar_aba_clientes(self):
        """Criar aba de clientes"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Clientes")
        
        # Frame de listagem
        list_frame = ttk.Frame(frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configurar grid
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        # Barra de pesquisa
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="Pesquisar:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        search_entry.bind('<KeyRelease>', self.pesquisar_clientes)
        
        ttk.Button(search_frame, text="Novo Cliente", command=self.novo_cliente).pack(side=tk.RIGHT)
        
        # Tabela de clientes
        columns = ('id', 'nome', 'telefone', 'email', 'data_cadastro')
        self.tree_clientes = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Definir cabeçalhos
        self.tree_clientes.heading('id', text='ID')
        self.tree_clientes.heading('nome', text='Nome')
        self.tree_clientes.heading('telefone', text='Telefone')
        self.tree_clientes.heading('email', text='E-mail')
        self.tree_clientes.heading('data_cadastro', text='Data Cadastro')
        
        # Ocultar coluna ID
        self.tree_clientes.column('id', width=0, stretch=False)
        
        # Definir largura das colunas
        self.tree_clientes.column('nome', width=200)
        self.tree_clientes.column('telefone', width=120)
        self.tree_clientes.column('email', width=200)
        self.tree_clientes.column('data_cadastro', width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscroll=scrollbar.set)
        
        self.tree_clientes.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Botões de ação
        btn_frame = ttk.Frame(list_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=(tk.E))
        
        ttk.Button(btn_frame, text="Editar", command=self.editar_cliente).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_cliente).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Atualizar", command=self.carregar_clientes).pack(side=tk.RIGHT, padx=5)
        
        # Bind duplo clique para editar
        self.tree_clientes.bind('<Double-1>', lambda e: self.editar_cliente())
    
    def criar_aba_veiculos(self):
        """Criar aba de veículos"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Veículos")
        
        ttk.Label(frame, text="Funcionalidade de veículos em desenvolvimento", 
                 font=('Helvetica', 12)).pack(expand=True)
    
    def criar_aba_servicos(self):
        """Criar aba de serviços"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Serviços")
        
        ttk.Label(frame, text="Funcionalidade de serviços em desenvolvimento", 
                 font=('Helvetica', 12)).pack(expand=True)
    
    def criar_aba_agendamentos(self):
        """Criar aba de agendamentos"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Agendamentos")
        
        ttk.Label(frame, text="Funcionalidade de agendamentos em desenvolvimento", 
                 font=('Helvetica', 12)).pack(expand=True)
    
    def criar_aba_relatorios(self):
        """Criar aba de relatórios"""
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text="Relatórios")
        
        ttk.Label(frame, text="Funcionalidade de relatórios em desenvolvimento", 
                 font=('Helvetica', 12)).pack(expand=True)
    
    def carregar_dados(self):
        """Carregar dados iniciais"""
        self.carregar_clientes()
        self.carregar_agendamentos()
    
    def carregar_clientes(self):
        """Carregar clientes na tabela"""
        # Limpar tabela
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        # Buscar clientes
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome, telefone, email, data_cadastro FROM clientes ORDER BY nome")
        
        # Adicionar à tabela
        for row in cursor.fetchall():
            self.tree_clientes.insert('', tk.END, values=row)
    
    def carregar_agendamentos(self):
        """Carregar agendamentos na tabela"""
        # Dados de exemplo (substituir por consulta ao banco)
        agendamentos = [
            ("Carlos Silva", "HB20 2020", "Revisão Completa", "08:30", "Em Andamento"),
            ("Ana Santos", "Onix 2021", "Troca de Óleo", "10:15", "Concluído"),
            ("Paulo Oliveira", "Corolla 2019", "Alinhamento e Balanceamento", "11:30", "Pendente"),
            ("Mariana Costa", "CR-V 2022", "Troca de Pastilhas de Freio", "14:00", "Em Andamento")
        ]
        
        # Limpar tabela
        for item in self.tree_agendamentos.get_children():
            self.tree_agendamentos.delete(item)
        
        # Adicionar à tabela
        for agendamento in agendamentos:
            self.tree_agendamentos.insert('', tk.END, values=agendamento)
    
    def pesquisar_clientes(self, event=None):
        """Pesquisar clientes conforme digitação"""
        query = self.search_var.get().lower()
        
        # Limpar tabela
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        # Buscar clientes
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, nome, telefone, email, data_cadastro 
            FROM clientes 
            WHERE LOWER(nome) LIKE ? OR LOWER(telefone) LIKE ? OR LOWER(email) LIKE ?
            ORDER BY nome
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        # Adicionar à tabela
        for row in cursor.fetchall():
            self.tree_clientes.insert('', tk.END, values=row)
    
    def novo_cliente(self):
        """Abrir formulário para novo cliente"""
        self.formulario_cliente()
    
    def editar_cliente(self):
        """Abrir formulário para editar cliente selecionado"""
        selection = self.tree_clientes.selection()
        if not selection:
            messagebox.showwarning("Seleção", "Selecione um cliente para editar")
            return
        
        item = self.tree_clientes.item(selection[0])
        cliente_id = item['values'][0]
        
        self.formulario_cliente(cliente_id)
    
    def formulario_cliente(self, cliente_id=None):
        """Janela de formulário de cliente"""
        # Criar janela
        form_window = tk.Toplevel(self.root)
        form_window.title("Novo Cliente" if cliente_id is None else "Editar Cliente")
        form_window.geometry("500x400")
        form_window.grab_set()  # Modal
        form_window.transient(self.root)  # Pertence à janela principal
        
        # Frame principal
        main_frame = ttk.Frame(form_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Variáveis do formulário
        nome_var = tk.StringVar()
        telefone_var = tk.StringVar()
        email_var = tk.StringVar()
        endereco_var = tk.StringVar()
        
        # Se estiver editando, carregar dados
        if cliente_id is not None:
            cursor = self.conn.cursor()
            cursor.execute("SELECT nome, telefone, email, endereco FROM clientes WHERE id = ?", (cliente_id,))
            cliente = cursor.fetchone()
            if cliente:
                nome_var.set(cliente[0])
                telefone_var.set(cliente[1] if cliente[1] else "")
                email_var.set(cliente[2] if cliente[2] else "")
                endereco_var.set(cliente[3] if cliente[3] else "")
        
        # Campos do formulário
        ttk.Label(main_frame, text="Nome *", font=('Helvetica', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        nome_entry = ttk.Entry(main_frame, textvariable=nome_var, width=40)
        nome_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(main_frame, text="Telefone", font=('Helvetica', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        telefone_entry = ttk.Entry(main_frame, textvariable=telefone_var, width=40)
        telefone_entry.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(main_frame, text="E-mail", font=('Helvetica', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        email_entry = ttk.Entry(main_frame, textvariable=email_var, width=40)
        email_entry.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(main_frame, text="Endereço", font=('Helvetica', 10, 'bold')).grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        endereco_text = scrolledtext.ScrolledText(main_frame, width=38, height=4)
        endereco_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        endereco_text.insert('1.0', endereco_var.get())
        
        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=(20, 0))
        
        def salvar_cliente():
            nome = nome_var.get().strip()
            if not nome:
                messagebox.showerror("Erro", "O nome é obrigatório")
                return
            
            telefone = telefone_var.get().strip()
            email = email_var.get().strip()
            endereco = endereco_text.get('1.0', tk.END).strip()
            data_cadastro = date.today().isoformat()
            
            cursor = self.conn.cursor()
            try:
                if cliente_id is None:
                    # Novo cliente
                    cursor.execute(
                        "INSERT INTO clientes (nome, telefone, email, endereco, data_cadastro) VALUES (?, ?, ?, ?, ?)",
                        (nome, telefone, email, endereco, data_cadastro)
                    )
                    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso")
                else:
                    # Editar cliente
                    cursor.execute(
                        "UPDATE clientes SET nome = ?, telefone = ?, email = ?, endereco = ? WHERE id = ?",
                        (nome, telefone, email, endereco, cliente_id)
                    )
                    messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso")
                
                self.conn.commit()
                self.carregar_clientes()
                form_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar cliente: {str(e)}")
        
        ttk.Button(btn_frame, text="Salvar", command=salvar_cliente).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=form_window.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Configurar grid
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Focar no campo nome
        nome_entry.focus()
    
    def excluir_cliente(self):
        """Excluir cliente selecionado"""
        selection = self.tree_clientes.selection()
        if not selection:
            messagebox.showwarning("Seleção", "Selecione um cliente para excluir")
            return
        
        item = self.tree_clientes.item(selection[0])
        cliente_id = item['values'][0]
        cliente_nome = item['values'][1]
        
        # Confirmar exclusão
        if not messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o cliente {cliente_nome}?"):
            return
        
        # Excluir cliente
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso")
            self.carregar_clientes()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir cliente: {str(e)}")
    
    def novo_agendamento(self):
        """Abrir formulário para novo agendamento"""
        messagebox.showinfo("Info", "Funcionalidade de agendamento em desenvolvimento")
    
    def run(self):
        """Executar a aplicação"""
        self.root.mainloop()
    
    def __del__(self):
        """Fechar conexão com o banco ao destruir o objeto"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    """Função principal"""
    root = tk.Tk()
    app = OficinaApp(root)
    app.run()

if __name__ == "__main__":
    main()
