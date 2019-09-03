

from flask_restful import Resource

class UserResource(Resource):
    def get(self, username):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}
