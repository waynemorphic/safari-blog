import unittest
from application.models import User, Post, Comment
from application import db
from datetime import datetime

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.new_comment = Comment(comment_stuff = 'comment', date_posted = datetime)
        db.session.add(self.new_comment)
        db.session.commit()
        
    def tearDown(self):
        Comment.query.delete()
        db.session.commit()
        
    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)
        
    def test_instance(self):
        self.assertEquals(self.new_comment.comment_stuff, 'comment')
        self.assertEquals(self.new_comment.date_posted, datetime)