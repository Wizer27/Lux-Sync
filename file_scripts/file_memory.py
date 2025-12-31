import os
from pathlib import Path



def count_size(file_name:str) -> int:
    try:
        filepath = Path(file_name)
        if filepath.exists():
            if filepath.is_file():
                return int(filepath.stat().st_size)
            else:
                raise TypeError("This is not a file")
        else:
            raise KeyError("File not found")                
    except Exception as e:
        raise Exception(f"Error : {e}")
print(count_size("test.txt"))    