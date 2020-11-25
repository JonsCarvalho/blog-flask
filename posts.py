from flask import request, jsonify
from post_model import Post
import uuid, csv, datetime
import config

##########? Método que retorna uma lista de todos os posts
def get_posts():
    postList = post_list()
    postListJson = []
    
    if postList:
        for postLine in postList:
            postListJson.append(
                post_for_json(
                    Post(
                        postLine[0],
                        postLine[1],
                        postLine[2],
                        postLine[3],
                        postLine[4],
                        postLine[5],
                        postLine[6]
                    )
                )
            )
        return jsonify({
            "message": "sucessfully fetched",
            "data": postListJson
        })
        
    return jsonify({"message": "nothing found", "data": {}})

##########? Método que retorna um post através de seu ID
def get_post(id):
    
    post = post_by_id(id)
    
    if not post:
        return jsonify({
            "message": "post don't exist",
            "data": {}
        }), 404
    
    return jsonify({
            "message": "sucessfully fetched",
            "data": post_for_json(post)
        }), 201

##########? Método que cria um post no banco de dados
def create_post():
    title = request.json['title']
    author = request.json['author']
    body = request.json['body']
    
    id = uuid.uuid4()
    likes = 0
    comments = 0
    created_on = datetime.datetime.now(tz=config.TIME_ZONE)
    
    post = Post(id, title, author, body, likes, comments, created_on)

    try:
        with open('./data/posts.txt', 'a', encoding="utf-8") as file:
            file.write(post_for_string(post))

        file.close()
        
        return jsonify({
            'message': 'sucessfully created',
            'data': post_for_json(post)
        }), 201
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500

##########? Método que deleta um post
def delete_post(id):
    
    post = post_by_id(id)
    
    if not post:
        return jsonify({
            "message": "post don't exist",
            "data": {}
        }), 404

    try:
        postList = post_list()
        
        index = 0;
        for postInstance in postList:
            if postInstance[0] == id:
                postList.remove(postList[index])
            index += 1
        
        with open('./data/posts.txt', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerows(postList)
        
        file.close()
        
        return jsonify({
            'message': 'sucessfully deleted',
            'data': post_for_json(post)
        }), 200
    except:
        return jsonify({'message': 'unable to delete', 'data': {}}), 500

##########? Método que busca todos os posts e retorna uma lista
def post_list():
    postList = []
    
    with open('./data/posts.txt', newline='', encoding="utf-8") as file:
        spamreader = csv.reader(file, delimiter='|')
        for line in spamreader:
            postList.append(line)
    
    file.close()
    
    return postList

##########? Método que busca um post pelo ID e retorna "None" caso não exista
def post_by_id(id):
    postList = post_list()
    
    postExists = False
    index = 0;
    indexFromLine = 0;
    
    for postInstance in postList:
        if postInstance[0] == id:
            postExists = True
            indexFromLine = index
        index += 1
    
    if not postExists:
        return None
    
    post = Post(
        postList[indexFromLine][0],
        postList[indexFromLine][1],
        postList[indexFromLine][2],
        postList[indexFromLine][3],
        postList[indexFromLine][4],
        postList[indexFromLine][5],
        postList[indexFromLine][6],
    )
    
    return post

##########? Método que converte um Model post em uma string válida para o banco de dados
def post_for_string(post: Post):
    postString = str(post.id)+'|'+ str(post.title)+'|'+ str(post.author)+'|'+ str(post.body)+'|'+ str(post.likes)+'|'+ str(post.comments)+'|'+ str(post.created_on)+'\n'

    return postString

##########? Método que converte um Model post em um json
def post_for_json(post: Post):
    return {
        'id': post.id,
        'title': post.title,
        'author': post.author,
        'body': post.body,
        'likes': post.likes,
        'comments': post.comments,
        'created_on': str(post.created_on),
    }