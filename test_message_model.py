"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()



class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.u = u.id
    
    def test_message_model(self):
        """Does our Basic model work?"""
        # print('*********************')
        # print(self.u)
        # print('*********************')
        m = Message(text="Test message",  user_id=self.u)
        db.session.add(m)
        db.session.commit() 

        u = User.query.get(self.u)

        #Confirming that our user does indeed have a message now
        self.assertEqual(len(u.messages), 1)

    # def test_user_must_exist(self):
    #     """Testing that a user_id must exist or a message will not submnit (will throw an error)"""
    #     m = Message(text="Test message",  user_id=10)
    #     db.session.add(m)
    #     db.session.commit() 
    #     all_messages = Message.query.all()
    #     self.assertEqual(len(all_messages), 1)


    
    def test_multiple_messages(self):
        """Testing that a single user may indeed have mutiple messages"""
        m = Message(text="Test message",  user_id=self.u)
        m2 = Message(text="Test message Take 2",  user_id=self.u)
        db.session.add_all([m,m2])
        db.session.commit()
        u = User.query.get(self.u)

        self.assertEqual(len(u.messages), 2)



    def test_message_date_time(self):
        """Testing our default date time creation if none is passed in."""
        m = Message(text="Test message",  user_id=self.u)
        db.session.add(m)
        db.session.commit() 
        # print('*********************')
        new_message = Message.query.get(m.id)
        # print(new_message.timestamp)
        # print('*********************')

        self.assertIsNotNone(new_message.timestamp)

    def test_delete_a_msg(self):
        """Testing if a user is deleted than associated messages will be as well"""
        m = Message(text="Test message",  user_id=self.u)
        db.session.add(m)
        db.session.commit()

        all_messages = Message.query.all()
        self.assertEqual(len(all_messages),1)

        new_message = Message.query.get(m.id)   

        
        db.session.delete(new_message)
        db.session.commit()

        new_total_messages = Message.query.all()
        self.assertEqual(len(new_total_messages),0)


    
    def test_message_user_relationship(self):
        """Testing if we can gather which user the message was created by via the user relationship"""
        m = Message(text="Test message",  user_id=self.u)
        db.session.add(m)
        db.session.commit()

        u = User.query.get(self.u)
        new_message = Message.query.get(m.id)
        # print('*********************')
        # print(new_message.user)
        # print('*********************')

        self.assertEqual(new_message.user, u)

