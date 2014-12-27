MyPleasu.re - Scraper CLI (Python)
=================================

### A Python based command line interface application, replacing Node.js, that crawls and scrapes content from websites ("providers").

---

#### 1 / Purpose

**Node.js** is famously known for not being a good choice for CPU intensive tasks. The first version of **scraper** allowed us to experience it first-hand.

This **Python** version is an attempt at circumventing the main issues we dealt with on the first iteration of the scraping tool we built, namely:

- **CPU usage**: Node versions, based on [phantom.js](https://github.com/ariya/phantomjs), then [zombie](http://zombie.labnotes.org/), then [request](https://github.com/request/request), consume way too much and are seemingly [prone to memory leaks and related issues](https://www.google.fr/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#safe=off&q=phantomjs%20memory%20leak).
- **Speed**: I have the intuition the **Python** may perform faster, and will set up execution timers for both version to find out.
- **Code readibility**: callback hell is real, even with modularized code, named functions and other precautions. It makes sharing code quite painful.

#### 2 / Settings

The app will look for an environment variable named `MYPLSR_ENV` to determine the current environement — either `dev` or `prod`.

- Set this variable on your machine (to `dev`). Ensure the production server has it set too (to `prod`).
- Create a `settings.cfg` file in `./settings/`. **This file will not be version controlled** so it can host sensitive data.
- Copy / inspire yourself from the content of `settings.example.cfg` to set the appropriate values for your configuration in `settings.cfg`.

#### 3 / Early results

As of commit `95d4e9c` (tag `0.1.0`), a _rough_ test consisting of fetching 20 different videos from Youporn (_test 1: scrape and scroll_) and trying to fetch the same 20 again right after (_test 2: get cached video documents_) provides the following results:

- 0.909 seconds, average execution time for scraping and getting **all** data for a single video (this actually includes a second fetch/scrape to get the duration of the video!)
- 0.0125 seconds, average execution time for TARS to know a video is cached in DB, and to return it.

I've left the tests in the commit, so checking it out and running `/usr/bin/time ./scraper.py` from a *nix machine will let you try it out yourself.
