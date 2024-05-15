from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
import models
import schemas
import bcrypt

crypto = CryptContext(schemes=["bcrypt"])

def verificar_contrasena(contrasena_plana, contrasena_hash):
    return crypto.verify(contrasena_plana, contrasena_hash)

def autenticar_usuario(documento_identidad: str, contrasena: str, db: Session):
    empleado = obtener_empleado_por_documento(db, documento_identidad)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    if not verificar_contrasena(contrasena, empleado.contrasena_hash):
        raise HTTPException(status_code=401, detail="Contrasena incorrecta")
    return empleado

def obtener_empleado_por_documento(db: Session, documento_identidad: str):
    return db.query(models.empleados).filter(models.empleados.documento == documento_identidad).first()

def obtener_empleado_por_id(db: Session, id_empleado: str):
    return db.query(models.empleados).filter(models.empleados.id_empleado == id_empleado).first()

def obtener_contrasena(db: Session, documento_identidad: str):
    return db.query(models.empleados.contrasena).filter(models.empleados.documento == documento_identidad).first()

def crear_empleado(db: Session, datos_empleado: schemas.EmpleadoCreado):
    contrasena_plana = datos_empleado.contrasena
    contrasena_hash = bcrypt.hashpw(contrasena_plana.encode(), bcrypt.gensalt())
    registro_empleado = models.empleados(id_empleado=datos_empleado.id_empleado,
                                         documento=datos_empleado.documento, 
                                         nombre_completo=datos_empleado.nombre_completo,
                                         correo=datos_empleado.correo,
                                         contrasena=contrasena_hash,
                                         salario=datos_empleado.salario,
                                         area=datos_empleado.area)
    db.add(registro_empleado)
    db.commit()
    db.refresh(registro_empleado)
    return registro_empleado

def listar_empleados(db: Session, omitir: int=0, limite: int=100):
    return db.query(models.empleados).offset(omitir).limit(limite).all()

def actualizar_info_personal(db: Session, info_empleado: schemas.InfoEmpleado, documento_identidad: str):
    print("Actualizando información personal...")
    db.query(models.empleados).filter(models.empleados.documento == documento_identidad).update({"documento": info_empleado.documento,
                                                                                                 "nombre_completo": info_empleado.nombre_completo,
                                                                                                 "correo": info_empleado.correo})
    db.commit()

def actualizar_datos_empleado(db: Session, datos_empleado: schemas.GeneralEmpleado, id_empleado: str):
    db.query(models.empleados).filter(models.empleados.id_empleado == id_empleado).update({
        "documento": datos_empleado.documento,
        "nombre_completo": datos_empleado.nombre_completo,
        "correo": datos_empleado.correo,
        "salario": datos_empleado.salario,
        "area": datos_empleado.area,
        "pago_realizado": datos_empleado.pago_realizado})
    db.commit()
