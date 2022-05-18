import unittest
from application.models import User, Post, Comment
from application import db
from datetime import datetime

class TestModelPost(unittest.TestCase):
    def setUp(self):
        self.new_post = Post(title_stuff = 'post', post_stuff = 'newest post', date_posted = datetime, comment_stuff = 'comment', user_id = '1')
        db.session.add(self.new_post)
        db.session.commit()
        
    def tearDown(self):
        Post.query.delete()
        db.session.commit()
    
    def test_save_post(self):
        self.new_post.save_post()
        self.assertTrue(len(Post.query.all())>0)
        
    def test_get_post_id(self):
        self.new_post.get_post_id()
        self.assertEqual(Post.query.filter_by(id = id))
        
    def test_instance(self):
        self.assertEquals(self.new_post.title_stuff, 'posts')
        self.assertEquals(self.new_post.post_stuff, 'newest post')
        self.assertEquals(self.new_post.date_posted, datetime)
        self.assertEquals(self.new_post.comment_stuff, 'comment')
        self.assertTrue(self.new_post.user_id, '1')
        
    