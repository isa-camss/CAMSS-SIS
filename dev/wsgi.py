from main import app
import cfg.ctt as ctt
import sys
import logging
from flask import Flask
from apis.nlp.lemmatizer import api
from apis.nlp.skosmapper import api
import com.nttdata.dgi.util.io as io

LOG_FILE = './log/skosmapper.log'
io.make_file_dirs(LOG_FILE)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO, filename=LOG_FILE)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logger = logging.getLogger("skosmapper")
logger.setLevel(level=logging.WARNING)

app = Flask(__name__)
api.init_app(app)
app.logger = logger

LOG_FILE = './log/nlp.log'
io.make_file_dirs(LOG_FILE)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO, filename=LOG_FILE)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logger = logging.getLogger("nlp")
logger.setLevel(level=logging.WARNING)

app = Flask(__name__)
api.init_app(app)
app.logger = logger


if __name__ == '__main__':
    app.run(port=ctt.API_PORT, debug=ctt.API_DEBUG)
