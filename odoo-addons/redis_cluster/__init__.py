# -*- coding: utf-8 -*-
from odoo.tools.func import lazy_property
from odoo.tools import config as openerp_config
from odoo import http
from odoo.http import Root as OdooRoot
from odoo.http import OpenERPSession

from werkzeug.contrib.sessions import SessionStore

import cPickle
import logging
from rediscluster import StrictRedisCluster

ONE_WEEK_IN_SECONDS = 60*60*24*7

logger = logging.getLogger(__name__)


class RedisClusterSessionStore(SessionStore):
    def __init__(self, rediscluster, salt, *args, **kwargs):
        self.rediscluster = rediscluster
        self.generate_salt = salt
        self.key_template = 'session:%s'

        super(RedisClusterSessionStore, self).__init__(*args, **kwargs)

    def new(self):
        return self.session_class({}, self.generate_key(self.generate_salt), True)

    def get_session_key(self, sid):
        if isinstance(sid, unicode):
            sid = sid.encode('utf-8')

        return self.key_template % sid

    def save(self, session):
        data = cPickle.dumps(dict(session))
        key = self.get_session_key(session.sid)
        try:
            # return self.rediscluster.setex(key, data, ONE_WEEK_IN_SECONDS)
            return self.rediscluster.set(key, data)
        except Exception as ex:
            logger.error("Error on setting session data", exc_info = ex)

    def delete(self, session):
        try:
            key = self.get_session_key(session.sid)
            return self.rediscluster.delete(key)
        except Exception as ex:
            logger.error("Error on deleting session data", exc_info = ex)

    def get(self, sid):
        if not self.is_valid_key(sid):
            return self.new()
        
        key = self.get_session_key(sid)
        try:
            saved = self.rediscluster.get(key)
            data = cPickle.loads(saved.encode('utf-8')) if saved else {}
        except Exception as ex:
            logger.error("Error on getting session data", exc_info = ex)
            data = {}
        return self.session_class(data, sid, False)


use_redis_cluster   = openerp_config.get('use_redis_cluster', False)

logger.debug("Enable Redis Cluster : {}".format(use_redis_cluster))

if use_redis_cluster:
    redis_cluster_host  = openerp_config.get('redis_cluster_host', 'localhost')
    redis_cluster_port  = openerp_config.get('redis_cluster_port', 6379)
    redis_cluster_master_password = openerp_config.get('redis_cluster_master_password', "")
    redis_cluster_salt  = openerp_config.get(
                    'redis_cluster_salt',
                    '-RMsSz~]3}4[Bu3_aEFx.5[57O^vH?`{X4R)Y3<Grvq6E:L?6#aoA@|/^^ky@%TI'
                    )

    logger.debug("Connecting Redis Cluster at {}:{}".format(redis_cluster_host, redis_cluster_port))

    # TODO: connection pool option
    startup_nodes = [{"host": redis_cluster_host, "port": redis_cluster_port}]
    redis_cluster_instance = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True, password=redis_cluster_master_password)

    class Root(OdooRoot):
        @lazy_property
        def session_store(self):
            return RedisClusterSessionStore(
                    redis_cluster_instance,
                    redis_cluster_salt,
                    session_class=OpenERPSession)


    http.root = Root()

    # we do nothing for session_gc
    def redis_cluster_session_gc(session_store):
        pass

    http.session_gc = redis_cluster_session_gc
