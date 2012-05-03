from AccessControl import ModuleSecurityInfo
from AccessControl import allow_class

utils_security = ModuleSecurityInfo('gs.skin.ogn.edem.utils')
utils_security.declarePublic('fn_to_nickname')

