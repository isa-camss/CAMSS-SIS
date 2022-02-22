from com.nttdata.dgi.io.textify.textify import Textifier
import com.nttdata.dgi.util.io as io
import os
import cfg.ctt as ctt
import json


# file = open(ctt.DOWNLOAD_CORPORA_DETAILS.get('corpora_metadata_file'), "r")
data = json.loads(ctt.DOWNLOAD_CORPORA_DETAILS.get('corpora_metadata_file'))
print(data)
