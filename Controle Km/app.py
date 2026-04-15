from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect("km.db")

conn = conectar()
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS viagens (
nome TEXT, km_i REAL, km_f REAL, km REAL
)
""")
conn.commit()
conn.close()

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        nome = request.form["nome"]
        km_i = float(request.form["km_i"])
        km_f = float(request.form["km_f"])
        km = km_f - km_i

        conn = conectar()
        c = conn.cursor()
        c.execute("INSERT INTO viagens VALUES (?,?,?,?)",(nome,km_i,km_f,km))
        conn.commit()
        conn.close()

        return redirect("/")

    return """
    <h2>Controle KM</h2>
    <form method='POST'>
    Nome: <input name='nome'><br>
    KM Inicial: <input name='km_i'><br>
    KM Final: <input name='km_f'><br>
    <button>Salvar</button>
    </form>
    <br>
    <a href='/relatorio'>Relatório</a>
    """

@app.route("/relatorio")
def relatorio():
    conn = conectar()
    c = conn.cursor()
    dados = c.execute("SELECT * FROM viagens").fetchall()
    conn.close()

    html = "<h2>Relatório</h2>"
    total = 0

    for d in dados:
        html += f"<p>{d}</p>"
        total += d[3]

    html += f"<h3>Total KM: {total}</h3>"
    html += "<br><a href='/'>Voltar</a>"

    return html

app.run(host="0.0.0.0", port=10000)