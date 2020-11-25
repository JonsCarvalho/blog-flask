from flask import Flask, jsonify
from users import get_user, get_users, update_user, delete_user, post_user
from posts import create_post, get_post, get_posts, delete_post
from comments import create_comment, get_comments
from likes import create_like, get_likes
import datetime, pytz

app = Flask(__name__)
app.config.from_object('config')

##########? Rota raiz da API
@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': f'Olá, seja bem-vindo ao nosso blog! {datetime.datetime.now(tz=pytz.timezone("America/Bahia"))}'})



#################* Rotas para usuários *#################

##########? Rota para criação de registro de usuário
@app.route('/register', methods=['POST'])
def route_post_user():
    return post_user()

##########? Rota para listagem de todos os usuários cadastrados
@app.route('/users', methods=['GET'])
def route_get_users():
    return get_users()

##########? Rota para busca de um usuário através de seu UID
@app.route('/users/<uid>', methods=['GET'])
def route_get_user(uid):
    return get_user(uid)

##########? Rota para atualização de dados de usuário através de seu UID
@app.route('/users/<uid>', methods=['PUT'])
def route_update_user(uid):
    return update_user(uid)

##########? Rota para deletar usuário através de seu UID
@app.route('/users/<uid>', methods=['DELETE'])
def route_delete_user(uid):
    return delete_user(uid)


#################* Rotas para posts *#################

##########? Rota para criação de post
@app.route('/posts', methods=['POST'])
def route_create_post():
    return create_post()

##########? Rota para listagem de todos os posts criados
@app.route('/posts', methods=['GET'])
def route_get_posts():
    return get_posts()

##########? Rota para busca de um post através de seu ID
@app.route('/posts/<id>', methods=['GET'])
def route_get_post(id):
    return get_post(id)

##########? Rota para deletar um post através de seu ID
@app.route('/posts/<id>', methods=['DELETE'])
def route_delete_post(id):
    return delete_post(id)


#################* Rotas para comentários *#################

##########? Rota para criação de comentário
@app.route('/posts/<id>/comments', methods=['POST'])
def route_create_comment(id):
    return create_comment(id)

##########? Rota para listagem de todos os comentários de um post
@app.route('/posts/<id>/comments', methods=['GET'])
def route_get_comments(id):
    return get_comments(id)


#################* Rotas para likes *#################

##########? Rota para criação de like
@app.route('/posts/<id>/likes', methods=['POST'])
def route_create_like(id):
    return create_like(id)

##########? Rota para listagem de todos os likes de um post
@app.route('/posts/<id>/likes', methods=['GET'])
def route_get_likes(id):
    return get_likes(id)



if __name__ == "__main__":
    app.run(host='0.0.0.0')