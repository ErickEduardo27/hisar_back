from django.db import models

class SeguridadArea(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = 'Administrativo_seguridadArea'  # Para que coincida con la tabla en la BD
    def __str__(self):
        return self.nombre

class SeguridadComponente(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    path = models.CharField(max_length=255, null=True, blank=True)
    padre = models.ForeignKey(
        'self',  # Referencia a la misma tabla
        on_delete=models.SET_NULL,  
        null=True, 
        blank=True,
        related_name='subcomponentes'
    )
    icon = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Administrativo_seguridadComponente'  # Nombre de la tabla en la BD

    def __str__(self):
        return self.nombre if self.nombre else "Sin nombre"


class SeguridadSystem(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Administrativo_seguridadSystem'  # Nombre de la tabla en la BD

    def __str__(self):
        return self.nombre if self.nombre else "Sin nombre"

class SeguridadRol(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)
    system =models.ForeignKey(SeguridadSystem, on_delete=models.PROTECT, related_name="system")
    class Meta:
        db_table = 'Administrativo_seguridadRol'  # Nombre de la tabla en la BD

    def __str__(self):
        return self.nombre if self.nombre else "Sin nombre"


class SeguridadUsuario(models.Model):
    correo = models.CharField(max_length=50, null=True, blank=True)
    estado = models.BooleanField(default=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    rol = models.ForeignKey(SeguridadRol, on_delete=models.PROTECT, related_name="usuario")
    area = models.ForeignKey(SeguridadArea, on_delete=models.PROTECT, related_name="usuario")
    usuario_id = models.CharField(max_length=255, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_edicion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Administrativo_seguridadUsuario'  # Nombre de la tabla en la BD

    def __str__(self):
        return f"{self.nombre} ({self.correo})"

class SeguridadRolComponentes(models.Model):
    rol = models.ForeignKey(SeguridadRol, on_delete=models.CASCADE, related_name="rol_componentes")
    componente = models.ForeignKey(SeguridadComponente, on_delete=models.CASCADE, related_name="componente_roles")

    class Meta:
        db_table = "Administrativo_seguridadRolComponentes"

    def __str__(self):
        return f"{self.rol.nombre} - {self.componente.nombre}"