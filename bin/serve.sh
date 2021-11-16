#!/bin/bash
source `dirname $0`/env.sh

export FLASK_APP=$BASE_DIR/app
export FLASK_ENV=development
flask run
