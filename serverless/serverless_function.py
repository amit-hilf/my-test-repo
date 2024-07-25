import typing

class MockServerlessFunction:
    def __init__(
        self,
        name: str, 
        func: typing.Callable,
    ):
        self.name = name
        self.func = func

    def invoke(
        self,
    ) -> None:
        try:
            print(f"Invoking {self.name}")
            self.func()
        except:
            print('An exception Occured During Execution')
        else:
            print('Function executed successfully')
