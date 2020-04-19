from flask import request  # 滙入 request


def show_cookies():
    return request.cookies
