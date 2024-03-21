import os
from fastapi import UploadFile, File

async def save_uploaded_file(user_name: str, file: UploadFile = File(...)):
    # Определяем путь к папке пользователя
    user_folder_path = os.path.join("user_folders", user_name)
    
    # Создаем папку пользователя, если её ещё нет
    if not os.path.exists(user_folder_path):
        os.makedirs(user_folder_path)
    
    # Сохраняем файл в папку пользователя
    file_path = os.path.join(user_folder_path, file.filename)
    with open(file_path, "wb") as buffer:
        while True:
            chunk = await file.read(8192) # Читаем файл по частям
            if not chunk:
                break
            buffer.write(chunk)
    
    return {"filename": file.filename, "user_folder": user_folder_path}