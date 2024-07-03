import unittest
from unittest.mock import patch
from io import StringIO
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from main import main

class TestMain(unittest.TestCase):
    @patch('sys.argv', ['main.py', 'test_query'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main(self, mock_stdout):
        main()
        output = mock_stdout.getvalue()
        self.assertIn('Response:', output)
        self.assertIn('Sources:', output)

    @patch('sys.argv', ['main.py'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_results(self, mock_stdout):
        with patch.object(Chroma, 'similarity_search_with_relevance_scores', return_value=[]):
            main()
            output = mock_stdout.getvalue()
            self.assertIn('Unable to find matching results.', output)

    @patch('sys.argv', ['main.py', 'test_query'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_low_relevance_score(self, mock_stdout):
        with patch.object(Chroma, 'similarity_search_with_relevance_scores', return_value=[
            (None, 0.5)
        ]):
            main()
            output = mock_stdout.getvalue()
            self.assertIn('Unable to find matching results.', output)

if __name__ == '__main__':
    unittest.main()