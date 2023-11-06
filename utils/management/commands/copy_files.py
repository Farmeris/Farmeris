from django.core.management.base import BaseCommand
import os
import shutil
from django.conf import settings


class Command(BaseCommand):
    help = 'Copy files from obrasteky folders to MEDIA_ROOT'

    def handle(self, *args, **kwargs):
        source_directory = 'obrasteky'  # Replace with the path to the source directory

        # Get the target directory (MEDIA_ROOT) from Django settings
        target_directory = settings.MEDIA_ROOT

        for root, _, files in os.walk(source_directory):
            for file in files:
                source_path = os.path.join(root, file)
                target_path = os.path.join(target_directory, os.path.relpath(source_path, source_directory))
                target_dirname = os.path.dirname(target_path)

                # Create the target directory if it doesn't exist
                os.makedirs(target_dirname, exist_ok=True)

                # Copy the file to the target directory
                shutil.copy2(source_path, target_path)

        self.stdout.write(self.style.SUCCESS('Files copied successfully'))