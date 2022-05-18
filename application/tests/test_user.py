import unittest
from application.models import User, Post, Comment
from application import db

class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(username = 'Doe', email = 'doe@gmail.com', bio = 'baddest', image_file = 'image.url', pass_hash = '123', posts = 'this post', comment_stuff = 'comment')
        db.session.add(self.new_user)
        db.session.commit()
        
    def tearDown(self):
        User.query.delete()
        db.session.commit()
        
    def test_password(self):
        self.assertTrue(self.new_user.pass_hash is not None)
        
    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('123'))
        
    def test_save_user(self):
        self.new_user.save_user()
        self.assertTrue(len(User.query.all())>0)
        
    def test_instance(self):
        self.assertEquals(self.new_user.username, 'Doe')
        self.assertEquals(self.new_user.email, 'doe@gmail.com')
        self.assertEquals(self.new_user.bio, 'baddest')
        self.assertEquals(self.new_user.image_file, 'image.url')
        self.assertTrue(self.new_user.pass_hash, 'Doe')
        self.assertEquals(self.new_user.posts, 'this post')
        self.assertEquals(self.new_user.comment_stuff, 'comment')
        
        