#!/bin/bash

src/form_user_login_get.py
if src/token_post_request.py; then
	src/do_export.py y y y
fi

