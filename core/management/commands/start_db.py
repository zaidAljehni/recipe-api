"""
Django command to start the database
"""

import os
import time

import environ
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    """Django command to start the database."""

    def handle(self, *args, **options):
        """Entry point for command."""

        env = environ.Env()
        db_container_id = env("DB_CONTAINER_ID")

        # Stopping previous running database container if exist
        self.stdout.write("Stopping previous running database if exist ⏳...")
        os.system("docker stop {db_container_id}".format(db_container_id=db_container_id))

        # Starting database container
        self.stdout.write("Waiting for database ⏳...")
        os.system("docker start {db_container_id}".format(db_container_id=db_container_id))

        # Checking database connection
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
