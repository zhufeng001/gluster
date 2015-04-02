

import gluster.swift.common.constraints

from swift.direr import server
from gluster.swift.common.DiskDirer import DiskDirer


class DirerController(server.DirerController):
    def _get_direr_broker(self, drive, part, account, container,direr):
        
        return DiskDirer(self.root, drive, account, container, direr,self.logger)


def app_factory(global_conf, **local_conf):
    """paste.deploy app factory for creating WSGI container server apps."""
    conf = global_conf.copy()
    conf.update(local_conf)
    return DirerController(conf)
