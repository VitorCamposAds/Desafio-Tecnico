from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import StringVar, ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkcalendar import Calendar, DateEntry
from datetime import date
from view import bar_valores, pie_valores, inserir_categoria, ver_categorias, inserir_gastos, tabela, deletar_gastos, deletar_categoria


""" Projeto: Controle de Despesas Pessoal
    @Autor: Vitor Campos Moura Costa - 19/02/2025 """

# ================= cores =====================================================
co0 = "#2e2d2b"   # Preta
co1 = "#ffffff"   # branca
co2 = "#4fa882"   # verde
co3 = "#38576b"   # valor
co4 = "#403d3d"   # letra
co5 = "#e06636"   # - profit
co6 = "#038cfc"   # azul
co7 = "#3fbfb9"   # verde
co8 = "#263238"   # + verde
co9 = "#e9edf5"   # + verde
# =============================================================================
co10 = "#68c985"  # Verde
co11 = "#ffdad6"  # Vermelho Claro
co12 = "#cbecd5"  # Verde Claro
co13 = "#ff5747"  # Vermelho

colors = ['#4583de', '#ff5747', '#68c985', '#ee9944', '#444466', '#bb5555']

# ================= Tela Para menores ou ate 18 anos =================================================
def login_menor(nome_usuario):
    janela = tk.Toplevel()  # Modificado para Toplevel()
    janela.title("Tela Principal")
    janela.geometry("1200x800")
    janela.configure(background="#f0f0f0")

    # Ícone do aplicativo e da barra de título
    janela.iconbitmap('img/icone1.ico')

    janela.title("Finanças Pessoais")
    janela.geometry('870x680')
    janela.configure(background=co1)

    # Bloqueia o redimensionamento da janela
    janela.resizable(width=False, height=False)

    style = ttk.Style(janela)
    # Tema
    style.theme_use("default") 
    # Modifique a fonte das células da tabela
    style.configure("Treeview", highlightthickness=0, bd=0, font=('Geometria', 13))

    # ================= Frames Cima =================
    frameCima = Frame(janela, width=1043, height=50, bg=co1, relief="flat")
    frameCima.grid(row=0, column=0)
    
    # ================= Frames Meio =================
    frameMeio = Frame(janela, width=1043, height=361, bg=co1, pady=20, relief="raised")
    frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

    # ================= Frames Baixo ================
    frameBaixo = Frame(janela, width=1043, height=300, bg=co1, relief="flat")
    frameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

    # ================= Frames Gráfico ================
    frame_gra_2 = Frame(frameMeio, width=580, height=250, bg=co1)
    frame_gra_2.place(x=415, y=5)

    # Acessando Imagem
    app_img = Image.open('img/logomarca.jpg')
    app_img = app_img.resize((45, 45))
    app_img = ImageTk.PhotoImage(app_img)

    app_logo = Label(frameCima, image=app_img, text=" Minhas Finanças", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Geometria 16 bold'), bg=co1, fg=co4)
    app_logo.place(x=0, y=0)
    
    # Exibe a mensagem de boas-vindas para menores de 18
    label_bem_vindo_menor = Label(frameCima, text=f"Olá {nome_usuario} 😊", font=("Arial", 12), bg=co1, fg=co4)
    label_bem_vindo_menor.place(x=400, y=10)  # Exibe a mensagem na tela de login do menor

# ================= Adicionando funcionalidade de inserção de categorias =================

    # Função para inserir categoria
    def inserir_categoria_b():
        nome = e_categoria.get()
        lista_inserir = [nome]

        # Verificando se os campos estão preenchidos
        for i in lista_inserir:
            if i == '':
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return

        # Passando a função inserir categoria presente na view
        inserir_categoria(lista_inserir)
        messagebox.showinfo('Sucesso', 'Categoria inserida com sucesso!')
        
        # Limpando o campo de entrada
        e_categoria.delete(0, 'end')

        # Pegando as categorias atualizadas
        categorias_funcao = ver_categorias()
        categoria = []

        # Adicionando as categorias na lista
        for i in categorias_funcao:
            categoria.append(i[1])

        # Atualizando o combo de categorias de despesas
        combo_categoria_despesas['values'] = categoria

    # Criando o campo de entrada e botão para inserir categoria
    e_categoria = Entry(frameBaixo, font=('Geometria', 14))
    e_categoria.grid(row=0, column=1, padx=10, pady=10)

    btn_inserir_categoria = Button(frameBaixo, text="Inserir Categoria", command=inserir_categoria_b, font=('Geometria', 14), bg=co2, fg=co1)
    btn_inserir_categoria.grid(row=0, column=2, padx=10, pady=10)

# Funcao inserir Despesa-------------------------------------------------------
    def inserir_despesas_b():
        nome = combo_categoria_despesas.get()
        data = e_cal_despeas.get()
        quantia = e_valor_despesas.get()

        lista_inserir = [nome, data, quantia]

        for i in lista_inserir:
            if i == '':
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return

# Chamando funcao inserir Despesas presente na view
        inserir_gastos(lista_inserir)
        messagebox.showinfo('Sucesso', 'Despesa inserido com sucesso!')

        combo_categoria_despesas.delete(0, 'end')
        e_cal_despeas.delete(0, 'end')
        e_valor_despesas.delete(0, 'end')

        # Atualizando dados
        mostrar_renda()
        grafico_bar()
        resumo()
        grafico_pie()
        
    # Função deletar
    def deletar_dados():
        try:
            treev_dados = tree.focus()
            treev_dicionario = tree.item(treev_dados)
            treev_lista = treev_dicionario['values']
            valor = treev_lista[0]
            nome = treev_lista[1]

            if valor:  # Verifica se há um valor válido
                deletar_gastos([valor])  # Chama a função para deletar os dados
                messagebox.showinfo('Sucesso', 'Excluído com sucesso!')
            else:
                # Atualizando dados
                mostrar_renda()
                grafico_bar()
                resumo()
                grafico_pie()

        except IndexError:
            messagebox.showerror('Erro', 'Selecione um dos dados na tabela')

    # Função para deletar categoria
    def deletar_categoria_b():
        try:
            # Pega a categoria selecionada na Treeview
            treev_dados = tree.focus()
            treev_dicionario = tree.item(treev_dados)
            treev_lista = treev_dicionario['values']
            valor = treev_lista[0]  # ID ou algum identificador único da categoria

            # Chamando a função deletar_categoria da view
            deletar_categoria([valor])
            messagebox.showinfo('Sucesso', 'Categoria excluída com sucesso!')

            # Atualizando dados após a exclusão
            categorias_funcao = ver_categorias()
            categoria = []
            for i in categorias_funcao:
                categoria.append(i[1])

            # Atualizando lista de categorias no combo
            combo_categoria_despesas['values'] = categoria

        except IndexError:
            messagebox.showerror('Erro', 'Selecione uma categoria para excluir')

    # funcao para abrir imagem-----------------------------------------------------
    def ver_imagem():
        global l_imagem, imagem, imagem_string

        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = [int(treev_lista[0])]

        iten = ver_iten(valor)

        imagem = iten[0][8]

        # Abrindo imagem
        imagem = Image.open(imagem)
        imagem = imagem.resize((170, 170))
        imagem = ImageTk.PhotoImage(imagem)

        l_imagem = Label(frameMeio, image=imagem, bg=co1, fg=co4)
        l_imagem.place(x=700, y=10)


    


    # funcao para grafico bar -----------------------------------------------------

    def grafico_bar():
        # obtendo valores de meses
        lista_categorias = ['Renda', 'Gastos', 'Saldo']
        lista_valores = bar_valores() #############################################

        # faça figura e atribua objetos de eixo
        figura = plt.Figure(figsize=(4, 3.45), dpi=60)
        ax = figura.add_subplot(111)

        # ax.autoscale(enable=True, axis='both', tight=None)
        ax.bar(lista_categorias, lista_valores,  color=colors, width=0.9)

        # cria uma lista para coletar os dados plt.patches
        c = 0


        # definir rótulos de barras individuais usando a lista acima
        for i in ax.patches:

            # get_x puxa para a esquerda ou para a direita; get_height empurra para cima ou para baixo
            ax.text(i.get_x()-.001, i.get_height()+.5, str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom', color='dimgrey')

            c += 1

        ax.set_xticklabels(lista_categorias, fontsize=16)
        ax.patch.set_facecolor('#ffffff')
        ax.spines['bottom'].set_color('#CCCCCC')
        ax.spines['bottom'].set_linewidth(1)
        ax.spines['right'].set_linewidth(0)
        ax.spines['top'].set_linewidth(0)
        ax.spines['left'].set_color('#CCCCCC')
        ax.spines['left'].set_linewidth(1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(bottom=False, left=False)
        ax.set_axisbelow(True)
        ax.yaxis.grid(False, color='#EEEEEE')
        ax.xaxis.grid(False)

        canva = FigureCanvasTkAgg(figura, frameMeio)
        canva.get_tk_widget().place(x=10, y=70)


# funcao de resumo total# -----------------------------------------------------
    def resumo():
        valor = bar_valores()

        l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Geometria 1 '), bg='#545454',)
        l_linha.place(x=309, y=54)  # Traço abaixo do texto Salário
        l_sumario = Label(frameMeio, text="Renda                                          ".upper(), height=1, anchor=NW, font=('Geometria 12 bold'), bg=co1, fg='#4583de')
        l_sumario.place(x=306, y=35)

        l_sumario = Label(frameMeio, text='R$ {:,.2f}'.format(valor[0]), height=1, anchor=NW, font=('Geometria 15 bold'), bg=co1, fg='#545454')
        l_sumario.place(x=306, y=70)

        l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Geometria 1 '), bg='#545454',)
        l_linha.place(x=309, y=134)  # Traço abaixo do texto Despesas
        l_sumario = Label(frameMeio, text="Gastos                                         ".upper(), height=1, anchor=NW, font=('Geometria 12 bold'), bg=co1, fg=co13)
        l_sumario.place(x=306, y=115)

        l_sumario = Label(frameMeio, text='R$ {:,.2f}'.format(valor[1]), height=1, anchor=NW, font=('Geometria 15 bold'), bg=co1, fg='#545454')
        l_sumario.place(x=306, y=150)

        l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Geometria 1 '), bg='#545454',)
        l_linha.place(x=309, y=209)  # Traço abaixo do texto Saldo
        l_sumario = Label(frameMeio, text="Saldo                                          ".upper(), height=1, anchor=NW, font=('Geometria 12 bold'), bg=co1, fg='#68c985')
        l_sumario.place(x=306, y=190)

        l_sumario = Label(frameMeio, text='R$ {:,.2f}'.format(valor[2]), height=1, anchor=NW, font=('Geometria 15 bold'), bg=co1, fg='#545454')
        l_sumario.place(x=306, y=220)


    # funcao grafico pie-----------------------------------------------------------
    def grafico_pie():
        
        figura = plt.Figure(figsize=(5, 3), dpi=90)
        ax = figura.add_subplot(111)

        lista_valores = pie_valores()[1] #############################################
        lista_categorias = pie_valores()[0]

        explode = []
        for i in lista_categorias:
            explode.append(0.05)
        ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors, shadow=True, startangle=90)
        ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

        canva_categoria = FigureCanvasTkAgg(figura, frame_gra_2)
        canva_categoria.get_tk_widget().grid(row=0, column=0)


    frame_renda = Frame(frameBaixo, width=300, height=250, bg=co1)
    frame_renda.grid(row=0, column=0)

    frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co11)
    frame_operacoes.grid(row=0, column=1, padx=5)

    frame_configuracao = Frame(frameBaixo, width=220, height=250, bg=co12)
    frame_configuracao.grid(row=0, column=2, padx=5)

    # Tabela Renda mensal ---------------------------------------------------------
    app_tabela = Label(frameMeio, text="Tabela Renda e Gastos", height=1, anchor=NW, font=('Geometria 14 bold'), bg=co1, fg=co4)
    app_tabela.place(x=5, y=309)


    # funcao para mostrar_renda----------------------------------------------------
    def mostrar_renda():
        # criando uma visualização em árvore com barras de rolagem duplas
        tabela_head = ['Cod', 'Categoria', 'Data', 'Qtd']

        lista_itens = tabela()

        global tree

        tree = ttk.Treeview(frame_renda, selectmode="extended", columns=tabela_head, show="headings")

        # vertical scrollbar
        vsb = ttk.Scrollbar()

        # horizontal scrollbar
        hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        hd = ["center", "center", "center", "center"]
        h = [45, 130, 130, 80]
        n = 0

        for col in tabela_head:
            tree.heading(col, text=col.title(), anchor=CENTER)

            # ajuste a largura da coluna para a string do cabeçalho
            tree.column(col, width=h[n], anchor=hd[n])

            n += 1

        for item in lista_itens:
            tree.insert('', 'end', values=item)


    # Configuracoes Despesas ------------------------------------------------------
    l_info = Label(frame_operacoes, text="Novas Despesas", height=1, anchor=NW, relief="flat", font=('Geometria 10 bold'), bg=co11, fg=co4)
    l_info.place(x=10, y=10)


    # Categoria
    l_categoria = Label(frame_operacoes, text="Categoria", height=1, anchor=NW, relief="flat", font=('Geometria 10'), bg=co11, fg=co4)
    l_categoria.place(x=10, y=40)


    # Pegando os categorias--------------------------------------------------------
    categorias_funcao = ver_categorias()
    categorias = []

    for i in categorias_funcao:
        categorias.append(i[1])

    combo_categoria_despesas = ttk.Combobox(
        frame_operacoes, width=10, font=('Geometria 10'))

    combo_categoria_despesas['values'] = (categorias)
    combo_categoria_despesas.place(x=110, y=41)


    # Despesas---------------------------------------------------------------------
    l_cal_despeas = Label(frame_operacoes, text="Data", height=1, anchor=NW, font=('Geometria 10 '), bg=co11, fg=co4)
    l_cal_despeas.place(x=10, y=70)
    e_cal_despeas = DateEntry(frame_operacoes, width=10, background='darkblue', foreground='white', borderwidth=2, year=2025)
    e_cal_despeas.place(x=110, y=71)


    # Valor------------------------------------------------------------------------
    l_valor_despesas = Label(frame_operacoes, text="Quantia Total", height=1, anchor=NW, font=('Geometria 10 '), bg=co11, fg=co4)
    l_valor_despesas.place(x=10, y=100)
    e_valor_despesas = Entry(frame_operacoes, width=11, justify='left', relief="solid")
    e_valor_despesas.place(x=110, y=101)


    # Botao Inserir----------------------------------------------------------------
    img_add_despesas = Image.open('image/add.png')
    img_add_despesas = img_add_despesas.resize((17, 17))
    img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
    botao_inserir_despesas = Button(frame_operacoes, command=inserir_despesas_b, image=img_add_despesas, compound=LEFT, anchor=NW, text="".upper(), width=19, overrelief=RIDGE,  font=('Geometria 7 bold'), bg=co1, fg=co0)
    botao_inserir_despesas.place(x=110, y=131)


    # Operacao Excluir ------------------------------------------------------------
    l_excluir = Label(frame_operacoes, text="Excluir Ação", height=1, anchor=NW, font=('Geometria 10 bold'), bg=co11, fg=co4)
    l_excluir.place(x=10, y=190)


    # Botao Excluir----------------------------------------------------------------
    img_delete = Image.open('image/delete.png')
    img_delete = img_delete.resize((17, 17))
    img_delete = ImageTk.PhotoImage(img_delete)
    botao_deletar = Button(frame_operacoes, command=deletar_dados, image=img_delete, compound=LEFT, anchor=NW, text="".upper(), width=19, overrelief=RIDGE,  font=('Geometria 7 bold'), bg=co1, fg=co0)
    botao_deletar.place(x=110, y=190)

    # Configuracoes Receitas ------------------------------------------------------
    l_info = Label(frame_configuracao, text="Sem Receitas", height=1, anchor=NW, relief="flat", font=('Geometria 10 bold'), bg=co12, fg=co4)
    l_info.place(x=10, y=10)


    # Operacao Nova Categoria -----------------------------------------------------
    l_info = Label(frame_configuracao, text="Categoria", height=1, anchor=NW, font=('Geometria 10 bold'), bg=co12, fg=co4)
    l_info.place(x=10, y=160)
    e_categoria = Entry(frame_configuracao, width=11, justify='left', relief="solid")
    e_categoria.place(x=110, y=160)


    # Botao Inserir----------------------------------------------------------------
    img_add_categoria = Image.open('image/add.png')
    img_add_categoria = img_add_categoria.resize((17, 17))
    img_add_categoria = ImageTk.PhotoImage(img_add_categoria)
    botao_inserir_categoria = Button(frame_configuracao, command=inserir_categoria_b, image=img_add_categoria, compound=LEFT, anchor=NW, text="".upper(), width=19, overrelief=RIDGE,  font=('Geometria 7 bold'), bg=co1, fg=co0)
    botao_inserir_categoria.place(x=110, y=190)


    # Camando funçoes--------------------------------------------------------------

    grafico_bar()
    resumo()
    grafico_pie()
    mostrar_renda()
    janela.mainloop()