from datetime import datetime
from decimal import Decimal

def transformData(data):
   data_transform = {}
   for k, v in data.items():
      if type(v) is dict and v.get('id') is not None:
            data_transform[f'{k}_id'] = v['id']
      else:
            data_transform[k] = v
   return data_transform

def transform(a):
   if type(a) is float:
      return round(a, 1)
   if type(a) is datetime:
      return str(a)
   return a
