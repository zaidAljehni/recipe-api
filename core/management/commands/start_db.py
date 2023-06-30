"""
Django command to wait for the DB to be available
"""

import os
import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entry point for command."""

        # Stopping previous running database container if exist
        self.stdout.write("Stopping previous running database if exist ⏳...")
        os.system("docker stop recipe-db")

        # Starting database container
        self.stdout.write("Waiting for database ⏳...")
        os.system("docker start recipe-db")

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
