import json

def save_config_to_json(config_obj, file_path: str):
    try:
        data = config_obj.to_saveable_dict()
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        return True
    except Exception as e:
        print(f"JSON Export Error: {e}")
        return False
