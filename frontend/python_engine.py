import os
import csv
from itertools import islice
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QThread, Signal

# Top-level function so it can be picked up by worker threads efficiently
def process_chunk(args):
    chunk, x_idx, y_idx, window_size = args
    
    x_out = []
    y_out = []
    
    # Local method references for faster execution in loops
    x_app = x_out.append
    y_app = y_out.append
    x_ext = x_out.extend
    y_ext = y_out.extend
    
    count = 0
    is_first = True
    min_x = max_x = min_y = max_y = 0.0
    
    if window_size <= 1:
        for row in chunk:
            try:
                x_app(float(row[x_idx]))
                y_app(float(row[y_idx]))
            except (ValueError, IndexError):
                pass
        return x_out, y_out

    for row in chunk:
        try:
            x_val = float(row[x_idx])
            y_val = float(row[y_idx])
        except (ValueError, IndexError):
            continue
            
        if is_first:
            min_x = max_x = x_val
            min_y = max_y = y_val
            is_first = False
        else:
            if y_val < min_y:
                min_y = y_val
                min_x = x_val
            if y_val > max_y:
                max_y = y_val
                max_x = x_val
                
        count += 1
        
        if count == window_size:
            if min_x < max_x:
                x_ext((min_x, max_x))
                y_ext((min_y, max_y))
            elif min_x > max_x:
                x_ext((max_x, min_x))
                y_ext((max_y, min_y))
            else:
                x_app(min_x)
                y_app(min_y)
            count = 0
            is_first = True
            
    if count > 0 and not is_first:
        if min_x < max_x:
            x_ext((min_x, max_x))
            y_ext((min_y, max_y))
        else:
            x_app(min_x)
            y_app(min_y)
            
    return x_out, y_out

class PurePythonStreamer(QThread):
    finished_parsing = Signal(list, list)
    error_occurred = Signal(str)

    def __init__(self, file_path, x_col_name, y_col_name):
        super().__init__()
        self.file_path = file_path
        self.x_col_name = x_col_name
        self.y_col_name = y_col_name
        self.chunk_size = 50000

    def run(self):
        try:
            file_size = os.path.getsize(self.file_path)
            # Rough estimation: ~30 bytes per row
            estimated_rows = file_size // 30
            # Target 4000 points for the UI to keep Matplotlib responsive
            window_size = max(1, estimated_rows // 4000)
            
            x_final = []
            y_final = []

            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                
                if self.x_col_name not in headers or self.y_col_name not in headers:
                    raise ValueError("Columns not found in CSV")
                    
                x_idx = headers.index(self.x_col_name)
                y_idx = headers.index(self.y_col_name)

                # Generator to yield chunks without loading the whole file into RAM
                def batch_generator():
                    while True:
                        batch = list(islice(reader, self.chunk_size))
                        if not batch:
                            break
                        yield (batch, x_idx, y_idx, window_size)

                # Use all available CPU cores
                workers = os.cpu_count() or 4
                
                with ThreadPoolExecutor(max_workers=workers) as executor:
                    # executor.map keeps the original order of the chunks
                    for x_dec, y_dec in executor.map(process_chunk, batch_generator()):
                        x_final.extend(x_dec)
                        y_final.extend(y_dec)

            self.finished_parsing.emit(x_final, y_final)

        except Exception as e:
            self.error_occurred.emit(str(e))
