from urllib import urlretrieve, urlopen
from json import load
from os import mkdir, path
from pyechonest import config
from pyechonest import song
import time
config.ECHO_NEST_API_KEY='WQ7YLXHWHTEIOZ9SK'

DATA_DIR = '../data/echonest'
DATA_SET = '7digital'

def download(url, file):
    start_t = time.time()
    
    def progress(bl, blsize, size):

        '''dldsize = min(bl*blsize, size)
        if size != -1:
            p = float(dldsize) / size
            try:
                elapsed = time.time() - start_t 
                est_t = elapsed / p - elapsed
            except:
                est_t = 0
                print "%6.2f %% %6.0f s %6.0f s %6i / %-6i bytes" % (p*100, elapsed, est_t, dldsize, size)
        else:
            print "%6i / %-6i bytes" % (dldsize, size)
    '''
    urlretrieve(url, file, progress)
    
def getsongs(emotion):
    if not path.exists(DATA_DIR+'/'+emotion):
        mkdir(DATA_DIR+'/'+emotion)
    songlist = song.search(mood=emotion, buckets=['id:'+DATA_SET, 'tracks'], limit=True)
    for everysong in songlist:
        print everysong.title
        if '/' in everysong.title:
            download(everysong.get_tracks(DATA_SET)[0].get('preview_url'), DATA_DIR+'/'+emotion+'/'+everysong.title.replace('/','_')+'.mp3')
        else:
            download(everysong.get_tracks(DATA_SET)[0].get('preview_url'), DATA_DIR+'/'+emotion+'/'+everysong.title+'.mp3')

if not path.exists(DATA_DIR):
    mkdir(DATA_DIR)

list_term_request = urlopen('http://developer.echonest.com/api/v4/artist/list_terms?api_key='+config.ECHO_NEST_API_KEY+'&format=json&type=mood')
emdic = load(list_term_request)

for emotionunit in emdic.get('response').get('terms'):
    emotion = emotionunit.get('name')
    getsongs(emotion)