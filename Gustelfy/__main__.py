# external
# python native
import logging
import sys
# project
from Gustelfy import app
from Gustelfy import test


if len(sys.argv) > 1:
    if sys.argv[1] == "test":
        test.test()
else:
    print("That doesent work yet :harold:")

