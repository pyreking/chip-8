import json
import numpy as np

class Chip8Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.dtype, np.generic, np.ndarray)):
            return obj.tolist()
        if isinstance(obj, set):
            return list(obj)
        
        return json.JSONEncoder.default(self, obj)