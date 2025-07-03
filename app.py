from flask import Flask, render_template, request, redirect, make_response

app = Flask(__name__)

filmes_por_genero = {
    "acao": ["Missão Impossível", "John Wick", "Mad Max"],
    "comedia": ["Se Beber, Não Case", "As Branquelas", "Superbad"],
    "drama": ["Clube da Luta", "Forrest Gump", "A Procura da Felicidade"],
    "ficcao": ["Matrix", "Interestelar", "Blade Runner"],
    "terror": ["Invocação do Mal", "O Iluminado", "Hereditário"]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        genero = request.form["genero"]
        notificacoes = "sim" if "notificacoes" in request.form else "nao"

        resp = make_response(redirect("/preferencias"))
        resp.set_cookie("nome", nome, max_age=7*24*60*60)
        resp.set_cookie("genero", genero, max_age=7*24*60*60)
        resp.set_cookie("notificacoes", notificacoes, max_age=7*24*60*60)
        return resp
    return render_template("cadastro.html")

@app.route("/preferencias")
def preferencias():
    nome = request.cookies.get("nome")
    genero = request.cookies.get("genero")
    notificacoes = request.cookies.get("notificacoes")

    if not nome or not genero or not notificacoes:
        return render_template("preferencias.html", preferencias=None)
    
    return render_template("preferencias.html", preferencias={
        "nome": nome,
        "genero": genero,
        "notificacoes": notificacoes
    })

@app.route("/recomendar")
def recomendar():
    genero = request.args.get("genero", "").lower()
    filmes = filmes_por_genero.get(genero, [])
    return render_template("recomendar.html", genero=genero, filmes=filmes)

if __name__ == "__main__":
    app.run(debug=True)
