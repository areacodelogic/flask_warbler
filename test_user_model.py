"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

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

        test_following = Follows(user_being_followed_id=self.u1.id, user_following_id=self.u2.id)

        db.session.add(test_following)
        db.session.commit()

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
        
        user1 = User.query.get_or_404(1)
        user2 = User.query.get_or_404(2)

        self.assertEqual(user1.is_following(user2), True)