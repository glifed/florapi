#!/bin/bash

virtualenv venvflorapi
source venvflorapi/bin/activate
pip3 install --upgrade pip
pip3 install Flask
pip3 install py-postgresql
pip3 install gunicorn
