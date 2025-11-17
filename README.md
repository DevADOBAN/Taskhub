# 🚀 TaskHub - Gerenciador de Tarefas

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Projeto full-stack é um Desafio** com API REST, interface responsiva e testes automatizados , Aqui você pode organizar suas tarefas de forma WEB ou somente pegar a API para inclemento em algum projeto, Esse projeto surgiu atráves de um Desafio para teste conhecimento em Front-end (HTML,CSS,JS,React) e tambem um pouco de Back-end (Python, Flask, CORS, SQL.

---

## ✨ Funcionalidades

- ✅ Cadastro e login seguro com **JWT**
- ✅ CRUD completo de tarefas
- ✅ Filtros por status, prioridade e data
- ✅ Interface intuitiva e responsiva
- ✅ Notificações e lembretes
- ✅ Modo claro/escuro automático

---

<div align="center">
  <br/>
  <h3>🚪 Comece a Usar Agora</h3>
  <p>Crie, organize e acompanhe suas tarefas com uma interface intuitiva e moderna.</p>
  
  <a style="
    display: inline-block;
    padding: 14px 32px;
    background: ;
    color: white;
    text-decoration: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1.1em;
    box-shadow: 0 4px 6px rgba(50,50,93,.11), 0 1px 3px rgba(0,0,0,.08);
    transition: all 0.3s;
  " onmouseover="this.style.background='#238636'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 7px 14px rgba(50,50,93,.1), 0 3px 6px rgba(0,0,0,.08)'" onmouseout="this.style.background='#2ea44f'; this.style.transform=''; this.style.boxShadow='0 4px 6px rgba(50,50,93,.11), 0 1px 3px rgba(0,0,0,.08)'">
  </a>
  <br/><br/>
</div>

---

## 🛠️ Tecnologias Utilizadas

| Categoria       | Tecnologias |
|-----------------|------------|
| **Back-End**    | `Python` `Flask` `Flask-SQLAlchemy` `Flask-Bcrypt` `Flask-JWT-Extended` |
| **Front-End**   | `HTML5` `CSS3` `JavaScript (Vanilla)` `Responsivo` |
| **Testes**      | `Pytest` `Unittest` `Selenium` |
| **Banco de Dados** | `SQLite` (dev) / `PostgreSQL` (produção) |

---

Como Executar Localmente</h2>
    <pre><code># Clone o repositório
git clone https://github.com/seu-usuario/taskhub.git
cd taskhub

# Back-end
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
flask run

# Front-end (em outra aba)
cd ../frontend
open index.html  # ou use live server
</code></pre>

# Requisitos (pip install ???)

Flask: O framework principal para construir o servidor e as rotas da API.


Flask-SQLAlchemy: Para interagir com o banco de dados e definir os modelos (Modelos Usuário e Tarefa ).


Flask-JWT-Extended: Para lidar com a autenticação JWT (JSON Web Token) , necessária para os endpoints de login e signup.

Flask-Cors: Essencial para permitir que o seu Front End (rodando em outra porta/domínio) possa fazer requisições para esta API.
