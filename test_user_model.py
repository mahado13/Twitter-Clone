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

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

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
    
    def test_user_repr(self):
        """Does the repr method work"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        db.session.commit()
        # print('******************************')
        # print(u)
        # print('******************************')
        self.assertEqual(f'<User #{u.id}: {u.username}, {u.email}>', User.__repr__(u))

    def test_is_following(self): 
        """Testing if a user is being followed"""

        u = User(email="test@test.com",username="testuser",password="HASHED_PASSWORD")
        u2 = User(email="test@test2.com",username="testuse2r",password="HASHED_PASSWORD")

        db.session.add_all([u,u2])
        db.session.commit()

        f = Follows(user_being_followed_id =u2.id, user_following_id=u.id)
        db.session.add(f)
        db.session.commit()

        # print('******************************')
        # print(u.is_following(u2))
        # print('******************************')
        self.assertEqual(u.is_following(u2), True)
    
    def test_is_not_following(self): 
        """Testing if a user is not being followed"""

        u = User(email="test@test.com",username="testuser",password="HASHED_PASSWORD")
        u2 = User(email="test@test2.com",username="testuse2r",password="HASHED_PASSWORD")

        db.session.add_all([u,u2])
        db.session.commit()

        # print('******************************')
        # print(u.is_following(u2))
        # print('******************************')
        self.assertEqual(u.is_following(u2), False)
    
    def test_is_following_by(self):
        """Testing if a user being followed by another"""

        u = User(email="test@test.com",username="testuser",password="HASHED_PASSWORD")
        u2 = User(email="test@test2.com",username="testuse2r",password="HASHED_PASSWORD")

        db.session.add_all([u,u2])
        db.session.commit()

        f = Follows(user_being_followed_id =u.id, user_following_id=u2.id)
        db.session.add(f)
        db.session.commit()
        
        self.assertEqual(u.is_followed_by(u2), True)
    
    def test_is_not_following_by(self):
        """Testing if a user is not being followed by another"""

        u = User(email="test@test.com",username="testuser",password="HASHED_PASSWORD")
        u2 = User(email="test@test2.com",username="testuse2r",password="HASHED_PASSWORD")

        db.session.add_all([u,u2])
        db.session.commit()

        # f = Follows(user_being_followed_id =u.id, user_following_id=u2.id)
        # db.session.add(f)
        # db.session.commit()
        
        self.assertEqual(u.is_followed_by(u2), False)

    def test_Create_User(self):
        """Testing whether a user can be created via our Signup methods"""
        u = User.signup("test@test.com","testuser","HASHED_PASSWORD","")
        db.session.commit()
        self.assertEqual(len(User.query.all()),1)
    
    # def test_Create_User_Fail(self):
    #     """Testing to confirm whether we can create a user without the required image_url it shall throw an error"""
    #     u = User.signup("test@test.com","testuser","HASHED_PASSWORD","")
    #     u2 = User.signup("test@test.com","testuser","HASHED_PASSWORD","")

    #     db.session.commit()
    #     self.assertEqual(len(User.query.all()),0)

    def test_authentication_sucess(self):
        """Confirming wheter we can authenticate our users"""
        u = User.signup("test@test.com","testuser","HASHED_PASSWORD","")
        db.session.commit()
   
        test = User.authenticate(u.username, 'HASHED_PASSWORD')
        
        self.assertEqual(test, u)


    def test_authentication_username_fail(self):
        """Confirming that incorrect username will not authenticate"""
        u = User.signup("test@test.com","testuser","HASHED_PASSWORD","")
        db.session.commit()
   
        test = User.authenticate('test', 'HASHED_PASSWORD')
        
        self.assertNotEqual(test, u)

    def test_authentication_password_fail(self):
        """Confirming that incorrect username will not authenticate"""
        u = User.signup("test@test.com","testuser","HASHED_PASSWORD","")
        db.session.commit()

        """This will pull our hashed password instead of our plain text, causing the password to not match"""
        test = User.authenticate(u.username, u.password)
        
        self.assertNotEqual(test, u)

                           