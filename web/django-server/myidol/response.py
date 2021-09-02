class AppResponse:
    def __init__(self):
        self.app = 'myidol'
        self.page = 'myidol'
        self.css = 'myidol'
        self.chain_page = 'myidol'
        self.next_point = 'process'
        
class MyResponse(AppResponse):
    def __init__(self):
        super().__init__()
        
class ProcessResponse(AppResponse):
    def __init__(self):
        super().__init__()
        self.page = 'process'
        self.css = 'process'
        self.chain_page = 'process'
        self.next_point = 'result'

class ResultReponse(AppResponse):
    def __init__(self):
        super().__init__()
        self.css = 'result'
