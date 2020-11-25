from flask import request, jsonify
from comment_model import Comment
from like_model import Like
from posts import post_by_id
import uuid, csv, datetime
import config

##########? Método que retorna uma lista de todos os likes de um post
def get_likes(post_id):
    post = post_by_id(post_id)
    
    if not post:
        return jsonify({
            "message": "post don't exist",
            "data": {}
        }), 404
    
    likeList = like_list(post_id)
    likeListJson = []
    
    if likeList:
        for likeLine in likeList:
            likeListJson.append(
                like_for_json(
                    Like(
                        likeLine[0],
                        likeLine[1],
                        likeLine[2],
                        likeLine[3]
                    )
                )
            )
        return jsonify({
            "message": "sucessfully fetched",
            "data": likeListJson
        })
        
    return jsonify({"message": "nothing found", "data": {}})

##########? Método que cria um like no banco de dados
def create_like(post_id):
    post = post_by_id(post_id)
    
    if not post:
        return jsonify({
            "message": "post don't exist",
            "data": {}
        }), 404
    
    author = request.json['author']
    
    id = uuid.uuid4()
    created_on = datetime.datetime.now(tz=config.TIME_ZONE)
    
    like = Like(id, post_id, author, created_on)

    try:
        with open('./data/likes.txt', 'a', encoding="utf-8") as file:
            file.write(like_for_string(like))

        file.close()
        
        return jsonify({
            'message': 'sucessfully created',
            'data': like_for_json(like)
        }), 201
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500

##########? Método que busca todos os likes e retorna uma lista
def like_list(post_id):
    likeList = []
    
    with open('./data/likes.txt', newline='', encoding="utf-8") as file:
        spamreader = csv.reader(file, delimiter='|')
        for line in spamreader:
            if line[1] == post_id:
                likeList.append(line)
    
    file.close()
    
    return likeList

##########? Método que converte um Model Like em uma string válida para o banco de dados
def like_for_string(like: Like):
    likeString = str(like.id)+'|'+ str(like.post_id)+'|'+ str(like.author)+'|'+ str(like.created_on)+'\n'

    return likeString

##########? Método que converte um Model like em um json
def like_for_json(like: Like):
    return {
        'id': like.id,
        'post_id': like.post_id,
        'author': like.author,
        'created_on': str(like.created_on),
    }