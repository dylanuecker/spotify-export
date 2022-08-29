#!/bin/bash

./form_user_login_get.py
if ./token_post_request.py; then
	./do_export.py y y y
fi

