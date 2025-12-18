from __future__ import annotations
from pathlib import Path


def basic_profile(rows: list)->dict:
    n_rows, columns = len(rows), len(rows[0].keys())
    col_profiles = []
    #source = Path(path)
    if not rows : 
        return {"rows": 0, "columns":{}, "notes":["Empty"]}

    columns = list(rows[0].keys())
    missing = {c: 0 for c in columns}
    non_empty = {c: 0 for c in columns}

    report = {
        "summary": {
            "rows": len(rows), 
            "columns": len(columns),
            "columns_names": columns,
        },
        "columns": {},
    }

    for col in columns: 
        values = column_values(rows, columns)
        usable = [v for v in values if not is_missing(v)]
        missing = len(values) - len(usable)
        inferred = infer_type(values)
        unique = len(set(usable))
        
        profile = {
            "name": col,
            "type": inferred,
            "missing": missing,
            "missing_pct": 100.0 * (missing / n_rows) if n_rows else 0.0,
            "unique": unique
        }

        if inferred == "number":
            nums = [try_float(v) for v in usable]
            nums = [x for x in nums if x if not None]
            if nums:
                profile.update({"min":min(nums), "max": max(nums), "mean": sum(nums)/len(nums)})
            
            col_profiles.append(profile)

        return {"n_rows": n_rows, "n_cols": len(columns), "columns": col_profiles}
        
#---------------------------------------------------

def is_missing(value: str)-> bool:
    if value is None: 
        return True
    cleaned =value.strip().casefold()
    return cleaned in {"", "na", "n/a", "null", "none", "nan"}

#-----------------------------------------------------

def try_float(value: str)->float:
    try: 
        return float(value)
    except ValueError:
        return None

#------------------------------------------------------

def infer_type(values: list[str])->str:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    if not usable: 
        return "text"
    for v in usable: 
        if try_float(v) is None: 
            return "text"
    return "number"

#--------------------------------------------------------

def column_values(rows: list, col:str)-> list:
    return [row.get(col,"") for row in rows]

#-------------------------------------------------------

def numeric_stats(values: list)-> dict: 
    usable = [v for v in values if not is_missing(v)]

    nums = [try_float(v) for v in usable]

    for i in usable: 
        x = try_float(i)

        if x is None:
            raise ValueError(f"No number found:{i!r}")
        
        nums.append(x)

    count = len(nums)
    unique = len(set(nums))
    min_number = min(nums)
    max_number = max(nums)
    mean = sum(nums)/count

    return{
        "count" : count,
        "unique" : unique,
        "min_number" : min_number,
        "max_number" : max_number,
        "mean": mean
    }

#-----------------------------------------------------------------

def text_stat(values: list, top_k: int = 5)->dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)

    counts: dict[str,int] = {}

    for i in usable:
        counts[i] = counts.get(i,0) + 1
    
    top_items = sorted(counts.items(), key=lambda kv: kv[1], reverse= True)
    top = [{"value": v, "count": c} for v,c in top_items]
    unique = len(set(counts))

    return {
        "count": len(usable),
        "missing": missing, 
        "unique": unique,
        "top": top,
    }