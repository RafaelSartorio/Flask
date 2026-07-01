import sqlite3
import json
import os

def popular_sistema(caminho_json):
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_absoluto = os.path.join(pasta_atual, caminho_json)

    if not os.path.exists(caminho_absoluto):
        print(f"❌ Erro: O arquivo '{caminho_absoluto}' não foi encontrado!")
        return

    with open(caminho_absoluto, 'r', encoding='utf-8') as f:
        lista_de_jogos = json.load(f)

    if not isinstance(lista_de_jogos, list):
        lista_de_jogos = [lista_de_jogos]

    conm = sqlite3.connect(os.path.join(pasta_atual, "Users.db"))
    cursor = conm.cursor()

    print("Iniciando a importação (mantendo os dados existentes)...")

    # Loop principal pelos jogos do JSON
    for dados_jogo in lista_de_jogos:
        # NOVO: Verifica se o jogo já está cadastrado pelo nome
        cursor.execute("SELECT id FROM jogos WHERE nome = ?", (dados_jogo["nome"],))
        jogo_existente = cursor.fetchone()

        if jogo_existente:
            print(f"⚠️ O jogo '{dados_jogo['nome']}' já existe no banco. Pulado para evitar duplicados.")
            continue # Pula para o próximo jogo do JSON, sem cadastrar de novo

        # Se o jogo não existe, cadastra ele normalmente
        print(f"🆕 Cadastrando novo jogo: {dados_jogo['nome']}...")
        cursor.execute("""
            INSERT INTO jogos (nome, sinopse, capa) 
            VALUES (?, ?, ?)
        """, (dados_jogo["nome"], dados_jogo["sinopse"], dados_jogo["capa"]))
        
        jogo_id = cursor.lastrowid

        # Prepara e insere as conquistas desse novo jogo
        lista_final = []
        for t in dados_jogo["conquistas"]:
            lista_final.append((jogo_id, t["nome_trofeu"], t["descricao"], t["dica"]))

        cursor.executemany("""
            INSERT INTO conquistas (jogo_id, nome_trofeu, descricao, dica) 
            VALUES (?, ?, ?, ?)
        """, lista_final)
        
        print(f"   ↳ {len(lista_final)} troféus associados a {dados_jogo['nome']}.")

    conm.commit()
    conm.close()
    print("\n🎉 Processo concluído! Os jogos novos foram adicionados com sucesso.")

if __name__ == "__main__":
    popular_sistema("jogos.json")