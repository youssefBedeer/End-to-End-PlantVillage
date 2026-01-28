from fastapi import UploadFile, HTTPException 

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/jpg"}
MAX_FILE_SIZE = 5 * 1024 * 1024 # 5MB


async def validate_image_file(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES: raise(
        HTTPException(
            status_code=400,
            detail="Only JPEG and PNG images are allowed"
        )
    )

    content = await file.read() 

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
        status_code=400,
        detail="Image size exceeds 5MB"
        )
    
    return content