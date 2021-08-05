class AccountResult:
    def __init__(self, success=True, captcha=False, body=[]):
        self.success = success
        self.captcha = captcha
        self.body = body
