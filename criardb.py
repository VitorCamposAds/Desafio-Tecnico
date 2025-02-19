import sqlite3 as lite  # Importando o módulo SQLite para gerenciar o banco de dados local.

# Criando a conexão com o banco de dados 'dados.db'. Caso o banco de dados não exista, ele será criado automaticamente.
con = lite.connect('dados.db')

# Função para garantir que as tabelas existam
def garantir_criar_tabelas():
    with con:  # O 'with' garante que a conexão seja fechada automaticamente após a execução.
        cur = con.cursor()  # Criando um cursor, que é usado para executar comandos SQL.
        
        # Criando a tabela 'Categoria' se não existir
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Categoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT
        )""")
        print("Tabela Categoria criada com sucesso ou já existente!")

        # Criando a tabela 'Receitas' se não existir
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            categoria TEXT, 
            adicionando_em DATE, 
            valor REAL
        )""")
        print("Tabela Receitas criada com sucesso ou já existente!")

        # Criando a tabela 'Gastos' se não existir
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            categoria TEXT, 
            retirado_em DATE, 
            valor REAL
        )""")
        print("Tabela Gastos criada com sucesso ou já existente!")
        
        # Criando a tabela 'Usuarios' para armazenar nome e senha
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT,
            usuario TEXT, 
            senha TEXT
        )""")
        print("Tabela Usuarios criada com sucesso ou já existente!")
        INSERT INTO Usuarios (nome, usuario, senha) VALUES ('Test User', 'testuser', '1234');


# Garantir que as tabelas estejam criadas
garantir_criar_tabelas()

# Função para visualizar categorias (mesmo se estiver vazio)
def ver_categorias():
    lista_itens = []
    with con:
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM Categoria")
            linha = cur.fetchall()

            if not linha:  # Se a tabela estiver vazia, não entra no loop
                print("Tabela 'Categoria' está vazia.")  # Apenas um aviso
            else:
                for l in linha:
                    lista_itens.append(l)
        except lite.OperationalError as e:
            print(f"Erro ao acessar a tabela Categoria: {e}")
    return lista_itens

# Teste: Ver categorias
categorias_funcao = ver_categorias()
print("Categorias:", categorias_funcao)


# Verificando se as tabelas foram realmente criadas, listando todas as tabelas do banco de dados.
with con:
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("Tabelas no banco de dados:", tables)