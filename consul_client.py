import consul
from config import conf

consul_client = consul.Consul(host=conf.consul.host, port=conf.consul.port, token=conf.consul.token, dc=conf.consul.dc)
