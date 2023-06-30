"""
Django command to drop the database
"""

import os

import environ
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to drop the database."""

    def handle(self, *args, **options):
        """Entry point for command."""
        env = environ.Env()
        db_container_id = env("DB_CONTAINER_ID")

        # Stopping & removing previous running database container if exist
        self.stdout.write("Stopping previous running database if exist ⏳...")
        os.system(
            "docker stop {db_container_id} && docker rm {db_container_id}"
            .format(db_container_id=db_container_id)
        )
