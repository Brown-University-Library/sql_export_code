# Purpose

Exports SQL for backup and for db data-and-structure migration.

For now just updates an sql-repo; eventually will also update a docker-data repo.

---

# Usage

```
$ cd /path/to/sqlexport_stuff/sr_sql_exports/
$ source /path/to/env/bin/activate      # to activate the venv
$ source /path/to/sql_settings_env.sh   # to set the env vars
$ python3 ./main.py
```

---