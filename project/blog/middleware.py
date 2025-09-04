import time


class response_time:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start
        print(f"\033[32m Response time = {duration:.2f} secs\033[0m")
        return response
