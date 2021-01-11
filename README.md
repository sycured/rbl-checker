# rbl-checker

Help you to check if any IP is blacklisted

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sycured_rbl-checker&metric=alert_status)](https://sonarcloud.io/dashboard?id=sycured_rbl-checker)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=sycured_rbl-checker&metric=code_smells)](https://sonarcloud.io/dashboard?id=sycured_rbl-checker)

*Author : sycured*

*LICENSE : GNU AFFERO GENERAL PUBLIC LICENSE Version 3*

## Requirements

- Python3
- Kafka
- PostgreSQL or compatible (ex. Yugabyte)


## DB: Setup table

```sql
create table rbl (id serial primary key, date timestamptz, ip_srv text, rblname text);
```

When you have entries inside the table, it looks like:

 id |             date              |   ip_srv   |       rblname
----|-------------------------------|------------|---------------------
  1 | 2021-01-10 19:35:29.533729+00 | 95.216.0.1 | bl.emailbasura.org
  4 | 2021-01-10 19:35:46.771444+00 | 95.216.0.2 | bl.spamcannibal.org
  2 | 2021-01-10 19:35:35.716627+00 | 95.216.0.1 | bl.spamcannibal.org
  3 | 2021-01-10 19:35:45.45523+00  | 95.216.0.2 | bl.emailbasura.org
(4 rows)

## rest_api

It's where you add new range to scan. By default uvicorn listen on http://127.0.0.1:8000

The config uses environment variables and you need to look the [rest_api/config.py](rest_api/config.py)

```bash
cd rest_api && uvicorn main:app
```

### How to insert a range to test

```bash
curl -X POST "http://127.0.0.1:8000/add" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"ip_range\":\"95.216.0.0/16\"}"
````

## consumer

Check the IP and add data to the database in case of it's inside an RBL.

The config uses environment variables and you need to look at [consumer/config.py](consumer/config.py)

```bash
cd consumer && DB_USER=rbl DB_PASS=toto python3 main.py
```