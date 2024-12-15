import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config/config.ini'))


class ConfigUtility:
    OPENAI_API_KEY = config.get('OPENAI', 'open_ai_api_key')

    GROQ_API_KEY = config.get('GROQ', 'groq_api_key')