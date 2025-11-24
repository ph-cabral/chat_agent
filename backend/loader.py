import os
from vectordb import VectorDB
from pathlib import Path

def load_initial_data():
    vector_db = VectorDB()
    input_dir = Path("/app/data/input")
    
    if not input_dir.exists():
        print("⚠️  No hay carpeta input, saltando carga inicial")
        return
    
    for area_folder in input_dir.iterdir():
        if area_folder.is_dir():
            area_name = area_folder.name
            print(f"Procesando área: {area_name}")
            
            for file_path in area_folder.rglob("*"):
                if file_path.is_file():
                    try:
                        vector_db.add_document(
                            str(file_path), 
                            file_path.name,
                            metadata={"area": area_name}
                        )
                        print(f"  ✓ {file_path.name}")
                    except Exception as e:
                        print(f"  ✗ Error en {file_path.name}: {e}")	
