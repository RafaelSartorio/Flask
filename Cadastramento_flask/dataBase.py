import sqlite3

def Inicializer_db():
    conm = sqlite3.connect("Users.db")
    cursor = conm.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf INTEGER UNIQUE NOT NULL,
            nome TEXT NOT NULL
        )
    """)

    conm.commit()
    conm.close()

def SalvarBanco(cpf, nome):
    conm = sqlite3.connect("Users.db")
    cursor = conm.cursor()
    cursor.execute("INSERT INTO usuarios (cpf, nome) VALUES (?, ?)", (cpf, nome))
    conm.commit()
    conm.close()