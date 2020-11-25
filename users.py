from werkzeug.security import generate_password_hash
from flask import request, jsonify
from user_model import User
import uuid, csv, datetime, ast
import config

##########? Método que retorna uma lista de todos os usuários
def get_users():
    userList = user_list()
    userListJson = []
    
    if userList:
        for userLine in userList:
            userListJson.append(
                user_for_json(
                    User(
                        userLine[0],
                        userLine[1],
                        userLine[2],
                        userLine[3],
                        userLine[4],
                        userLine[5]
                    )
                )
            )
        return jsonify({
            "message": "sucessfully fetched",
            "data": userListJson
        })
        
    return jsonify({"message": "nothing found", "data": {}})

##########? Método que retorna um usuário através de seu UID
def get_user(uid):
    
    user = user_by_uid(uid)
    
    if not user:
        return jsonify({
            "message": "user don't exist",
            "data": {}
        }), 404
    
    return jsonify({
            "message": "sucessfully fetched",
            "data": user_for_json(user)
        }), 201

##########? Método que cria um usuário no banco de dados
def post_user():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    
    
    if user_by_email(email):
        return jsonify({
            "message": "this email is already in use",
            "data": {}
        }), 404
    
    pass_hash = generate_password_hash(password)
    uid = uuid.uuid4()
    created_on = datetime.datetime.now(tz=config.TIME_ZONE)
    updated_on = ''
    user = User(uid, username, pass_hash, email, created_on, updated_on)

    try:
        with open('./data/users.txt', 'a', encoding="utf-8") as file:
            file.write(user_for_string(user))

        file.close()
        
        return jsonify({
            'message': 'sucessfully registered',
            'data': user_for_json(user)
        }), 201
    except:
        return jsonify({'message': 'unable to create', 'data': {}}), 500
    
##########? Método que atualiza dados de um usuário
def update_user(uid):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']
    
    user = user_by_uid(uid)
    if not user:
        return jsonify({
            "message": "user don't exist",
            "data": {}
        }), 404
        
    userTmp = user_by_email(email)
    if userTmp:
        if userTmp.uid != user.uid:
            return jsonify({
            "message": "this email is already in use",
            "data": {}
        }), 404
    
    updated_on = datetime.datetime.now(tz=config.TIME_ZONE)
    pass_hash = generate_password_hash(password)
    
    newUser = User(user.uid, username, pass_hash, email, user.created_on, updated_on)

    try:
        userList = user_list()
        
        index = 0;
        for userInstance in userList:
            if userInstance[0] == uid:
                userList.remove(userList[index])
            index += 1
        
        with open('./data/users.txt', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerows(userList)
        
        file.close()
        
        
        with open('./data/users.txt', 'a', encoding="utf-8") as file:
            file.write(user_for_string(newUser))

        file.close()
        
        return jsonify({
            'message': 'sucessfully updated',
            'data': user_for_json(newUser)
        }), 201
    except:
        return jsonify({'message': 'unable to updated', 'data': {}}), 500

##########? Método que deleta um usuário
def delete_user(uid):
    
    user = user_by_uid(uid)
    
    if not user:
        return jsonify({
            "message": "user don't exist",
            "data": {}
        }), 404

    try:
        userList = user_list()
        
        index = 0;
        for userInstance in userList:
            if userInstance[0] == uid:
                userList.remove(userList[index])
            index += 1
        
        with open('./data/users.txt', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerows(userList)
        
        file.close()
        
        return jsonify({
            'message': 'sucessfully deleted',
            'data': user_for_json(user)
        }), 200
    except:
        return jsonify({'message': 'unable to delete', 'data': {}}), 500

##########? Método que busca todos os usuários e retorna uma lista
def user_list():
    userList = []
    
    with open('./data/users.txt', newline='', encoding="utf-8") as file:
        spamreader = csv.reader(file, delimiter='|')
        for line in spamreader:
            userList.append(line)
    
    file.close()
    
    return userList


##########? Método que busca uma eleição pelo nome e retorna "None" caso não exista
def user_by_email(email):
    userList = user_list()
    
    userExists = False
    index = 0;
    indexFromLine = 0;
    
    for userInstance in userList:
        if userInstance[3] == email:
            userExists = True
            indexFromLine = index
        index += 1
    
    if not userExists:
        return None
    
    user = User(
        userList[indexFromLine][0],
        userList[indexFromLine][1],
        userList[indexFromLine][2],
        userList[indexFromLine][3],
        userList[indexFromLine][4],
        userList[indexFromLine][5]
    )
    
    return user

##########? Método que busca um usuário pelo UID e retorna "None" caso não exista
def user_by_uid(uid):
    userList = user_list()
    
    userExists = False
    index = 0;
    indexFromLine = 0;
    
    for userInstance in userList:
        if userInstance[0] == uid:
            userExists = True
            indexFromLine = index
        index += 1
    
    if not userExists:
        return None
    
    user = User(
        userList[indexFromLine][0],
        userList[indexFromLine][1],
        userList[indexFromLine][2],
        userList[indexFromLine][3],
        userList[indexFromLine][4],
        userList[indexFromLine][5],
    )
    
    return user

##########? Método que converte um Model user em uma string válida para o banco de dados
def user_for_string(user: User):
    userString = str(user.uid)+'|'+ str(user.username)+'|'+ str(user.password)+'|'+ str(user.email)+'|'+ str(user.created_on)+'|'+ str(user.updated_on)+'\n'
    
    return userString

##########? Método que converte um Model user em um json
def user_for_json(user: User):
    return {
        'uid': user.uid,
        'username': user.username,
        'password_hash': user.password,
        'email': user.email,
        'created_on': str(user.created_on),
        'updated_on': str(user.updated_on)
    }