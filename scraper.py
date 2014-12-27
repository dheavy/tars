#!/usr/bin/env python

import os
import argparse
from mypleasure.tars import Tars
from configparser import ConfigParser

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
  tars = Tars()
  tars.send_on_mission('http://www.youporn.com/watch/9565375/lesbea-busty-lesbian-has-g-spot-orgasm-during-soapy-romp-in-the-bath-tub/?from=vbwn')
  tars.send_on_mission('http://www.youporn.com/watch/9627203/a-class-in-sexercise/?from=vbwn')
  tars.send_on_mission('http://www.youporn.com/watch/10717535/mrs-santa-gets-a-cream-pie-for-xxxmas/')
  tars.send_on_mission('http://www.youporn.com/watch/9082257/like-my-naughty-miss-santa-outfit-now-watch-me-suck-and-fuck-you-in-it/')
  tars.send_on_mission('http://www.youporn.com/watch/10781107/porn-films-3d-explicit-dildo-gymnastics/')
  tars.send_on_mission('http://www.youporn.com/watch/10356485/doubleviewcasting-mila-regular/')
  tars.send_on_mission('http://www.youporn.com/watch/8395983/lone-cock-rider-playvision/')
  tars.send_on_mission('http://www.youporn.com/watch/10778551/rachel-loves-to-please/')
  tars.send_on_mission('http://www.youporn.com/watch/10774689/love-creampie-exotic-busty-beauty-needs-two-men-to-satisfy-her/')
  tars.send_on_mission('http://www.youporn.com/watch/9442047/her-pussy-gets-very-creamy-masturbating-in-gym/')
  tars.send_on_mission('http://www.youporn.com/watch/10314337/evilangel-sheena-shaw-s-anal-insertion-and-rim-job/')
  tars.send_on_mission('http://www.youporn.com/watch/10350691/big-ass-blonde-beauty-alexis-texas-is-a-whore/')
  tars.send_on_mission('http://www.youporn.com/watch/10501033/horny-redhead-faye-reagan-fucks-her-twat-with-a-toy/')
  tars.send_on_mission('http://www.youporn.com/watch/10621025/do-you-have-any-extra-room-for-my-tongue-critical-x/')
  tars.send_on_mission('http://www.youporn.com/watch/10684159/lesbian-sex-shower/')
  tars.send_on_mission('http://www.youporn.com/watch/10221345/sperm-swap-three-way-with-two-hot-babes-and-sperm-swap/')
  tars.send_on_mission('http://www.youporn.com/watch/10720537/femaleagent-sexy-agents-asshole-licked-and-her-perfect-pussy-fucked-in-doggy/')
  tars.send_on_mission('http://www.youporn.com/watch/10338569/latina-pornstar-mari-possa-with-huge-natural-dd-boobs-masturbates/')
