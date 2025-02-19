# Sistema de Controle de Despesas Pessoais 💸

**Desenvolvedor**: Vitor Campos Moura Costa  
**Versão**: 1.0

Bem-vindo ao **Sistema de Controle de Despesas Pessoais**! Este projeto foi desenvolvido em Python, utilizando a poderosa biblioteca **Tkinter** para a interface gráfica e **SQLite3** como banco de dados. O sistema foi criado com o intuito de gerenciar suas finanças pessoais, permitindo o controle de receitas, despesas e categorização das transações.

## 📋 Funcionalidades

### ✅ Cadastro de Usuários & Login
- **Cadastro de usuários** com validação de senha utilizando **bcrypt** para segurança.
- **Login** com restrição para usuários menores de 18 anos, com funcionalidades limitadas para garantir que apenas despesas sejam contabilizadas.

### 📊 Gráficos Interativos
- **Gráfico de barras**: Representa as receitas e despesas de forma visual e interativa.
- **Gráfico de pizza**: Exibe a distribuição das categorias de despesas de forma clara e objetiva.

### 💵 Controle Financeiro
- **Cálculo de despesas e receitas**: O sistema calcula o total das despesas e receitas, permitindo ao usuário verificar seu saldo.
- **Inserção e Exclusão de Transações**: O usuário pode adicionar ou excluir transações financeiras (despesas e receitas).
- **Categorias de Gasto**: O usuário pode cadastrar e visualizar diferentes tipos de gastos.

### 📅 Restrição de Idade
- **Usuários menores de 18 anos**: A versão do app é limitada apenas ao controle de **despesas** para usuários menores de 18 anos, sem a possibilidade de adicionar receitas.

### 🖥️ Interface Amigável
- Desenvolvida utilizando a biblioteca **Tkinter**, proporcionando uma **interface gráfica simples e intuitiva**.

## 🔧 Tecnologias Utilizadas

Este sistema utiliza as seguintes bibliotecas Python:

- `tkinter`: Para a criação da interface gráfica.
- `sqlite3`: Banco de dados local para armazenar transações e informações de usuários.
- `bcrypt`: Para garantir segurança no armazenamento de senhas dos usuários.
- `PIL` (Pillow): Para manipulação de imagens, como ícones e gráficos.
- `matplotlib`: Para gerar gráficos interativos, como gráficos de barras e pizza.
- `tkcalendar`: Para exibição e seleção de datas.
- `datetime`: Para manipulação de datas no sistema.

## 🚀 Como Rodar o Projeto

### 1. **Clonar o Repositório**

Clone o repositório para o seu computador:

git clone https://github.com/VitorCamposAds/Desafio-Tecnico.git

pip install -r requirements.txt

python app.py

O banco de dados utilizado é o SQLite3. O arquivo de banco de dados, dados.db, será criado automaticamente ao rodar o sistema pela primeira vez.


🗂️ Estrutura do Projeto:

Desafio-Tecnico/
│
├── app.py               # Arquivo principal que inicia a aplicação
├── app_idade.py         # Funções para verificar a idade do usuário
├── view.py              # Funções de visualização e gráficos
├── requirements.txt     # Dependências do projeto
├── dados.db             # Banco de dados SQLite3
├── image/               # Imagens usadas na interface
├── img/                 # Imagens usadas na interface
└── README.md            # Documentação do projeto

📈 Screenshots
Aqui estão algumas imagens de como o sistema se apresenta:
![tela_login](https://github.com/user-attachments/assets/35536dce-5f27-47ac-9765-656c76710729)


![app](https://github.com/user-attachments/assets/2d8848aa-765b-438a-bbf9-5659055b20ae)

Feito por Vitor Campos Moura Costa

www.linkedin.com/in/vitor-campos-tech




