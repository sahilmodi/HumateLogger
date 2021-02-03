import numpy as np
from typing import List

from .humate import Humate
from .utils import UnitsRange

buckets = [0, 600, 1200, 2000, 4000]

def optimal_dispension(units_range: UnitsRange, medicine: List[Humate]) -> List[Humate]:
    bucketized = np.digitize([humate.units for humate in medicine], bins=buckets)
    medicine_zip = sorted(zip(medicine, bucketized), key=lambda x: (-x[1], x[0].expiration))
    return dispension_dfs(units_range, [x[0] for x in medicine_zip], []) 

def dispension_dfs(units_range: UnitsRange, medicine: List[Humate], res: List[Humate]) -> List[Humate]:
    if units_range.max < 0:
        return []
    if units_range.min <= 0:
        return res

    for i in range(len(medicine)):
        humate = medicine[i]
        new_medicine = medicine[:i] + medicine[i+1:]
        recurse = dispension_dfs(units_range - humate.units, new_medicine, res + [humate])
        if len(recurse):
            return recurse
    
    return []