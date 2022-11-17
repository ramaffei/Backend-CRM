import collections
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app.common.util import transform
from sqlalchemy.orm import ColumnProperty, RelationshipProperty, InstrumentedAttribute

db = SQLAlchemy()

class BaseModelMixin:
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self, data: dict):
        for k, v in data.items():
            #print(f'{k} = {v}\n')
            setattr(self, k, v)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def buscar_cambios(self, **kwargs) -> dict:
        cambios = {}
        for k, v in self.__dict__.items():
            if kwargs.get(k) is not None:
                if isinstance(v, self.__class__.__bases__):
                    cambios_sub = v.buscar_cambios(**kwargs.get(k))
                    if len(cambios_sub) > 0:
                        cambios[k] = cambios_sub
                elif transform(kwargs.get(k)) != transform(v):
                    
                    cambios[k] = transform(kwargs.get(k))
        return self.transformData(cambios)

    def transformData(self, data):
        data_transform = {}
        for k, v in data.items():
            if type(v) is dict and v.get('id') is not None:
                    data_transform[f'{k}_id'] = v['id']
            else:
                    data_transform[k] = v
        return data_transform                    

    def buscarRelacionEnLista(self, key_list, **kwargs):
            
        for k, v in kwargs.items():
            if v is not None:
                obj = list(
                    filter(
                    lambda x: getattr(x, k, None) is not None and getattr(x, k) == v,
                    getattr(self, key_list)
                    )
                )

                if len(obj)> 0 and obj[0] is not None:
                    return obj[0]

    @classmethod
    def get_all(cls, limit = None, page = None):
        query = cls.query
        headers = {
            'x-count': query.count(),
        }
        if limit is not None:
            query = query.limit(limit)
            headers['x-limit'] = limit
        if page is not None:
            query = query.offset(int(page)*int(limit))
            headers['x-page'] = page
            headers['x-total-pages'] = (int(headers['x-count']) // int(limit))+1

        return query.all(), 201, headers

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
        
    @classmethod
    def simple_filter_all(cls, **kwargs):
        print(kwargs)
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def simple_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def avanze_filter_all(cls, json, limit = None, page = None):
        query = cls.query
        q = False
        for arg, value in json.items():
            key=None
            if '__' in arg:
                arg = arg.split('__')
                if len(arg) >= 2:
                    key = arg[1]
                    arg = arg[0]
            column = getattr(cls, arg, None)
            if isinstance(column, InstrumentedAttribute):
                q = True
                if isinstance(column.property, ColumnProperty):
                    sub_query = query.filter(column == value)
                    try :
                        value = datetime.strptime(value, r'%Y-%m-%d')
                        if key == 'desde': 
                            sub_query = query.filter(column > value)
                        elif key == 'hasta':
                            sub_query = query.filter(column < value)
                        else:
                            sub_query = query.filter(column == value)
                    except Exception:
                        pass
                    query = sub_query
                elif isinstance(column.property, RelationshipProperty):
                    model = column.property.entity.class_
                    query = query.join(model).filter(getattr(model, key).like(f'{value}%'))
        if limit is not None:
            query = query.limit(limit)
        if page is not None:
            query = query.offset(int(page)*int(limit))
        return query.all() if q else []