# Filename convention

Kartoza/postgis docker-entrypoint.sh loads the files in order. And it
is good that the filenames names:

- 00.first_file_to_load_maybe_the_structure.sql
- 01.second_file_to_load_maybe_data.sql
- 02.third_file_to_load_maybe_another_data.sql
- 03.other_file_to_load_maybe_another_data.sql
- {number}.{filename}.sql

# CAVEATS: file ".entry_point.lock"

When Kartoza/postgis docker-entrypoint.sh finish, it creates the file
".entry_point.lock". if you delete all containers and try to up,
the Kartoza/postgis docker-entrypoint.sh checks this file and will not
load the data.sql files.

When first load the data, Postgis container become autist and maybe it
does't response to external connections (from other containers or
directly psql command from host) for first minutes before the first data
load (when docker-compose up --build -d).

# Dump of the data

Execute the following commands inside the docker container:

- Structure: `pg_dump -h localhost -U <user> -C -s <database_name> > {number}.{database_name}.structure.sql`
- Data: `pg_dump -h localhost -U <user> -C -a --column-inserts <database_name> > {number}.{database_name}.data.sql`
