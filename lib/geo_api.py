import requests
import json
from datetime import date
from typing import Tuple, List

def get_num_str(num: int):
    return str(num) if num > 9 else f'0{num}'

def get_by_coordinates(point: Tuple[float, float], distance: int, start: date, end: date, language: str) -> List[int]:
    start_str = f'{start.year}-{get_num_str(start.month)}-{get_num_str(start.day)}'
    end_str = f'{end.year}-{get_num_str(end.month)}-{get_num_str(end.day)}'
    query = f'?from_date={start_str}&to_date={end_str}&distance={distance}&latitude={point[0]}&longitude={point[1]}&language={language}'
    res = requests.get(f'https://sigspatial.yunhefeng.me/api/query_coordinates.php{query}')
    if res.status_code != 200:
        print(res)
        return []
    data = json.loads(res.content)
    return [int(item) for item in data]