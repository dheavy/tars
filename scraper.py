#!/usr/bin/env python

import os
import argparse
from mypleasure.tars import Tars

def parse_args():
  """Parse argument passed in CLI

  Returns:
    The tuple of arguments (url, id, requester, workers) passed in CLI.
  """
  parser = argparse.ArgumentParser(description='Crawls and scrapes content from websites ("providers").')
  parser.add_argument('--url', type=str, help='url to crawl and scrape')
  parser.add_argument('--id', type=int, help='job id in queue')
  parser.add_argument('--requester', type=int, help='user id')
  parser.add_argument('--workers', type=int, default=8, help='number of workers to use, 8 by default')
  return parser.parse_args()

if __name__ == '__main__':
  options = parse_args()
  tars = Tars()
  result = tars.send_on_mission('http://www.youporn.com/watch/9438103/victoria-rae-black-in-the-bedroom/?from=vbwn')
