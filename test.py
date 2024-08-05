from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """ Initiate Setup before each test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_redirect(self):
        """ Test to make sure redirect takes to boggle"""

        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 302)

    def test_show_board(self):
        """Ensure the board page displays correctly"""

        with self.client:
            response = self.client.get('/boggle')
            html = response.get_data(as_text=True)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIn('<h1>B</h1>', html)
            self.assertIn(b'High Score:', response.data)
            self.assertIn(b'Seconds Remaining:', response.data)

    def test_valid_word(self):
        """Test to see if the words are valid in the session"""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["T", "R", "U", "C", "K"], 
                                 ["T", "R", "U", "C", "K"], 
                                 ["T", "R", "U", "C", "K"], 
                                 ["T", "R", "U", "C", "K"], 
                                 ["T", "R", "U", "C", "K"]]
        response = self.client.get('/check-word?word=truck')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test to see if word can be found in the text file"""

        self.client.get('/boggle')
        response = self.client.get('/check-word?word=abacus')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test to see if word is not on board if error will work"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=marioandluigi')
        self.assertEqual(response.json['result'], 'not-word')

