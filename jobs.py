# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 11:43:32 2017

@author: BOUEHNNI
"""

from crontab import CronTab
file_cron = CronTab(tabfile='filename.tab')
job  = file_cron.new(command='python Services/DiseaseForcasting.py')
job.hour.every(4)
job.enable(False)
list = file_cron.find_command('python Services/DiseaseForcasting.py')
