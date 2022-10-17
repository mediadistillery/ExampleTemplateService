import datetime
import pathlib
import typing

from google.cloud.storage import Bucket, Client, Blob


class BlobNotFoundException(FileNotFoundError):
    pass


class GoogleStorage:
    def __init__(self, service_account_filepath: typing.Union[str, pathlib.Path] = None) -> None:
        self.client = (
            Client.from_service_account_json(service_account_filepath) if service_account_filepath else Client()
        )

    def download(
        self, bucket_name: str, blob_name: typing.Union[str, pathlib.Path], filepath: typing.Union[str, pathlib.Path]
    ) -> None:
        bucket = Bucket(self.client, name=bucket_name)
        blob = bucket.get_blob(str(blob_name))
        if blob is None:
            raise BlobNotFoundException(f"Could not find blob with name {blob_name} in bucket {bucket_name}")
        blob.download_to_filename(str(filepath))

    def upload(
        self,
        bucket_name: str,
        destination_blob_name: typing.Union[str, pathlib.Path],
        filepath: typing.Union[str, pathlib.Path],
        content_type: str = None,
    ) -> None:
        bucket = Bucket(self.client, name=bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(str(filepath), content_type=content_type)

    def list(self, bucket_name: str) -> typing.Iterator[Blob]:
        return self.client.list_blobs(bucket_name)

    def generate_download_signed_url_v4(self, bucket_name, blob_name, ttl_days=7):
        """Generates a v4 signed URL for downloading a blob.

        Note that this method requires a service account key file. You can not use
        this if you are using Application Default Credentials from Google Compute
        Engine or from the Google Cloud SDK.
        """

        bucket = Bucket(self.client, name=bucket_name)
        blob = bucket.blob(blob_name)

        url = blob.generate_signed_url(version="v4", expiration=datetime.timedelta(days=ttl_days), method="GET")

        return url
