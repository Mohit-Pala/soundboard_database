from python_access.models.sound_model import SoundModel
from python_access.errors.exceptions import NotFoundError, DeleteError, CreateError
from config import SOUNDS_FILE_PATH

import pandas as pd

def read_sounds_file() -> pd.DataFrame:
    df = pd.read_csv(SOUNDS_FILE_PATH)
    return df

def get_all() -> list[SoundModel]:
    df = read_sounds_file()
    sounds = [SoundModel(**row) for index, row in df.iterrows()]
    if not sounds:
        raise NotFoundError("No sounds found")
    return sounds

def get_by_id(id: int) -> SoundModel:
    df = read_sounds_file()
    sound_row = df[df['Id'] == id]
    if sound_row.empty:
        raise NotFoundError(f"Sound with Id {id} not found")
    return SoundModel(**sound_row.iloc[0])

def delete_by_id(id: int) -> None:
    df = read_sounds_file()
    if id not in df['Id'].values:
        raise NotFoundError(f"Sound with Id {id} not found")
    df = df[df['Id'] != id]
    try:
        df.to_csv(SOUNDS_FILE_PATH, index=False)
    except Exception as e:
        raise DeleteError(f"Failed to delete sound with Id {id}: {e}")
    return None

def create(user_id: int, sound_name: str, description: str, sound_path: str, time: int) -> SoundModel:
    df = read_sounds_file()
    new_id = df['Id'].max() + 1 if not df.empty else 1
    new_sound = SoundModel(Id=new_id, UserId=user_id, SoundName=sound_name, Description=description, SoundPath=sound_path, Time=time)
    df = pd.concat([df, pd.DataFrame([new_sound.__dict__])], ignore_index=True)
    try:
        df.to_csv(SOUNDS_FILE_PATH, index=False)
    except Exception as e:
        raise CreateError(f"Failed to create sound: {e}")
    return new_sound