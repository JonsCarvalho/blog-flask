from flask import request, jsonify
from comment_model import Comment
from posts import post_by_id
import uuid, csv, datetime
import config

##########? Método que retorna uma lista de todos os comentários de um post
def get_comments(post_id):
    post = post_by_id(post_id)
    
    if not post:
        return jsonify({
            "message": "post don't exist",
            "data": {}
        }), 404
    
    commentList = comment_list(post_id)
    commentListJson = []
    
    if commentList:
        for commentLine in commentList:
            commentListJson.append(
                comment_for_json(
                    Comment(
                        commentLine[0],
                        commentLine[1],
                        commentLine[2],
                        commentLine[3],
                        commentLine[4]
                    )
                )
            )
        return jsonify({
            "message": "sucessfully fetched",
            "data": commentListJson
        })
        
    return jsonify({"message": "nothing found", "data": {}})

##########? Método que cria um comentário no banco de dados
def create_comment(post_id):
    post = post_by_id(post_id)
    
    if not post:
        return jsonify({
            "message": "post don't exist",
            "data": {}
        }), 404
    
    body = request.json['body']
    author = request.json['author']
    
    id = uuid.uuid4()
    created_on = datetime.datetime.now(tz=config.TIME_ZONE)
    
    comment = Comment(id, post_id, body, author, created_on)

    try:
        with open('./data/comments.txt', 'a', encoding="utf-8") as file:
            file.write(comment_for_string(comment))

        file.close()
        
        return jsonify({
            'message': 'sucessfully created',
            'data': comment_for_json(comment)
        }), 201
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500

# ##########? Método que deleta um comentário
# def delete_comment(id):
    
#     comment = comment_by_id(id)
    
#     if not post:
#         return jsonify({
#             "message": "post don't exist",
#             "data": {}
#         }), 404

#     try:
#         postList = post_list()
        
#         index = 0;
#         for postInstance in postList:
#             if postInstance[0] == id:
#                 postList.remove(postList[index])
#             index += 1
        
#         with open('./data/posts.txt', 'w', newline='', encoding="utf-8") as file:
#             writer = csv.writer(file, delimiter='|')
#             writer.writerows(postList)
        
#         file.close()
        
#         return jsonify({
#             'message': 'sucessfully deleted',
#             'data': post_for_json(post)
#         }), 200
#     except:
#         return jsonify({'message': 'unable to delete', 'data': {}}), 500

##########? Método que busca todos os comentários e retorna uma lista
def comment_list(post_id):
    commentList = []
    
    with open('./data/comments.txt', newline='', encoding="utf-8") as file:
        spamreader = csv.reader(file, delimiter='|')
        for line in spamreader:
            if line[1] == post_id:
                commentList.append(line)
    
    file.close()
    
    return commentList

##########? Método que converte um Model comment em uma string válida para o banco de dados
def comment_for_string(comment: Comment):
    commentString = str(comment.id)+'|'+ str(comment.post_id)+'|'+ str(comment.body)+'|'+ str(comment.author)+'|'+ str(comment.created_on)+'|'+'\n'

    return commentString

##########? Método que converte um Model comment em um json
def comment_for_json(comment: Comment):
    return {
        'id': comment.id,
        'post_id': comment.post_id,
        'body': comment.body,
        'author': comment.author,
        'created_on': str(comment.created_on),
    }