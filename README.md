# OpenStack dynamic vendordata consul provider

This component looks into Consul's KV in order to fetch instance vendor-data that could be used as generic #cloud-config applied to all instances without using user-data

## TODO

- [ ] Use only fastapi *;
- [ ] Add routes to handle upsert/delete instance vendor-data using instance-id;
- [x] Set up specific route especially for `cloud-init` to provide simple way to return plain #cloud-config in response stored in specific key;

\* at this moment no way found to use keystonemiddleware with fastapi so basic Flask app used as sub-app

# evaluation
<sup>not ready for production usage at this moment</sup>

Set up `ocdv.conf` with your credentials

Install deps
```
pip install -r requirements.txt
```

Start server
```
python main.py
```
# running in docker
1. Build docker image `docker build -t ocdv .` or `docker-compose build`
2. Run manually
```
docker run -it -p 8000:8000 --rm --mount type=bind,source="$(pwd)"/ocdv.conf,target=/home/ocdv/ocdv.conf,readonly ocdv
```
or use compose
```
docker-compose up
```
3. Set up your nova-api to use DynamicJSON provider
```
[api]
vendordata_providers = DynamicJSON
vendordata_dynamic_targets = 'cloud-init@http://10.10.10.10:8000/ocdv/cloud-init'
```
Here first `cloud-init` stands for vendor data key. cloud-init expect this to process `#cloud-config` provided by vendor_data2.json. Last cloud-init is url path that returns cloud-config stored in Consul KV by path `f"cloud/instances/{instance_id}/cloud-config`

Send POST request with JSON contains "instance-id" field. In case Consul KV have a key following path `f"cloud/instances/{instance_id}/vendor-data"` response will be returned as application/json.

⚠️ vendor-data have to be [json-compliant format](https://docs.openstack.org/nova/latest/user/metadata.html#metadata-vendordata);
Send POST request with JSON contains "instance-id" field to /cloud-config. In case Consul KV have a key following path `f"cloud/instances/{instance_id}/cloud-config"` response cloud-config will return.
⚠️ cloud-init have to be provided as yaml string which converts to JSON string (counts as valid JSON);
