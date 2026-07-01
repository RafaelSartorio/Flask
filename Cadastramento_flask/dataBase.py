import sqlite3

def Inicializer_db():
    conm = sqlite3.connect("Users.db")
    cursor = conm.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, cpf INTEGER UNIQUE NOT NULL, nome TEXT NOT NULL, password TEXT NOT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS jogos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, sinopse TEXT NOT NULL, capa TEXT NOT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS conquistas (id INTEGER PRIMARY KEY AUTOINCREMENT, jogo_id INTEGER NOT NULL, nome_trofeu TEXT NOT NULL, descricao TEXT NOT NULL, dica TEXT NOT NULL, FOREIGN KEY (jogo_id) REFERENCES jogos (id) ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE IF NOT EXISTS usuario_conquistas (cpf_usuario INTEGER NOT NULL, conquista_id INTEGER NOT NULL, PRIMARY KEY (cpf_usuario, conquista_id), FOREIGN KEY (cpf_usuario) REFERENCES usuarios (cpf) ON DELETE CASCADE, FOREIGN KEY (conquista_id) REFERENCES conquistas (id) ON DELETE CASCADE)")

    conm.commit()
    conm.close()

def SalvarBanco(cpf, nome, password):
    conm = sqlite3.connect("Users.db")
    cursor = conm.cursor()
    cursor.execute("INSERT INTO usuarios (cpf, nome, password) VALUES (?, ?, ?)", (cpf, nome, password))
    conm.commit()
    conm.close()

def buscarBanco(cpf):
    conm = sqlite3.connect("Users.db")
    cursor = conm.cursor()
    cursor.execute("SELECT nome, password FROM usuarios WHERE cpf = ?", (cpf,))
    usuario = cursor.fetchone()
    conm.close()
    return usuario