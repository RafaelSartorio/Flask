from flask import Flask, redirect, render_template, request, session, url_for
from dataBase import Inicializer_db, SalvarBanco, buscarBanco
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "coloque_uma_chave_criptografica_aqui_super_segura"
Inicializer_db()


@app.route("/dashboard")
def tela_dashboard():
    if "usuario_logado" not in session:
        return redirect(url_for('TelaLogin'))
    return render_template("dashboard.html", nome=session["nome_usuario"], cpf=session["usuario_logado"])

@app.route("/")
def cadastroUsuario():
    return render_template("cadastro.html")

@app.route("/criarUser", methods=["POST"])
def SalvarUser():
    cpfUser = request.form.get("cpf")
    nameUser = request.form.get("nome")
    passwordUser = request.form.get("password")

    if cpfUser and nameUser and passwordUser:
        passwordUserEnconder = generate_password_hash(passwordUser)
        SalvarBanco(cpfUser, nameUser, passwordUserEnconder)
        # Opcional: Você pode mudar isso para redirecionar para o login após cadastrar!
        # return redirect(url_for('TelaLogin'))
        return "Usuário criado com sucesso"
    
    return "Digite os dados que foram solicitados"

@app.route("/telaLogin", methods=["GET"])
def TelaLogin():
    return render_template("login.html")

@app.route("/fazerLogin", methods=["POST"])
def Fazerlogin():
    cpf_digitado = request.form.get("cpf")
    senhaDigitado = request.form.get("password")

    usuario = buscarBanco(cpf_digitado)

    if usuario:
        nome_usuario = usuario[0]
        senha_banco = usuario[1]
        if check_password_hash(senha_banco, senhaDigitado):
            session["usuario_logado"] = cpf_digitado
            session["nome_usuario"] = nome_usuario
            # Adicionado o redirecionamento para mandar o usuário para a página restrita
            return redirect(url_for('tela_dashboard'))
        else:
            return 'Senha incorreta'
    else:
        return "Dados não encontrados"
    
@app.route("/logout")
def fazer_logout():
    # Limpa todos os dados salvos na sessão (destrói o crachá)
    session.clear() 
    return redirect(url_for('tela_login'))