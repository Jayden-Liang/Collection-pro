# -*- coding: utf-8 -*-
bind = '0.0.0.0:5000'
accesslog = '-'    #记录到终端输出，保存日志到文件为accesslog = '/var/logs/gunicorn.access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" in %(D)sµs'
