class AccountResult:
    def __init__(self, success=True, captcha=False, body=[], not_founded=False):
        self.success = success
        self.captcha = captcha
        self.body = body
        self.not_founded = not_founded
