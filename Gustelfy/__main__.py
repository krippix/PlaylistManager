# external
# python native
import logging
import sys
# project
from Gustelfy import app
from Gustelfy import test


if len(sys.argv) > 1:
    if sys.argv[1] == "db":
        test.db_connection()
    if sys.argv[1] == "api":
        test.api()
    else:
        test.test()
else:
    print("That doesent work yet :harold:")

