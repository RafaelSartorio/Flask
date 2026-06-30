from flask import Flask, render_template ,request
from dataBase import Inicializer_db, SalvarBanco


app = Flask(__name__)

Inicializer_db()



@app.route("/")
def hello_world():
    return render_template("cadastro.html")

@app.route("/criarUser", methods=["POST"])
def SalvarUser():
    cpfUser = request.form.get("cpf")
    nameUser = request.form.get("nome")

    SalvarBanco(cpfUser,nameUser)

    return f"O usuario:{nameUser}  com o CPF:{cpfUser} foi cadastrado com sucesso"
