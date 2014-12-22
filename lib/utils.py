#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: utils.py
# Date: Mon Dec 22 23:24:02 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import sys
import time

def ensure_bin_str(s):
    if type(s) == str:
        return s
    if type(s) == unicode:
        return s.encode('utf-8')

def ensure_unicode(s):
    if type(s) == str:
        return s.decode('utf-8')
    if type(s) == unicode:
        return s

class ProgressReporter(object):
    """report progress of long-term jobs"""
    _start_time = None
    _prev_report_time = 0
    _cnt = 0
    _name = None
    _total = None

    def __init__(self, name, total=0, fout=sys.stderr):
        self._start_time = time.time()
        self._name = name
        self._total = int(total)
        self._fout = fout

    @property
    def total_time(self):
        return time.time() - self._start_time

    def trigger(self, delta=1, extra_msg='', target_cnt=None):
        if target_cnt is None:
            self._cnt += int(delta)
        else:
            self._cnt = int(target_cnt)
        now = time.time()
        if now - self._prev_report_time < 0.5:
            return
        self._prev_report_time = now
        dt = now - self._start_time
        if self._total and self._cnt > 0:
            eta_msg = '{}/{} ETA: {:.2f}'.format(self._cnt, self._total,
                    (self._total-self._cnt)*dt/self._cnt)
        else:
            eta_msg = '{} done'.format(self._cnt)
        self._fout.write(u'{}: avg {:.3f}/sec'
                         u', passed {:.3f}sec, {}  {} \r'.format(
            self._name, self._cnt / dt, dt, eta_msg, extra_msg))
        self._fout.flush()

    def finish(self):
        """:return: total time"""
        self._fout.write('\n')
        self._fout.flush()
        return self.total_time
