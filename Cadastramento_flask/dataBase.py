import sqlite3

def Inicializer_db():
    conm = sqlite3.connect("Users.db")
    cursor = conm.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf INTEGER UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            password TEXT NOT NULL    
        )
    """)

    conm.commit()
    conm.close()

def SalvarBanco(cpf, nome, password):
    conm = sqlite3.connect("Users.db")
    cursor = conm.cursor()
    cursor.execute("INSERT INTO usuarios (cpf, nome ,password) VALUES (?, ? , ?)", (cpf, nome,password,))
    conm.commit()
    conm.close()


def buscarBanco(cpf):
    conm = sqlite3.connect("Users.db")
    cursor = conm.cursor()
    cursor.execute("SELECT nome , password FROM usuarios WHERE cpf = ? ", (cpf,))
    usuario = cursor.fetchone()
    return usuario
