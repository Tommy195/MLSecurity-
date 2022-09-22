import json
import requests
from dataclasses import dataclass
from db import db
import bcrypt
import base64, hashlib

class InformationModel(db.Model):
    __tablename__ = 'information'

    id = db.Column(db.Integer, primary_key=True)
    fec_alta = db.Column(db.String(200))
    user_name = db.Column(db.String(200))
    codigo_zip = db.Column(db.Text)
    credit_card_num = db.Column(db.Text) 
    credit_card_ccv = db.Column(db.Text) 
    cuenta_numero = db.Column(db.Text) 
    direccion = db.Column(db.Text) 
    geo_latitud = db.Column(db.Text) 
    geo_longitud = db.Column(db.Text) 
    color_favorito = db.Column(db.Text) 
    foto_dni = db.Column(db.Text) 
    ip = db.Column(db.Text) 
    auto = db.Column(db.String(200))
    auto_modelo = db.Column(db.String(200))
    auto_tipo = db.Column(db.String(200))
    auto_color = db.Column(db.String(200))
    cantidad_compras_realizadas = db.Column(db.Text)  
    avatar = db.Column(db.String(200))
    fec_birthday = db.Column(db.Text)         


    def __init__(self, id, fec_alta, user_name, codigo_zip, credit_card_num, credit_card_ccv, cuenta_numero, direccion, geo_latitud, geo_longitud, color_favorito, foto_dni, ip, auto, auto_modelo, auto_tipo, auto_color, cantidad_compras_realizadas, avatar, fec_birthday):
        self.id = id
        self.fec_alta = fec_alta
        self.user_name = user_name
        self.codigo_zip = codigo_zip
        self.credit_card_num = credit_card_num
        self.credit_card_ccv = credit_card_ccv
        self.cuenta_numero = cuenta_numero
        self.direccion = direccion
        self.geo_latitud = geo_latitud
        self.geo_longitud = geo_longitud
        self.color_favorito = color_favorito
        self.foto_dni = foto_dni
        self.ip = ip
        self.auto = auto
        self.auto_modelo = auto_modelo
        self.auto_tipo = auto_tipo
        self.auto_color = auto_color
        self.cantidad_compras_realizadas = cantidad_compras_realizadas 
        self.avatar = avatar
        self.fec_birthday = fec_birthday        

    def json(self):
        return {'id': self.id, 'fec_alta': self.fec_alta, 'user_name': self.user_name, 'codigo_zip': self.codigo_zip, 'credit_card_num': self.credit_card_num, 'credit_card_ccv': self.credit_card_ccv, 'cuenta_numero': self.cuenta_numero, 'direccion': self.direccion, 'geo_latitud': self.geo_latitud, 'geo_longitud': self.geo_longitud, 'color_favorito': self.color_favorito, 'foto_dni': self.foto_dni, 'ip': self.ip, 'auto': self.auto, 'auto_modelo': self.auto_modelo, 'auto_tipo': self.auto_tipo, 'auto_color': self.auto_color, 'cantidad_compras_realizadas': self.cantidad_compras_realizadas, 'avatar': self.avatar, 'fec_birthday': self.fec_birthday}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def hashing(self, objectToBeHashed):
            toHash = objectToBeHashed.encode('utf-8')
            hash_pass = bcrypt.hashpw(toHash, bcrypt.gensalt())
            
            return hash_pass
    
    def get(self):        
        response = requests.get('https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios')
        information_dict = json.loads(response.content)
        
        for information in information_dict:
            information_object = InformationModel(**information)
            existentID = information_object.find_by_id(information_object.id)
            
            if not existentID:
                information_object.codigo_zip = information_object.hashing(information_object.codigo_zip)
                information_object.color_favorito = information_object.hashing(information_object.color_favorito)
                information_object.credit_card_ccv = information_object.hashing(information_object.credit_card_ccv)
                information_object.credit_card_num = information_object.hashing(information_object.credit_card_num)
                information_object.cuenta_numero = information_object.hashing(information_object.cuenta_numero)
                information_object.direccion = information_object.hashing(information_object.direccion)
                information_object.fec_birthday = information_object.hashing(information_object.fec_birthday)
                information_object.foto_dni = information_object.hashing(information_object.foto_dni)
                information_object.geo_latitud = information_object.hashing(information_object.geo_latitud)
                information_object.geo_longitud = information_object.hashing(information_object.geo_longitud)
                information_object.ip = information_object.hashing(information_object.ip)
                information_object.user_name = information_object.hashing(information_object.user_name)
                
                information_object.save_to_db()
        
        return information_object