#!/usr/bin/env python

import os
import argparse
from mypleasure.tars import Tars
from configparser import ConfigParser
from multiprocessing.pool import ThreadPool as Pool


def parse_args():
  """Parse argument passed in CLI.

  Returns:
    The tuple of arguments (url, id, requester, workers) passed in CLI.
  """
  config = ConfigParser()
  config.read('settings/settings.cfg')

  parser = argparse.ArgumentParser(description='Crawls and scrapes content from websites ("providers").')
  parser.add_argument('--url', type=str, help='url to crawl and scrape')
  parser.add_argument('--id', type=int, help='job id in queue')
  parser.add_argument('--requester', type=int, help='user id')
  parser.add_argument('--workers', type=int, default=config.get('app', 'workers'), help='number of workers to use, ' + config.get('app', 'workers') + ' by default - ideal number is twice the number of CPUs available on the machine')

  return parser.parse_args()

if __name__ == '__main__':
  options = parse_args()

  tars = Tars(debug=True)
  tars.send_on_mission('http://xhamster.com/movies/377175/swingers_party_on_a_yacht_in_florida.html')
  tars.send_on_mission('http://xhamster.com/movies/3093854/short_shorts.html')
  tars.send_on_mission('http://xhamster.com/movies/1996078/italian_beauties_full_italian_movie.html')
  """
  tars.send_on_mission('http://www.youporn.com/watch/10166327/dorcel-airlines-paris-new-york/?from=search_full&pos=1')
  tars.send_on_mission('http://www.xvideos.com/video1162298/born_slippy_best_anal_compilation_ever_')
  tars.send_on_mission('http://www.xvideos.com/video7244861/wet_and_horny_amateur_asian_slut_rides_white_boyfriend')
  tars.send_on_mission('http://www.xvideos.com/video8382765/_homepornwatchhd.com_full_movie_with_hard_passionate_fucking')
  tars.send_on_mission('http://www.xvideos.com/video7255307/homemade_amateur_sextape')
  tars.send_on_mission('http://www.xvideos.com/video4238684/img_0977')
  tars.send_on_mission('http://www.xvideos.com/video5194815/lets_try_anal_')
  """
  """
  pool = Pool(options.workers)
  pool.map(tars.send_on_mission,
           ('http://www.youporn.com/watch/10436027/18yo-busty-buffy-fucks-for-cum-on-tits/?from=related3&al=2&from_id=10436027&pos=5',
            'http://www.youporn.com/watch/9565375/lesbea-busty-lesbian-has-g-spot-orgasm-during-soapy-romp-in-the-bath-tub/?from=vbwn',
            'http://www.youporn.com/watch/9627203/a-class-in-sexercise/?from=vbwn',
            'http://www.youporn.com/watch/10717535/mrs-santa-gets-a-cream-pie-for-xxxmas/',
            'http://www.youporn.com/watch/9082257/like-my-naughty-miss-santa-outfit-now-watch-me-suck-and-fuck-you-in-it/',
            'http://www.youporn.com/watch/10781107/porn-films-3d-explicit-dildo-gymnastics/',
            'http://www.youporn.com/watch/10356485/doubleviewcasting-mila-regular/',
            'http://www.youporn.com/watch/8395983/lone-cock-rider-playvision/',
            'http://www.youporn.com/watch/10778551/rachel-loves-to-please/',
            'http://www.youporn.com/watch/10774689/love-creampie-exotic-busty-beauty-needs-two-men-to-satisfy-her/',
            'http://www.youporn.com/watch/9442047/her-pussy-gets-very-creamy-masturbating-in-gym/',
            'http://www.youporn.com/watch/10314337/evilangel-sheena-shaw-s-anal-insertion-and-rim-job/',
            'http://www.youporn.com/watch/10350691/big-ass-blonde-beauty-alexis-texas-is-a-whore/',
            'http://www.youporn.com/watch/10501033/horny-redhead-faye-reagan-fucks-her-twat-with-a-toy/',
            'http://www.youporn.com/watch/10621025/do-you-have-any-extra-room-for-my-tongue-critical-x/',
            'http://www.youporn.com/watch/10684159/lesbian-sex-shower/',
            'http://www.youporn.com/watch/10221345/sperm-swap-three-way-with-two-hot-babes-and-sperm-swap/',
            'http://www.youporn.com/watch/10720537/femaleagent-sexy-agents-asshole-licked-and-her-perfect-pussy-fucked-in-doggy/',
            'http://www.youporn.com/watch/10338569/latina-pornstar-mari-possa-with-huge-natural-dd-boobs-masturbates/'))"""
