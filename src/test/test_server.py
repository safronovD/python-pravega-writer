import sys

sys.path.append("./src/server/core")

from json import loads

from util import id_generator


class TestClassUtil:
    def test_id_length(self):
        x = id_generator(size=5)
        assert len(x) == 5

    def test_id_content(self):
        x = id_generator()
        assert x.isalnum()
