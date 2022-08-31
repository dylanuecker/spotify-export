#!/bin/bash

SRC_PATH="$(cd $(dirname $0) && pwd)/src/"

${SRC_PATH}form_user_login_get.py
if ${SRC_PATH}token_post_request.py; then
	${SRC_PATH}do_export.py y y y
fi

