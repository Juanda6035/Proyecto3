from pydantic import BaseModel

class EmpleadoBase(BaseModel):
    id_empleado : str
    documento: str
    nombre_completo: str
    correo : str
    salario: int
    area: str

class EmpleadoCreado(EmpleadoBase):
    contraseña : str



class InfoEmpleado(BaseModel):
    documento: str
    nombre_completo: str
    correo : str

class GeneralEmpleado(InfoEmpleado):

    salario: int
    area: str
    pago_realizado: bool

    class Config:
        from_attributes = True

class Crear_empleado(BaseModel):
    Empleado: EmpleadoCreado

class Eliminar_empleado(BaseModel):
    Doc_empleado: str

class Actualizar_empleado(BaseModel):
    id_empleado: str
    Info_empleado: GeneralEmpleado


