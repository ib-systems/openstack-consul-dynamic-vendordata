# OpenStack dynamic vendordata consul provider

This component looks into Consul's KV in order to fetch instance vendor-data that could be used as generic #cloud-config applied to all instances without using user-data

## TODO

- [ ] Use only fastapi *
- [ ] Add routes to handle upsert/delete instance vendor-data using instance-id

\* at this moment no way found to use keystonemiddleware with fastapi  so basic Flask app used as sub-app

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

Send POST request with JSON contains "instance-id" field. In case Consul KV have a key following path `f"cloud/instances/{instance_id}/vendor-data"` response will be returned as application/json.

⚠️ vendor-data have to be [json-compliant format](https://docs.openstack.org/nova/latest/user/metadata.html#metadata-vendordata)