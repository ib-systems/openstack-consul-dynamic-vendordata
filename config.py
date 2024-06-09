from oslo_config import cfg
import os, re

conf = cfg.CONF
consul_opts = [
    cfg.StrOpt("host", default="127.0.0.1", required=True),
    cfg.IntOpt("port", default=8500, required=True),
    cfg.StrOpt("dc", default=None),
    cfg.StrOpt("token", default=None)
]
consul_group = cfg.OptGroup(name="consul")

conf.register_group(consul_group)
conf.register_opts(consul_opts, consul_group)
conf(default_config_files=[os.getcwad() + "/ocdv.conf"])