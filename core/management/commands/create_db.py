"""Django command to create the database."""

import os
import time

import environ
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    """Django command to create the database."""

    def handle(self, *args, **options):
        """Entry point for command."""

        env = environ.Env()
        db_container_id = env("DB_CONTAINER_ID")
        db_connection_user = env("DB_USER")
        db_connection_port = env("DB_PORT")
        db_connection_password = env("DB_PASSWORD")
        db_name = env("DB_NAME")

        # Stopping & removing previous running database container if exist
        self.stdout.write("Stopping previous running database if exist ⏳...")
        os.system(
            "docker stop {db_container_id} && docker rm {db_container_id}"
            .format(db_container_id=db_container_id)
        )

        # Creating database container
        self.stdout.write("Creating a database container ⏳...")
        command = "docker run --name {db_container_id}" \
                  " -e POSTGRES_PASSWORD={db_connection_password}" \
                  " -p {db_connection_port}:{db_connection_port} -d postgres" \
            .format(
                db_container_id=db_container_id,
                db_connection_password=db_connection_password,
                db_connection_port=db_connection_port
            )
        os.system(command)

        # checking database connection
        # TODO: find a better way to check connection
        self.stdout.write("checking connection ⏳...")
        is_db_up = False
        while is_db_up is False:
            try:
                self.check(databases=["default"])
                self.stdout.write("Connection established ✅")
                is_db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Connection failed ❌, re-trying in 1 second...")
                time.sleep(1)
        self.stdout.write("Connection available! ✅")

        self.stdout.write("Creating the database...")
        time.sleep(5)
        os.system(
            "docker exec -it {db_container_id} sh -c " \
            "\"psql -U {db_connection_user} -c 'CREATE DATABASE {db_name}'\""
            .format(
                db_container_id=db_container_id,
                db_connection_user=db_connection_user,
                db_name=db_name
            )
        )
        self.stdout.write("Database created! ✅")
