# 🎮 Game Vault

<p align="center">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/SQLite-074D5B?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="TailwindCSS" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
</p>

> **Game Vault** é uma plataforma web no estilo *cyberpunk/neon purple* focada no gerenciamento de coleções de jogos e controle de conquistas (troféus) personalizadas por usuário.

---

## 💻 Sobre o Projeto

O sistema foi desenvolvido utilizando o micro-framework **Flask** integrado ao **SQLite3** para a persistência de dados. A interface visual foi totalmente remodelada utilizando **Tailwind CSS**, trazendo uma atmosfera imersiva inspirada em setups gamers e interfaces futuristas com tons roxos e efeitos neon.

### 🌟 Principais Funcionalidades

* 🔐 **Sistema de Autenticação**: Cadastro de usuários e login seguro utilizando criptografia de senhas (`werkzeug.security`).
* 🎮 **Painel de Jogos (Dashboard)**: Listagem dinâmica e sistema de busca em tempo real para localizar títulos específicos na sua coleção.
* 🏆 **Cofre de Conquistas**: Página interna para cada jogo contendo sinopse, capa e uma lista interativa de troféus com dicas expansíveis para desbloqueio.
* 💾 **Persistência de Progresso**: Marque ou desmarque suas conquistas diretamente na interface e o sistema salvará o estado no banco de dados de forma independente para cada perfil.

---

## 🛠️ Tecnologias Utilizadas

O ecossistema do projeto é composto por:

* **Backend:** [Python](https://www.python.org/) (Versão 3.x) & [Flask](https://flask.palletsprojects.com/)
* **Banco de Dados:** [SQLite3](https://www.sqlite.org/) (Modelagem relacional com chaves estrangeiras e ações em cascata)
* **Segurança:** Criptografia via hash (`generate_password_hash` e `check_password_hash`)
* **Frontend:** HTML5, Jinja2 (Templates dinâmicos) e [Tailwind CSS](https://tailwindcss.com/) (Via CDN para estilização utilitária)

---

## 📐 Estrutura do Banco de Dados

O banco de dados relacional `Users.db` opera com quatro entidades principais estruturadas da seguinte forma:
* `usuarios`: Armazena dados de login (ID, CPF único, Nome e Password com Hash).
* `jogos`: Títulos cadastrados no ecossistema (Nome, Sinopse e URL da Capa).
* `conquistas`: Troféus vinculados a um jogo específico (ID do Jogo, Nome, Descrição e Dica).
* `usuario_conquistas`: Tabela intermediária de relacionamento Muitos-para-Muitos para salvar quais troféus específicos cada CPF obteve.
