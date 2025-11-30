from datetime import datetime
from collections import deque

class HistoryManager:
    def __init__(self, max_items=10):
        self.max_items = max_items
        self.history = deque(maxlen=max_items)
    
    def add_entry(self, image, ocr_result, art_result):
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'image': image,
            'ocr_result': ocr_result,
            'art_result': art_result
        }
        self.history.append(entry)
        return len(self.history)
    
    def get_history(self):
        return list(self.history)
    
    def get_latest(self):
        if self.history:
            return self.history[-1]
        return None
    
    def clear_history(self):
        self.history.clear()
    
    def get_summary(self):
        summary = []
        for idx, entry in enumerate(self.history, 1):
            summary.append({
                'index': idx,
                'timestamp': entry['timestamp'],
                'ocr_preview': entry['ocr_result'][:50] + '...' if len(entry['ocr_result']) > 50 else entry['ocr_result'],
                'art_preview': entry['art_result'][:50] + '...' if len(entry['art_result']) > 50 else entry['art_result']
            })
        return summary
    
    def get_entry(self, index):
        if 0 <= index < len(self.history):
            return self.history[index]
        return None
    
    def export_history(self):
        history_data = []
        for entry in self.history:
            history_data.append({
                'timestamp': entry['timestamp'],
                'ocr_result': entry['ocr_result'],
                'art_result': entry['art_result']
            })
        return history_data