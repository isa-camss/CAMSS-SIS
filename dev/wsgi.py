from main import app
import cfg.ctt as ctt
import sys
import logging
import com.nttdata.dgi.util.io as io

LOG_FILE = './log/CAMSS_SIS_API.log'
io.make_file_dirs(LOG_FILE)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO, filename=LOG_FILE)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logger = logging.getLogger("CAMSS_SIS")
logger.setLevel(level=logging.WARNING)


if __name__ == '__main__':
    app.run(port=ctt.API_PORT, debug=ctt.API_DEBUG)
