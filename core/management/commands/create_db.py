"""
Django command to create a database
"""

import os
import time

import environ
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    """Django command to create a database."""

    def handle(self, *args, **options):
        """Entry point for command."""
        env = environ.Env()

        # Stopping & removing previous running database container if exist
        command = "docker stop recipe-db && docker rm recipe-db"
        self.stdout.write("Stopping previous running database if exist ⏳...")
        os.system(command)

        # Creating database container
        self.stdout.write("Creating a database ⏳...")
        command = "docker run --name recipe-db -e POSTGRES_PASSWORD={password} -p {port}:{port} -d postgres" \
            .format(password=env("DB_PASSWORD"), port=env("DB_PORT"))
        os.system(command)

        # checking database connection
        self.stdout.write("checking database ⏳...")
        is_db_up = False
        while is_db_up is False:
            try:
                self.check(databases=["default"])
                self.stdout.write("DB checked ✅")
                is_db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavailable ❌, waiting 1 second...")
                time.sleep(1)
        self.stdout.write("Database available! ✅")
