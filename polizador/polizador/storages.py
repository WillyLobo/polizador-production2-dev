from storages.backends.gcloud import GoogleCloudStorage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class GCloudAndLocalStorage(GoogleCloudStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

    def _save(self, name, content):
        # Save to Google Cloud first
        cloud_bucket_name = super()._save(name, content)

        # Reset content stream for local save
        content.seek(0) 

        # Check if file exist in local storage
        if self.local_storage.exists(name):
            # Delete file from local storage
            self.local_storage.delete(name)

        # Save to local storage
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        self.local_storage._save(name, content)

        return cloud_bucket_name