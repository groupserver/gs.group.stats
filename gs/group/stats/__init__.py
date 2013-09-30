# -*- coding: utf-8 -*-
# TODO: Figure out why the following is HERE
from AccessControl import ModuleSecurityInfo

utils_security = ModuleSecurityInfo('gs.skin.ogn.edem.utils')
utils_security.declarePublic('fn_to_nickname')
