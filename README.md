# 📖 Sistema Breach

Bem-vindo ao **Breach System**, um sistema acadêmico inspirado em um AVA (Ambiente Virtual de Aprendizagem), desenvolvido em **Python + Django**.  
O sistema oferece funcionalidades para **alunos**, **professores** e **administradores**, permitindo gestão acadêmica completa e interação entre usuários.

# 📚 Imagens do Sistema
<img width="1055" height="526" alt="{F7D9ADD3-D233-4187-B600-63810DD6067A}" src="https://github.com/user-attachments/assets/f416e2f8-6d18-467c-a446-2b4ca3941f90" />
<img width="1056" height="528" alt="{BA6996E6-7008-4274-AC1E-AE5E2FEB679D}" src="https://github.com/user-attachments/assets/e30ca568-008c-4843-b561-f0aee8cc94ee" />
<img width="1058" height="527" alt="{26DA6E72-68C9-48C1-B07A-E3AF7A274195}" src="https://github.com/user-attachments/assets/1f83213d-ef20-410a-b1b2-8f18ed3a5ecd" />
<img width="1055" height="526" alt="{DF120FA1-DD9F-45EC-A399-70C43A850D1F}" src="https://github.com/user-attachments/assets/11a7d41c-87bd-4a20-b5cd-6c8128103144" />
<img width="1059" height="525" alt="{A191E4FC-4910-4A2A-ABAF-5AE2D5207C5D}" src="https://github.com/user-attachments/assets/879ee50e-f259-4094-8318-5770d0454b84" />
<img width="1058" height="528" alt="{C00A0665-7AE8-4FB3-AB6A-05AF7E774EF9}" src="https://github.com/user-attachments/assets/6bafd819-982f-43d8-86dd-3cfb4fc78b93" />

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
