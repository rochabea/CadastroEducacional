# 📚 Sistema de Cadastro Educacional – AVA

Bem-vindo ao **Cadastro Educacional**, um sistema acadêmico inspirado em um AVA (Ambiente Virtual de Aprendizagem), desenvolvido em **Python + Django**.  
O sistema oferece funcionalidades para **alunos**, **professores** e **administradores**, permitindo gestão acadêmica completa e interação entre usuários.

---

## 🚀 Funcionalidades

### 👨‍🎓 Área do Aluno
O aluno pode:

- 📊 **Dashboard acadêmico** — Visualização de notas e desempenho
- 📝 **Feedbacks do professor**
- 📅 **Presença nas disciplinas**
- 🕐 **Quadro de horários**
- 🙋‍♂️ **Informações pessoais** — consulta de dados pessoais

---

### 👨‍🏫 Área do Professor
O professor possui todas as funcionalidades dos alunos **+**:

- ➕ **Lançamento de avaliações**
- ✏️ **Edição e exclusão de avaliações**
- 📉 **Cadastro de faltas**
- 💬 **Envio de feedbacks**
- 📊 Dashboard com controle administrativo sobre turmas e notas

---

### 🛠️ Área Administrativa (ADMIN)
Responsável por:

- 📘 Cadastro de disciplinas
- 🏫 Criação e gerenciamento de turmas
- 🕒 Configuração do quadro de horários
- 👥 Administração de usuários e permissões

Acesso ao painel administrativo Django:
```
/ admin
```

Credenciais padrão:

| Usuário | Senha |
|--------|--------|
| admin | admin |

> ⚠️ **Altere essas credenciais ao usar em produção.**

---

## 🧠 Tecnologias Utilizadas

| Tecnologia | Função |
|-----------|--------|
| **Python** | Linguagem principal |
| **Django** | Framework web |
| **SQLite / PostgreSQL** | Banco de dados |
| **HTML / CSS / JS** | Interface |

---

## 📂 Estrutura do Projeto (Simplificada)

CadastroEducacional/
│
├── app/ # Apps do Django
├── templates/ # Arquivos HTML
├── static/ # CSS, JS e imagens
├── manage.py
└── settings/ # Configurações do projeto


---

## ▶️ Como Rodar o Projeto

### ✅ Pré-requisitos
- Python 3.9+
- Pip
- Virtualenv (opcional, recomendado)

### ⚙️ Instalação

```bash
git clone https://github.com/rochabea/CadastroEducacional.git
cd CadastroEducacional

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```
Acesse:

```
http://127.0.0.1:8000
```
Painel admin:
```
http://127.0.0.1:8000/admin
```

🤝 Contribuindo

Contribuições são bem-vindas!

Abra uma issue ou envie um PR:
https://github.com/rochabea/CadastroEducacional/issues

#👨‍🎓 Criadores:

Beatriz Rocha de Araújo, Lucas Tesche, João Victor de Jesus Alves, Ana Alice Martins e Matheus Dias Coelho

# Documentação Online:
https://docs.google.com/document/d/1yIr4DCFEIjcXDgJZFIh3NAHsMw7EEc8riYf-x9j8Oj0/edit?usp=sharing
