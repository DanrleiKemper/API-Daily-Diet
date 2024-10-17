from flask import Flask, request, jsonify
from config import Config
from models.models import db, Refeicao
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar o banco de dados
db.init_app(app)

with app.app_context():
    db.create_all()  # Cria as tabelas no banco de dados

# Registrar uma nova refeição
@app.route('/refeicoes', methods=['POST'])
def registrar_refeicao():
    data = request.json
    nome = data.get('nome')
    descricao = data.get('descricao')
    data_hora = datetime.strptime(data.get('data_hora'), '%Y-%m-%d %H:%M:%S')
    dentro_dieta = data.get('dentro_dieta')

    nova_refeicao = Refeicao(nome=nome, descricao=descricao, data_hora=data_hora, dentro_dieta=dentro_dieta)
    db.session.add(nova_refeicao)
    db.session.commit()
    
    return jsonify({'message': 'Refeição registrada com sucesso!', 'refeicao': nova_refeicao.to_dict()}), 201

# Editar uma refeição existente
@app.route('/refeicoes/<int:id>', methods=['PUT'])
def editar_refeicao(id):
    data = request.json
    refeicao = Refeicao.query.get_or_404(id)
    
    refeicao.nome = data.get('nome', refeicao.nome)
    refeicao.descricao = data.get('descricao', refeicao.descricao)
    refeicao.data_hora = datetime.strptime(data.get('data_hora'), '%Y-%m-%d %H:%M:%S')
    refeicao.dentro_dieta = data.get('dentro_dieta', refeicao.dentro_dieta)

    db.session.commit()
    
    return jsonify({'message': 'Refeição atualizada com sucesso!', 'refeicao': refeicao.to_dict()}), 200

# Apagar uma refeição
@app.route('/refeicoes/<int:id>', methods=['DELETE'])
def apagar_refeicao(id):
    refeicao = Refeicao.query.get_or_404(id)
    db.session.delete(refeicao)
    db.session.commit()
    
    return jsonify({'message': 'Refeição apagada com sucesso!'}), 200

# Listar todas as refeições
@app.route('/refeicoes', methods=['GET'])
def listar_refeicoes():
    refeicoes = Refeicao.query.all()
    return jsonify([refeicao.to_dict() for refeicao in refeicoes]), 200

# Visualizar uma única refeição
@app.route('/refeicoes/<int:id>', methods=['GET'])
def visualizar_refeicao(id):
    refeicao = Refeicao.query.get_or_404(id)
    return jsonify(refeicao.to_dict()), 200

if __name__ == '__main__':
    app.run(debug=True)
