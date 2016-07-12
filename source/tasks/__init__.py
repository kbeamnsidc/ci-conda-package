from invoke import Collection

from . import test
from . import version
from . import build
from . import deploy
from . import clean

ns = Collection()
ns.add_collection(test)
ns.add_collection(version)
ns.add_collection(build)
ns.add_collection(deploy)
ns.add_collection(clean)
