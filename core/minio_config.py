import json

from miniopy_async import Minio

from config import get_settings

settings = get_settings()

minio_client = Minio(
    endpoint=settings.MINIO_HOST,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    secure=settings.MINIO_USE_HTTPS,
)


async def init_minio():
    exist = await minio_client.bucket_exists(settings.MINIO_BUCKET_NAME)
    if not exist:
        await minio_client.make_bucket(settings.MINIO_BUCKET_NAME, location="")

        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": ["s3:GetObject"],
                    "Resource": ["arn:aws:s3:::media/*"],
                }
            ],
        }

        await minio_client.set_bucket_policy(
            settings.MINIO_BUCKET_NAME, json.dumps(policy)
        )

        print("Minio bucket created")
