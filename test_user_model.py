"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        db.session.commit()

        self.client = app.test_client()

        self.u1 = User.signup(username="test1",
                       email="test1@test1.com",
                       password="HASHED_PASSWORD",
                       image_url=None)
        self.u1.id = 1
        db.session.add(self.u1)
        db.session.commit()

        self.u2 = User.signup(username="test2",
                       email="test2@test2.com",
                       password="HASHED_PASSWORD",
                       image_url=None)
        self.u2.id = 2
        db.session.add(self.u2)
        db.session.commit()

        # test_following = Follows(user_being_followed_id=self.u2.id, user_following_id=self.u1.id)

        # db.session.add(test_following)
        # db.session.commit()
    def tearDown(self):
        """Remove all data from db""" 

        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_repr(self):
        """Does repr work as expected?""" 
        
        self.assertEqual(repr(self.u1), '<User #1: test1, test1@test1.com>')

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?""" 
        
        self.u1.following.append(self.u2)

        self.assertEqual(self.u1.is_following(self.u2), True)

    def test_is_not_following(self):
        """Does is_following successfully detect when user1 is following user2?""" 
        
        self.u1.following.append(self.u2)
        self.assertEqual(self.u1.is_following(self.u2), True)
        
        self.u1.following.pop()
        self.assertEqual(self.u1.is_following(self.u2), False)
    
    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?""" 

        self.u1.followers.append(self.u2)
        self.assertEqual(self.u1.is_followed_by(self.u2), True)

    def test_is_not_followed_by(self):
        """Does is_followed_by successfully detect when user1 is not followed by user2?""" 

        self.u1.followers.append(self.u2)
        self.assertEqual(self.u1.is_followed_by(self.u2), True)

        self.u1.followers.pop()
        self.assertEqual(self.u1.is_followed_by(self.u2), False)
    
    def test_user_create(self): 
        """Does User.create successfully create a new user given valid credentials?""" 

        User.signup(
            username="testuser3",
            email="test3@test3.com",
            password="HASHED_PASSWORD",
            image_url=None
        )

        db.session.commit()

        user = User.query.filter_by(username="testuser3").first()
        
        self.assertTrue(user)

    def test_user_not_create(self): 
        """Does User.create successfully create a new user given valid credentials?""" 

        with self.assertRaises(IntegrityError):
            User.signup(username="test1", email="asdfa", password="HASHED_PASSWORD",image_url=None)
            db.session.commit()

    def test_user_authenticate(self):
        """Does User.authenticate successfully return a user when given a valid username and password?""" 
        
        u = User.signup("test3", "3email", "HASHED_PASSWORD", None)
        db.session.commit()
        
        result = u.authenticate("test3", "HASHED_PASSWORD")

        self.assertTrue(result)
    
    def test_username_not_authenticate(self): 
        u = User.signup("test4", "3email", "HASHED_PASSWORD", None)
        db.session.commit()

        result=u.authenticate("tet4", "HASHED_PASSWORD")

        self.assertFalse(result)

    def test_password_not_authenticate(self): 
        u = User.signup("test4", "3email", "HASHED_PASSWORD", None)
        db.session.commit()

        result = u.authenticate("test4", "H")

        self.assertFalse(result)


