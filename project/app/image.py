from typing import List
import uuid
from project.config import AWS_S3_BUCKET_NAME
from fastapi import APIRouter, status, UploadFile, File, HTTPException

from project.core.models.S3 import s3_connection

s3 = s3_connection()
import torch
from project.core.schemas.image import ContentDTO
from diffusers import StableDiffusionPipeline
from googletrans import Translator

translator = Translator()
model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda"

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16")
pipe = pipe.to(device)

router = APIRouter()


@router.get("/profile", status_code=status.HTTP_201_CREATED)
async def gen_profile():
    pipe("Rabbit").images[0].save("/home/modeep1/Programing/kiwi/softwave/daliy-boram-fastapi/project/images/profile/0.png")
    a = []
    name = str(uuid.uuid4())
    s3.upload_file(
        "/home/modeep1/Programing/kiwi/softwave/daliy-boram-fastapi/project/images/profile/0.png",
        AWS_S3_BUCKET_NAME,
        name,
        ExtraArgs={
            "ACL": "public-read",
            'ContentType': 'image/png'
        }
    )
    return f"https://s3.ap-northeast-2.amazonaws.com/softwave/{name}"

@router.get("/thumb", status_code=status.HTTP_201_CREATED)
async def gen_thumb(content: str):
    content = translator.translate(content, src='ko', dest='en').text
    a = []
    for i in range(9):
        pipe(content).images[0].save("/home/modeep1/Programing/kiwi/softwave/daliy-boram-fastapi/project/images/thumb/0.png")
        name = str(uuid.uuid4())
        s3.upload_file(
            "/home/modeep1/Programing/kiwi/softwave/daliy-boram-fastapi/project/images/thumb/0.png",
            AWS_S3_BUCKET_NAME,
            name,
            ExtraArgs={
                "ACL": "public-read",
                'ContentType': 'image/png'
            }
        )
        print(i)
        a.append(f"https://s3.ap-northeast-2.amazonaws.com/softwave/{name}")
    #위에거 저장해주세요 S3에.
    return a

@router.get("/character", status_code=status.HTTP_201_CREATED)
async def gen_character(content: str):
    a=[]
    content = translator.translate(content, src='ko', dest='en').text
    for i in range(9):
        pipe(content).images[0].save(f"/home/modeep1/Programing/kiwi/softwave/daliy-boram-fastapi/project/images/character/0.png")
        name = str(uuid.uuid4())
        s3.upload_file(
            "/home/modeep1/Programing/kiwi/softwave/daliy-boram-fastapi/project/images/character/0.png",
            AWS_S3_BUCKET_NAME,
            name,
            ExtraArgs={
                "ACL": "public-read",
                'ContentType': 'image/png'
            }
        )
        a.append(f"https://s3.ap-northeast-2.amazonaws.com/softwave/{name}")
        # 위에거 저장해주세요 S3에.
    return a

@router.get("/", status_code=status.HTTP_201_CREATED)
async def save_images(files: List[UploadFile]):
    a = []
    for i in files:
        name = str(uuid.uuid4())
        try:
            s3.upload_fileobj(
                i.file,
                AWS_S3_BUCKET_NAME,
                name,
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": i.content_type
                }
            )

            a.append(f"https://s3.ap-northeast-2.amazonaws.com/softwave/{name}")

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {
        "url": a
    }