"""
S3 storage utilities for Django SaaS Starter.

Provides helper functions for interacting with AWS S3, including:
- Cached S3 client management
- Batch deletion of S3 objects with prefix matching
"""
import boto3
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

_cached_s3_client = None


def get_s3_client():
    """
    Get or create a cached S3 client.

    Uses singleton pattern to avoid creating multiple clients, which improves
    performance by reusing connections.

    Returns:
        boto3.client: S3 client instance configured with settings

    Example:
        >>> s3 = get_s3_client()
        >>> s3.list_objects_v2(Bucket='my-bucket', Prefix='uploads/')
    """
    global _cached_s3_client
    if _cached_s3_client is None:
        _cached_s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
    return _cached_s3_client


def delete_s3_objects(prefix=None):
    """
    Delete S3 objects with the given prefix.

    Handles pagination automatically for large numbers of objects.
    Requires a prefix to prevent accidental deletion of all objects.

    Args:
        prefix (str): The S3 key prefix to match (e.g., 'users/123/uploads/')
                     Required to prevent accidental deletion of all objects.

    Returns:
        bool: True if objects were deleted successfully, False otherwise

    Example:
        >>> delete_s3_objects('users/abc-123/uploads/')
        INFO: Deleted 42 objects with prefix: users/abc-123/uploads/
        True
    """
    if not prefix:
        logger.warning("No prefix provided for S3 object deletion")
        return False  # Require a prefix to avoid accidental deletion

    try:
        s3_client = get_s3_client()
        deleted_count = 0

        # List objects with the given prefix
        logger.info(f"Listing S3 objects with prefix: {prefix}")
        objects = s3_client.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Prefix=prefix
        )

        # If there are no objects, return early
        if 'Contents' not in objects:
            logger.info(f"No objects found with prefix: {prefix}")
            return True

        # Delete objects in batches
        while True:
            if 'Contents' in objects:
                delete_keys = {
                    'Objects': [{'Key': obj['Key']} for obj in objects['Contents']]
                }

                if delete_keys['Objects']:
                    deleted_count += len(delete_keys['Objects'])
                    logger.info(f"Deleting {len(delete_keys['Objects'])} objects from S3")
                    s3_client.delete_objects(
                        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                        Delete=delete_keys
                    )

            # Check if there are more objects to process
            if not objects.get('IsTruncated', False):
                break

            # Get next batch
            objects = s3_client.list_objects_v2(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Prefix=prefix,
                ContinuationToken=objects['NextContinuationToken']
            )

        logger.info(f"Successfully deleted {deleted_count} objects with prefix: {prefix}")
        return True

    except Exception as e:
        logger.error(f"Error deleting S3 objects with prefix '{prefix}': {str(e)}")
        return False
