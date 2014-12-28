MyPleasu.re - Scraper CLI (Python)
=================================

### A Python based command line interface application, replacing Node.js, that crawls and scrapes content from websites ("providers").

---

#### 1 / Installation

This is a **Python 3.4** app. I've developped it on **Python 3.4.2**.

Install **Python 3.4++** on your machine, then follow these steps to install.

- Install [`pip`](https://pip.pypa.io/en/latest/installing.html);
- Create a Python 3 based [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/): `pyvenv <ENV_DIR>` (`ENV_DIR` can be named anything);
- Activate it: `source <ENV_DIR>/bin/activate`;
- Install dependencies with `pip install -r requirements.txt`.

#### 2 / Purpose

**Node.js** is famously known for not being a good choice for CPU intensive tasks. The first version of **scraper** allowed us to experience it first-hand.

This **Python** version is an attempt at circumventing the main issues we dealt with on the first iteration of the scraping tool we built, namely:

- **CPU usage**: Node versions, based on [phantom.js](https://github.com/ariya/phantomjs), then [zombie](http://zombie.labnotes.org/), then [request](https://github.com/request/request), consume way too much and are seemingly [prone to memory leaks and related issues](https://www.google.fr/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#safe=off&q=phantomjs%20memory%20leak).
- **Speed**: I have the intuition the **Python** may perform faster, and will set up execution timers for both version to find out.
- **Code readibility**: callback hell is real, even with modularized code, named functions and other precautions. It makes sharing code quite painful.

#### 3 / Settings

The app will look for an environment variable named `MYPLSR_ENV` to determine the current environement — either `dev` or `prod`.

- Set this variable on your machine (to `dev`). Ensure the production server has it set too (to `prod`).
- Create a `settings.cfg` file in `./settings/`. **This file will not be version controlled** so it can host sensitive data.
- Copy / inspire yourself from the content of `settings.example.cfg` to set the appropriate values for your configuration in `settings.cfg`.

#### 4 / Early results

Keep in mind these tests are not set like real benchmarks should be done, and only exist for their comparitive value next to Node.js on the same setups.
For the record, I'm using a **Macbook Pro Retina Late 2012, 2,5 GHz Intel Core i5, duo-core 8 Go 1600 MHz DDR3, on OS X 10.9.5 (13F34)**.

As of commit `95d4e9c` (tag `0.1.0`), a _rough_ test consisting of fetching 20 different videos from Youporn (_test 1: scrape and scroll_) and trying to fetch the same 20 again right after (_test 2: get cached video documents_) provides the following results:

- **0.909 seconds**, average execution time for scraping and getting **all** data for a single video (this actually includes a second fetch/scrape to get the duration of the video!);
- **0.0125 seconds**, average execution time for TARS to know a video is cached in DB, and to return it.

I've left the tests in the commit, so checking it out and running `/usr/bin/time ./scraper.py` from a *nix machine will let you try it out yourself.

On commit `df38325` I set up multithreading, tailored for my machine's specs. The logs become a bit messy but the results are obviously even better:

- **0.4225**, average execution time for scraping the same data;
- **0.0185**, average execution time for fetching cached data afterwards.
