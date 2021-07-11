# coding=utf-8

from fastapi import APIRouter, Form, File, UploadFile

router = APIRouter()


@router.post("/thepianist/", summary="Form parameters")
def the_pianist(username: str = Form(...)):
    return {"username": username}


@router.post("/file/", summary="File parameter")
def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@router.post(
    "/uploadfile/",
    summary="File parameter with UploadFile",
    description="UploadFile uses a `spooled` file, after filesize passing the limit it will be stored in disk.",
)
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {
        "file_name": file.filename,
        "content_type": file.content_type,
        "file_size": len(content),
        "attr_file_type": str(type(file.file)),
    }


@router.post("/files/", summary="Multiple File parameters")
def create_multiple_files(files: list[bytes] = File(...)):
    return {"file_sizes": [len(i) for i in files]}


@router.post("/uploadfiles/", summary="Multiple File parameters with UploadFile")
def create_multiple_upload_files(files: list[UploadFile] = File(...)):
    return {"file_names": [i.filename for i in files]}


@router.post(
    "/thelionking/",
    summary="Request form and files",
    description="Need to declare `File` parameters before `Form` parameters!",
)
def the_lion_king(
    file1: bytes = File(...),
    file2: UploadFile = File(...),
    username: str = Form(...),
):
    return {
        "file1_size": len(file1),
        "file2_name": file2.filename,
        "username": username,
    }
