#Imports necesários
import sqlite3 as lite
import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import messagebox


""" Projeto: Controle de Despesas Pessoal
    @Autor: Vitor Campos Moura Costa 19/02/2025 """  
           
# -----------------------------------------------------------------------------

# Criando a conexão com o banco de dados
con = lite.connect('dados.db')

def garantir_criar_tabelas():
    with con:
        cur = con.cursor()
        
        # Criando a tabela Categoria, caso não exista
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Categoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT
        )""")
        print("Tabela Categoria criada ou já existente!")

        # Criando a tabela Receitas, caso não exista
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            categoria TEXT, 
            adicionando_em DATE, 
            valor REAL
        )""")
        print("Tabela Receitas criada ou já existente!")

        # Criando a tabela Gastos, caso não exista
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            categoria TEXT, 
            retirado_em DATE, 
            valor REAL
        )""")
        print("Tabela Gastos criada ou já existente!")

        # Criando a tabela Usuarios, caso não exista
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT, 
            usuario TEXT UNIQUE,
            idade INTEGER,
            senha TEXT
        )""")
        print("Tabela Usuarios criada ou já existente!")

# Chama a função para garantir que as tabelas existem
garantir_criar_tabelas()

def inserir_categoria(i):
    retries = 5  # Número de tentativas
    for attempt in range(retries):
        try:
            with con:
                cur = con.cursor()
                query = "INSERT INTO Categoria (nome) VALUES (?)"
                cur.execute(query, i)
            print("Categoria inserida com sucesso!")
            break  # Se a operação for bem-sucedida, sai do loop
        except sqlite3.OperationalError as e:
            if attempt < retries - 1:
                print(f"Erro de banco de dados. Tentando novamente... ({attempt + 1}/{retries})")
                time.sleep(1)  # Espera 1 segundo antes de tentar novamente
            else:
                print("Erro ao inserir categoria: o banco de dados está bloqueado.")
                raise e

# Funções para Inserir---------------------------------------------------------
# Inserir Receitas
def inserir_receita(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria, adicionando_em, valor) VALUES (?,?,?)"
        cur.execute(query, i)

# Inserir Gastos
def inserir_gastos(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i)

# Funções para Deletar---------------------------------------------------------
# Deletar Receitas
def deletar_receitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id=?"
        cur.execute(query, i)

# Deletar Gastos
def deletar_gastos(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id=?"
        cur.execute(query, i)

# Deletar categorias
def deletar_categoria(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Categoria WHERE id=?"
        cur.execute(query, (i,)) 
        
# Função para ver Dados--------------------------------------------------------
# Ver Categorias
def ver_categorias():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        if not linha:
            print("Nenhuma categoria encontrada!")
        for l in linha:
            print(f"Categoria: {l}")  # Exibindo cada linha retornada
            lista_itens.append(l)
    return lista_itens

# Ver Receitas
def ver_receitas():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

# Ver Gastos
def ver_gastos():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Gastos")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

# -----------------------------------------------------------------------------#################
def tabela():
    gastos = ver_gastos()
    receitas = ver_receitas()

    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    for i in receitas:
        tabela_lista.append(i)

    return tabela_lista


def bar_valores():
    # Receita Total -----------------------------------------------------------
    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    # Despesas Total ----------------------------------------------------------
    gastos = ver_gastos()
    gastos_lista = []

    for i in gastos:
        gastos_lista.append(i[3])

    gasto_total = sum(gastos_lista)

    # Saldo Total -------------------------------------------------------------##################
    saldo_total = receita_total - gasto_total 

    return [receita_total, gasto_total, saldo_total]


def percentagem_valor():
    # Receita Total -----------------------------------------------------------
    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    # Despesas Total ----------------------------------------------------------
    gastos = ver_gastos()
    gastos_lista = []

    for i in gastos:
        gastos_lista.append(i[3])

    gasto_total = sum(gastos_lista)

    # Porcentagem Total ----------------------------------------------------------
    if receita_total != 0:
        total = 100 - ((receita_total - gasto_total) / receita_total) * 100
    else:
        total = 0

    return [total]


def pie_valores():# -----------------------------------------------------------
    gastos = ver_gastos()
    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    dataframe = pd.DataFrame(tabela_lista, columns=['id', 'categoria', 'data', 'valor'])
    dataframe = dataframe.groupby('categoria')['valor'].sum()  # Obtenha a soma das durações por categoria

    lista_quantias = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)

    return ([lista_categorias, lista_quantias])

# Função para pegar os usuários do banco de dados
def carregar_usuarios():
    con = sqlite3.connect('dados.db')
    cur = con.cursor()
    
    # Pega os usuários da tabela
    cur.execute("SELECT nome FROM Usuarios")  # Aqui você pode pegar o nome ou outro campo
    usuarios = cur.fetchall()  # Retorna uma lista de tuplas (nome,)

    con.close()
    
    return [usuario[0] for usuario in usuarios]  # Extrai o nome de cada tupla

# Função para exibir o nome do usuário selecionado
def usuario_selecionado(event):
    usuario = combo_usuarios.get()
    print(f"Usuário selecionado: {usuario}")