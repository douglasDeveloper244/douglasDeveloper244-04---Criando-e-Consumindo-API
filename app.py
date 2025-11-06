from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Configurções Gerais
app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, 'database', 'db-produtos.db')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Entidade do Banco de Dados
class Produto(db.Model):
    __tablename__ = "produtos"
    idproduto = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    precocompra = db.Column(db.Float, nullable=False)
    precovenda = db.Column(db.Float, nullable=False)
    datacriacao = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Produto {self.descricao}>"


# Rotas.
@app.route("/")
def home():
    return redirect(url_for("listar_produtos"))


@app.route("/produtos/cadastrar", methods=["GET", "POST"])
def cadastrar_produto():
    if request.method == "POST":
        descricao = request.form["descricao"]
        precocompra = float(request.form["precocompra"])
        precovenda = float(request.form["precovenda"])
        datacriacao = datetime.now()

        produto = Produto(
            descricao=descricao,
            precocompra=precocompra,
            precovenda=precovenda,
            datacriacao=datacriacao,
        )

        db.session.add(produto)
        db.session.commit()

        return redirect(url_for("listar_produtos"))

    return render_template("cadastrar.html")


@app.route("/produtos/listar")
def listar_produtos():
    produtos = Produto.query.all()
    return render_template("listar.html", produtos=produtos)


@app.route("/produtos/editar/<int:idproduto>", methods=["GET", "POST"])
def editar_produto(idproduto):
    produto = Produto.query.get_or_404(idproduto)

    if request.method == "POST":
        produto.descricao = request.form["descricao"]
        produto.precocompra = float(request.form["precocompra"])
        produto.precovenda = float(request.form["precovenda"])
        db.session.commit()
        return redirect(url_for("listar_produtos"))

    return render_template("editar.html", produto=produto)


@app.route("/produtos/excluir/<int:idproduto>")
def excluir_produto(idproduto):
    produto = Produto.query.get_or_404(idproduto)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for("listar_produtos"))


@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
