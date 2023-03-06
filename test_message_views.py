"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_add_message(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    
    def test_add_message_annoynmus(self):
        """If we are not logged in will it kick us back with the proper flash message"""
        with self.client as c:
            resp = c.post("/messages/new", data={"text": "Hello"})
            html = resp.get_data(as_text=True)

            #It should redirect us since were not logged in
            self.assertEqual(resp.status_code, 302)
            
            all_messages = Message.query.all()
            self.assertEqual(len(all_messages),0)
    
    def test_indivdual_message(self):
        """Confirming we can get to an individaul messages post"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
        
        resp = c.post("/messages/new", data={"text": "Welcome to our brand new message"})

        msg = Message.query.one()

        new_resp = c.get(f"/messages/{msg.id}")
        html = new_resp.get_data(as_text=True)
        # print('**********************')
        # print(html)
        # print('**********************')
        self.assertIn("Welcome to our brand new message", html)

    def test_delete_message(self):
        """Confirming if we can delete a message"""
        with self.client as c:
                with c.session_transaction() as sess:
                    sess[CURR_USER_KEY] = self.testuser.id    


        resp = c.post("/messages/new", data={"text": "Welcome to our brand new message"})
        msg = Message.query.one()
        self.assertIsNotNone(msg)
        self.assertEqual(len(Message.query.all()), 1)


        delete_resp = c.post(f"/messages/{msg.id}/delete")
        self.assertEqual(delete_resp.status_code, 302)
        self.assertEqual(len(Message.query.all()), 0)



    

