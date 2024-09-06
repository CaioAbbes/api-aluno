from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt 
from config import Config
from models import db, Aluno
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app) 

@app.route('/get_login_aluno', methods=['GET'])
def get_login_aluno():
    try:
        email_entry = request.args.get('email')
        senha_entry = request.args.get('senha')

        if not email_entry:
            return jsonify({'Erro': 'Email nao digitado'}), 400
        
        if not senha_entry:
            return jsonify({'Erro': 'Senha nao digitada'}), 400

        aluno = Aluno.query.filter_by(email=email_entry).first()

        if aluno and bcrypt.check_password_hash(aluno.senha, senha_entry):
            return jsonify({'Login': True, 'Mensagem': {'id_aluno': aluno.id_aluno, 'nome_completo': aluno.nome_completo, 'data_nascimento': aluno.data_nascimento, 'celular': aluno.celular, 'endereco': aluno.endereco, \
                        'cpf': aluno.cpf, 'foto_perfil': aluno.foto_perfil, 'email': aluno.email, 'senha': aluno.senha}})
        
        return jsonify({'Login': False, 'Mensagem': 'E-mail ou senha incorretos'}), 401

    except Exception as e:
        logging.error(f"Erro no create_aluno {e}")
        return jsonify({'Erro': str(e)}), 500   

@app.route('/get_aluno_email', methods=['GET'])
def get_aluno_email():
    try:
        email_entry = request.args.get('email')

        if not email_entry:
            return jsonify({'Erro': 'Email nao digitado'}), 400
        
        aluno = Aluno.query.filter_by(email=email_entry).first()

        if aluno:
            return jsonify({'Aluno': True, 'Mensagem': {'id_aluno': aluno.id_aluno, 'nome_completo': aluno.nome_completo, 'data_nascimento': aluno.data_nascimento, 'celular': aluno.celular, 'endereco': aluno.endereco, \
                        'cpf': aluno.cpf, 'foto_perfil': aluno.foto_perfil, 'email': aluno.email, 'senha': aluno.senha}})
        
        return jsonify({'Aluno': False, 'Mensagem': 'CPF não existente'}), 401

    except Exception as e:
        logging.error(f"Erro no create_aluno {e}")
        return jsonify({'Aluno': False, 'Mensagem': str(e)}), 500

@app.route('/create_aluno', methods=['POST'])
def create_aluno():
    try:
        data = request.get_json()
        novo_aluno = Aluno(nome_completo = data['nome_completo'], data_nascimento = data['data_nascimento'], celular = data['celular'], endereco = data['endereco'], cpf = data['cpf'], \
                            foto_perfil = data['foto_perfil'], email = data['email'], senha = bcrypt.generate_password_hash(data['senha']).decode('utf-8'))
        db.session.add(novo_aluno)
        db.session.commit()

        logging.info("Sucesso no create_aluno")
        return jsonify({'Criado': True, 'Mensagem': 'Aluno criado com sucesso!'})
    
    except Exception as e:
        logging.error(f"Erro no create_aluno {e}")
        return jsonify({'Criado': True, 'Mensagem': str(e)}), 500


@app.route('/edit_aluno', methods=['POST'])
def edit_aluno():
    try:
        id_entry = request.args.get('id_aluno')
        data = request.get_json()
        
        aluno = Aluno.query.filter_by(id_aluno=id_entry).first()

        if not id_entry:
            return jsonify({'Editado': False, 'Mensagem': 'ID nao digitado'}), 400

        if not aluno:
            return jsonify({'Editado': False, 'Mensagem': 'Aluno nao encontrado'}), 404
        
        aluno.nome_completo = data['nome_completo']
        aluno.data_nascimento = data['data_nascimento']
        aluno.celular = data['celular']
        aluno.endereco = data['endereco']
        aluno.cpf = data['cpf']
        aluno.foto_perfil = data['foto_perfil']
        aluno.email = data['email']
        aluno.senha = bcrypt.generate_password_hash(data['senha']).decode('utf-8')
        
        db.session.commit()
        logging.info("Sucesso no edit_aluno")
        
        return jsonify({'Editado': True, 'Mensagem': 'Aluno editado com sucesso!'})
    
    except Exception as e:
        logging.error(f"Erro no edit_aluno {e}")
        db.session.rollback()
        return jsonify({'Editado': False, 'Mensagem': str(e)}), 500

@app.route('/delete_aluno', methods=['POST'])
def delete_aluno():
    try:
        id_entry = request.args.get('id_aluno')
        
        if not id_entry:
            return jsonify({'Erro': 'id nao digitado'}), 400
        
        aluno = Aluno.query.filter_by(id_aluno=id_entry).first()
        
        if aluno:
            db.session.delete(aluno)
            db.session.commit()
            logging.info("Sucesso no delete_aluno")
            return jsonify({'Deletado': True, 'Mensagem': 'Aluno deletado com sucesso"'})
        
        return jsonify({'Deletado': False, 'Mensagem': 'Aluno nao encontrado'}), 404
        
    except Exception as e:
        logging.error(f"Erro no delete_aluno: {e}")
        db.session.rollback()
        return jsonify({'Deletado': False, 'Mensagem': str(e)}), 500
  
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
