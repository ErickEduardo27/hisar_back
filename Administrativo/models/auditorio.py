from django.db import models

class AuditorioArea(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = 'Administrativo_auditorioAreas'  # Para que coincida con la tabla en la BD
    def __str__(self):
        return self.nombre

class AuditorioComponente(models.Model):
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
        db_table = 'Administrativo_auditorioComponentes'  # Nombre de la tabla en la BD

    def __str__(self):
        return self.nombre if self.nombre else "Sin nombre"

class AuditorioRol(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Administrativo_auditorioRol'  # Nombre de la tabla en la BD

    def __str__(self):
        return self.nombre if self.nombre else "Sin nombre"

class AuditorioPersonal(models.Model):
    correo = models.CharField(max_length=50, null=True, blank=True)
    estado = models.BooleanField(default=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    rol = models.ForeignKey(AuditorioRol, on_delete=models.PROTECT, related_name="personal")
    area = models.ForeignKey(AuditorioArea, on_delete=models.PROTECT, related_name="personal")
    usuario_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Administrativo_auditorioPersonal'  # Nombre de la tabla en la BD

    def __str__(self):
        return f"{self.nombre} ({self.correo})"

class AuditorioRolComponentes(models.Model):
    rol = models.ForeignKey(AuditorioRol, on_delete=models.CASCADE, related_name="rol_componentes")
    componente = models.ForeignKey(AuditorioComponente, on_delete=models.CASCADE, related_name="componente_roles")

    class Meta:
        db_table = "Administrativo_auditorioRolComponentes"

    def __str__(self):
        return f"{self.rol.nombre} - {self.componente.nombre}"