#!/bin/sh

coverage run --source='.' manage.py test api
coverage report
