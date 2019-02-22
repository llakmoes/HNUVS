import os


class Config:
    DATABASE_URL = os.environ.get('CLEARDB_DATABASE_URL', 'postgres://iqhtizvllchnwk'
                                                          ':2d5314762a2288ce2ded30d3a527600'
                                                          '0ae1ca65025f53c8a17fb0822d665bd76'
                                                          '@ec2-54-75-230-41.eu-west-1.compute.amazonaws.com:5432'
                                                          '/dfkdep2p0fnjbb')
    TOKEN = os.environ.get('TOKEN', '560289646:AAHat0P1dn9zwO0Lihw953gmRNsiOxwQ3K4')
    PORT = int(os.environ.get('PORT', '5000'))
    VIRTUAL_HOST = os.getenv('VIRTUAL_HOST', 'hnuvs.herokuapp.com')
    MODE = os.getenv('MODE', 'polling')
