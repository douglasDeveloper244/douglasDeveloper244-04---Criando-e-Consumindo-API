from Code.app import db


class Produto(db.Model):
    __tablename__ = "produtos"

    idproduto = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    precocompra = db.Column(db.Float, nullable=False)
    precovenda = db.Column(db.Float, nullable=False)
    datacriacao = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Produto {self.descricao}>"
