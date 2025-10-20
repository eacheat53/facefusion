import sys
from functools import partial

import facefusion.exit_helper

facefusion.exit_helper.fatal_exit = partial(sys.exit)
