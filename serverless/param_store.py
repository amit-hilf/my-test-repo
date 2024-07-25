import typing

class MockParamStore:
    def __init__(
        self,
    ):
        self.config = {}

    def set_param(
        self, 
        key: str,
        value: typing.Any,
    ) -> None:
        self.config[key] = value

    def get_param(
        self, 
        key: str,
    ) -> typing.Any:
        return self.config.get(key, None)