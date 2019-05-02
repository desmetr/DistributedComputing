#!/bin/sh

export FLASK_APP=$1
export FLASK_RUN_PORT=$2
flask run
