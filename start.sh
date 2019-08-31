#!/bin/bash
cd /opt/florapi
source venvflorapi/bin/activate
gunicorn --bind 0.0.0.0:5000 wsgi:app 
