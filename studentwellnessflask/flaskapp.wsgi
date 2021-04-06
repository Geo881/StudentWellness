#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/studentwellnessflask/")

from studentwellnessflask import app as application
application.secret_key = 'studentwellness2020'
