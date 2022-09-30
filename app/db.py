import collections
from flask_sqlalchemy import SQLAlchemy
from app.common.util import transform

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
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
        
    @classmethod
    def simple_filter_all(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def simple_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()