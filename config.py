import os


class Config:
    DATABASE_URL = os.environ.get('CLEARDB_DATABASE_URL', 'mysql+mysqlconnector://root:root@localhost:8889/hnuvs_db')
    TOKEN = os.environ.get('TOKEN', '560289646:AAFzO2loYla3rOfMPBT_1S9YihU1JYN6dBU')
    PORT = int(os.environ.get('PORT', '5000'))
    VIRTUAL_HOST = os.getenv('VIRTUAL_HOST', 'hnuvs.herokuapp.com')
    MODE = os.getenv('MODE', 'webhook')
