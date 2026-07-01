from flask import Flask, redirect, render_template, request, session, url_for
from dataBase import Inicializer_db, SalvarBanco, buscarBanco
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

app.secret_key = "coloque_uma_chave_criptografica_aqui_super_segura"

Inicializer_db()


@app.route("/dashboard")
def tela_dashboard():
    if "usuario_logado" not in session:
        return redirect(url_for('TelaLogin'))
    
    pesquisa = request.args.get("pesquisa", "")

    conm = sqlite3.connect("Users.db")
    cursor = conm.cursor()

    if pesquisa:
        cursor.execute("SELECT id, nome, sinopse, capa FROM jogos WHERE nome LIKE ?", (f"%{pesquisa}%",))
    else:
        cursor.execute("SELECT id, nome, sinopse, capa FROM jogos")

    jogos_finais = []
    for linha in cursor.fetchall():
        jogos_finais.append({
            "id": linha[0],
            "nome": linha[1],
            "sinopse": linha[2],
            "capa": linha[3]
        })

    conm.close()
    
    return render_template("dashboard.html", 
                           nome=session.get("nome_usuario", "Usuário"), 
                           cpf=session["usuario_logado"], 
                           jogos=jogos_finais,
                           termo_pesquisado=pesquisa)


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

        return redirect(url_for('TelaLogin')) 
    
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
            return redirect(url_for('tela_dashboard'))
        else:
            return 'Senha incorreta'
    else:
        return "Dados não encontrados"
    

@app.route("/logout")
def fazer_logout():
    session.clear() 
    return redirect(url_for('TelaLogin'))


@app.route("/jogo/<int:jogo_id>")
def tela_jogo(jogo_id):
    if "usuario_logado" not in session:
        return redirect(url_for('TelaLogin'))

    cpf_usuario = session["usuario_logado"]

    conm = sqlite3.connect("Users.db")
    cursor = conm.cursor()

    # Busca os dados do jogo
    cursor.execute("SELECT id, nome, sinopse, capa FROM jogos WHERE id = ?", (jogo_id,))
    linha_jogo = cursor.fetchone()
    
    if not linha_jogo:
        conm.close()
        return "Jogo não encontrado", 404
        
    jogo = {"id": linha_jogo[0], "nome": linha_jogo[1], "sinopse": linha_jogo[2], "capa": linha_jogo[3]}

    # Busca todas as conquistas do jogo
    cursor.execute("SELECT id, nome_trofeu, descricao, dica FROM conquistas WHERE jogo_id = ?", (jogo_id,))
    lista_conquistas = []
    for linha in cursor.fetchall():
        lista_conquistas.append({
            "id": linha[0],
            "nome": linha[1],
            "descricao": linha[2],
            "dica": linha[3]
        })

    # CORREÇÃO: Alterado uc.usuario_cpf para uc.cpf_usuario de acordo com sua tabela
    cursor.execute("""
        SELECT uc.conquista_id 
        FROM usuario_conquistas uc
        JOIN conquistas c ON uc.conquista_id = c.id
        WHERE uc.cpf_usuario = ? AND c.jogo_id = ?
    """, (cpf_usuario, jogo_id))
    
    lista_obtidos = [linha[0] for inline_list in cursor.fetchall() for linha in [inline_list]]

    conm.close()
    
    return render_template("jogo.html", jogo=jogo, trofeus=lista_conquistas, obtidos=lista_obtidos)


@app.route("/conquistar/<int:jogo_id>/<int:trofeu_id>", methods=["GET", "POST"])
def conquistar_trofeu(jogo_id, trofeu_id):
    if "usuario_logado" not in session:
        return redirect(url_for('TelaLogin'))

    cpf_usuario_logado = session["usuario_logado"]

    conm = sqlite3.connect("Users.db")
    cursor = conm.cursor()

    # Verifica se este usuário já tem este troféu marcado
    cursor.execute("""
        SELECT 1 FROM usuario_conquistas 
        WHERE cpf_usuario = ? AND conquista_id = ?
    """, (cpf_usuario_logado, trofeu_id))
    
    ja_conquistado = cursor.fetchone()

    if ja_conquistado:
        cursor.execute("""
            DELETE FROM usuario_conquistas 
            WHERE cpf_usuario = ? AND conquista_id = ?
        """, (cpf_usuario_logado, trofeu_id))
    else:
        cursor.execute("""
            INSERT INTO usuario_conquistas (cpf_usuario, conquista_id) 
            VALUES (?, ?)
        """, (cpf_usuario_logado, trofeu_id))

    conm.commit()
    conm.close()

    return redirect(url_for('tela_jogo', jogo_id=jogo_id))


if __name__ == "__main__":
    app.run(debug=True)