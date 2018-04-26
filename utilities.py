import os
import sys
import random
import giphypop
import urllib.request
from config.config import giphy_key

class Utilities:

    def get_gif(self):
        g = giphypop.Giphy(api_key=giphy_key)
        results = [x for x in g.search('slap')]
        img = random.choice(results)
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        gif = dir_path + '/media/target.gif'

        return urllib.request.urlretrieve(img.media_url, gif)
