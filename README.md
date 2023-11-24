# heimdal_api_script
Heimdal API python script for automatic log collection for ELK-Stack(SIEM), by sending the Heimdal logs to Logstash.

# Config
To run the Heimdal API script you wil need python3, the Heimdal script and a config.ini file with the Heimdal API config and the customer_ID and bearer token.
script usage
```bash
python3 heimdal_script.py conig.ini
```

Sample configuration file:

```
[HeimdalConfig]
base_url = https://dashboard.heimdalsecurity.com/api/heimdalapi/
heimdal_modules_3days = customers
heimdal_modules_15minutes = darklayerguard,vectorn,vigilancedetections,encryptiondetection,threatPreventionNetwork
heimdal_modules_1hours = activeclients,thirdparty,microsoftupdates,xtp
logstash_url = http://logstash-url:logstash-port/heimdal

[CustomerGroupData1]
customer_id = 123456
bearer_token = Bearer N0TR3ALB3ARB3RT0KEN1234567891234
customer_group = customer_group_name

[CustomerGroupData2]
customer_id = 234567
bearer_token = Bearer N0TR3ALB3ARB3RT0KEN2345678912345
customer_group = customer_group_name2
```
