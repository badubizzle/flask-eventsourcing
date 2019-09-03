
from database import db
from model_types import User, Post

db.create_all()
john = User(username="johndoe")
post = Post()
post.title = "Hello World"
post.body = "This is the first post"
post.author = john

db.session.add(post)
db.session.add(john)

db.session.commit()
print(User.query.all())
print(Post.query.all())
