# Purpose

Exports SQL for backup and for db data-and-structure migration.

For now just updates an sql-repo; eventually may also update a docker-data repo.

---

# Usage

```
$ cd /path/to/sqlexport_stuff/sr_sql_exports/
$ source ../source_first.sh  # activates the venv and loads envars
$ python3 ./run_exports.py
```

---

# Flag info...

`--events`

_(chatgpt4)_ This flag includes the events for the dumped databases in the output. Events in MySQL are tasks that are scheduled to run at a specific time or at regular intervals. They are part of the MySQL Event Scheduler, a feature that allows you to automate the execution of SQL queries based on a schedule. By default, mysqldump does not include events in the backup. When you use the --events option, it ensures that the events are also backed up along with the database tables, data, and other objects.

`--routines`

_(chatgpt4)_ This flag includes stored routines (both stored procedures and stored functions) in the output. Stored routines are a set of SQL statements that have been saved and can be executed as a unit. They are used to encapsulate complex operations into a single callable routine, making it easier to manage and reuse code. Like events, stored routines are not included in the mysqldump output by default. Using the --routines option ensures that these objects are included in the backup, allowing for a more comprehensive restoration of the database state.

_(chatgpt4)_ Notes about including `--events` and `--routines` in a mysqldump command... 

While including --events and --routines in your mysqldump command can be very useful for ensuring a complete backup of your database, including all its functionalities, there are a couple of considerations to keep in mind:

- Security and Privacy: If the routines or events contain sensitive logic or information, including them in a dump could potentially expose this information if the backup is not securely stored.
- Portability: In some cases, if you're moving to a database system that doesn't support these features in the same way, including events and routines might necessitate additional adjustments during restoration or migration.

However, these considerations are generally outweighed by the benefits of having a complete backup that includes all database objects and logic for most use cases, especially for purposes of disaster recovery, cloning environments, or migrating databases.

`--skip-extended-insert`

This is the main difference between the two files produced. When this flag is ommitted, many thousands of insert commands can be on one line, making export and some kinds of imports much faster (and the dump is smaller). When this flag is present, each insert is on a single line. The reasons one of the files uses this flag: 

- It makes it possible to review the changes to the db via a diff with the previous version.
- The script we use to make sqlite tables for local-development cannot handle too many inserts on one line. 

---