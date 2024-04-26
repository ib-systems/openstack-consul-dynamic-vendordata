# OpenStack dynamic vendordata consul provider

This component looks into Consul's KV in order to fetch instance vendor-data that could be used as generic #cloud-config applied to all instances without using user-data

# ⚠️ Depends on [vendor data blueprint](https://blueprints.launchpad.net/nova/+spec/dynamicjson-vendordata-cloud-config)

Following this [bug](https://bugs.launchpad.net/cloud-init/+bug/1841104) cloud-init expect vendor_data2.json to contain "cloud-init" key to apply vendor specific #cloud-config. Current vendor data implementation expect it to [be as JSON complaint](https://docs.openstack.org/nova/latest/admin/vendordata.html#dynamicjson). Blueprint will allow to use specific vendor data service like `cloud-init@10.10.10.10:8000/ocdv` to pass `cloud-init` key as plain text instead of JSON. Probably we might have specific route like `/cloud-init` to return text/plain content stored in Consul KV by path to let cloud-init initialize vendor's `cloud-config`
```py
f"cloud/instances/{instance_id}/cloud-init"
```
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
