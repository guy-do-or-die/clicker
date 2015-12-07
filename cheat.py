from selenium import webdriver
from stem.control import Controller
from stem import Signal

import multiprocessing
import random
import signal
import time
import sys


def reconn():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


def inst(_id):
    try:
        opts = webdriver.ChromeOptions()
        opts.add_argument('--proxy-server=http://127.0.0.1:8118')
        driver = webdriver.Chrome(chrome_options=opts)
    except Exception as e:
        print _id, e

    def handler(*args):
        driver.quit()
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    signal.signal(signal.SIGINT, handler)

    def scroll():
        h = lambda: driver.execute_script('return document.body.scrollHeight')
        prev = h()
        new = prev + 1
        while new > prev:
            driver.execute_script('window.scrollTo(0, 100000)')
            time.sleep(.5)
            prev = new
            new = h()

    def fire():
        reconn()
        driver.get('http://soundcloud.com/rosemary_loves_a_blackberry')
        time.sleep(3)
        scroll()

        els = driver.find_elements_by_class_name('sc-button-play')
        while len(els) > 0:
            el = random.choice(els)
            driver.execute_script('window.scrollTo(0, {0!s})'.format((el.location['y'] - 200)))
            el.click()
            time.sleep(7)
            els.remove(el)

    errs = 0
    while 1:
        try:
            fire()
        except Exception as e:
            print _id, e

try:
    num = int(sys.argv[1])
except:
    num = 1

pool = multiprocessing.Pool(num)

try:
    pool.map_async(inst, xrange(num))
    pool.close()
    pool.join()
except KeyboardInterrupt:
    pool.terminate()
