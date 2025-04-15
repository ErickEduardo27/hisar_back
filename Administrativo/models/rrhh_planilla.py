from django.db import models
""" Seguridad """
class RrhhPlanillaArea(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    class Meta:
        db_table = 'Administrativo_rrhhPlanillaArea'  # Para que coincida con la tabla en la BD
    def __str__(self):
        return self.nombre

class RrhhPlanillaComponente(models.Model):
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
        db_table = 'Administrativo_rrhhPlanillaComponente'  # Nombre de la tabla en la BD

    def __str__(self):
        return self.nombre if self.nombre else "Sin nombre"

class RrhhPlanillaRol(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Administrativo_rrhhPlanillaRol'  # Nombre de la tabla en la BD

    def __str__(self):
        return self.nombre if self.nombre else "Sin nombre"

class RrhhPlanillaUsuario(models.Model):
    correo = models.CharField(max_length=50, null=True, blank=True)
    estado = models.BooleanField(default=True)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    rol = models.ForeignKey(RrhhPlanillaRol, on_delete=models.PROTECT, related_name="personal")
    area = models.ForeignKey(RrhhPlanillaArea, on_delete=models.PROTECT, related_name="personal")
    usuario_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Administrativo_rrhhPlanillaUsuario'  # Nombre de la tabla en la BD

    def __str__(self):
        return f"{self.nombre} ({self.correo})"

class RrhhPlanillaRolComponentes(models.Model):
    rol = models.ForeignKey(RrhhPlanillaRol, on_delete=models.CASCADE, related_name="rol_componentes")
    componente = models.ForeignKey(RrhhPlanillaComponente, on_delete=models.CASCADE, related_name="componente_roles")

    class Meta:
        db_table = "Administrativo_rrhhPlanillaRolComponentes"

    def __str__(self):
        return f"{self.rol.nombre} - {self.componente.nombre}"


""" class AdministrativoRRHHPersonal(models.Model):
    cod_planilla = models.CharField(max_length=50)
    nombre_completo = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    nombres = models.CharField(max_length=150)
    cargo = models.CharField(max_length=150)
    cond_ingreso = models.CharField(max_length=50)
    horario = models.CharField(max_length=50)
    descripcion_cargo = models.TextField(null=True, blank=True)
    horario_id = models.IntegerField(null=True, blank=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = "Administrativo_rrhhPersonal"

    def __str__(self):
        return f"{self.nombre_completo} - {self.cargo}" """

class AdministrativoRRHHPersonal(models.Model):
    cod_planilla = models.CharField(max_length=50)
    nombre_completo = models.CharField(max_length=255)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    nombres = models.CharField(max_length=150)
    cargo = models.CharField(max_length=150)
    cond_ingreso = models.CharField(max_length=50)
    horario = models.CharField(max_length=50,null=True, blank=True)
    descripcion_cargo = models.TextField(null=True, blank=True)
    horario_id = models.IntegerField(null=True, blank=True)
    estado = models.BooleanField(default=True)
    # Nuevos campos añadidos:
    marca = models.CharField(max_length=10, null=True, blank=True)
    codigo_uni = models.CharField(max_length=50, null=True, blank=True)
    #Datos laborales
    codigo_dep = models.CharField(max_length=50, null=True, blank=True)
    cuenta_cor = models.CharField(max_length=50, null=True, blank=True)
    codigo_ban = models.CharField(max_length=50, null=True, blank=True)
    cuenta_cts = models.CharField(max_length=50, null=True, blank=True)
    banco_cts = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    codigo_lin = models.CharField(max_length=50, null=True, blank=True)
    descri_lin = models.CharField(max_length=255, null=True, blank=True)
    cod_linant = models.CharField(max_length=50, null=True, blank=True)
    grupo_ocup = models.CharField(max_length=10, null=True, blank=True)
    exone = models.CharField(max_length=10, null=True, blank=True)
    por_zmd = models.CharField(max_length=10, null=True, blank=True)
    codigo_spp = models.CharField(max_length=50, null=True, blank=True)
    codigo_sap = models.CharField(max_length=50, null=True, blank=True)
    fecha_camb = models.CharField(max_length=20, null=True, blank=True)  # puedes cambiar a DateField si es fecha real
    fecha_iafp = models.CharField(max_length=20, null=True, blank=True)  # lo mismo
    #Datos financieros
    codigo_niv = models.CharField(max_length=10, null=True, blank=True)
    descri_niv = models.CharField(max_length=100, null=True, blank=True)
    codigo_esp = models.CharField(max_length=50, null=True, blank=True)
    area_ubica = models.CharField(max_length=10, null=True, blank=True)
    funcion = models.CharField(max_length=10, null=True, blank=True)
    oodd = models.CharField(max_length=10, null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    fecha_ingr = models.CharField(max_length=20, null=True, blank=True)
    fecha_ulqu = models.CharField(max_length=20, null=True, blank=True)
    quin_recon = models.CharField(max_length=10, null=True, blank=True)
    acum_falta = models.CharField(max_length=10, null=True, blank=True)
    tiemp_serv = models.CharField(max_length=20, null=True, blank=True)
    fecha_naci = models.CharField(max_length=20, null=True, blank=True)
    nume_cipss = models.CharField(max_length=50, null=True, blank=True)
    cent_asist = models.CharField(max_length=10, null=True, blank=True)
    tipo_perso = models.CharField(max_length=10, null=True, blank=True)
    regi_pensi = models.CharField(max_length=10, null=True, blank=True)
    cond_ingre = models.CharField(max_length=10, null=True, blank=True)
    codi_afp = models.CharField(max_length=10, null=True, blank=True)
    exoneafp = models.CharField(max_length=10, null=True, blank=True)
     #Datos financieros
    situacion = models.CharField(max_length=10, null=True, blank=True)
    designacio = models.CharField(max_length=10, null=True, blank=True)
    mes_vacaci = models.CharField(max_length=10, null=True, blank=True)
    lib_electo = models.CharField(max_length=20, null=True, blank=True)
    esta_civil = models.CharField(max_length=10, null=True, blank=True)
    tipo_doc = models.CharField(max_length=10, null=True, blank=True)
    periodo = models.CharField(max_length=10, null=True, blank=True)
    totai = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    totad = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    porc_aum = models.CharField(max_length=10, null=True, blank=True)
    remunera = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    enc_plaz = models.CharField(max_length=10, null=True, blank=True)
    bonifica = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    liberados = models.CharField(max_length=10, null=True, blank=True)
    dias_licen = models.CharField(max_length=10, null=True, blank=True)
    dias_falta = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = "Administrativo_rrhhPersonal"

    def __str__(self):
        return f"{self.nombre_completo} - {self.cargo}"

class AdministrativoRRHHHorario(models.Model):
    horario = models.CharField(max_length=100)
    hora_inicio = models.CharField(max_length=100)
    hora_fin = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_edicion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Administrativo_rrhhHorario"

    def __str__(self):
        return self.horario

class AdministrativoRRHHPeriodo(models.Model):
    periodo = models.CharField(max_length=100,unique=True)
    mes = models.CharField(max_length=50)
    year = models.CharField(max_length=50)

    class Meta:
        db_table = "Administrativo_rrhhPeriodo"

    def __str__(self):
        return self.periodo

class AdministrativoRRHHDias(models.Model):
    periodo = models.ForeignKey(AdministrativoRRHHPeriodo, on_delete=models.PROTECT, related_name="dias_del_periodo")
    nombre_dia = models.CharField(max_length=15)
    numero_dia = models.IntegerField()
    es_feriado = models.BooleanField(default=False)

    class Meta:
        db_table = "Administrativo_rrhhPlanillaDias"

    def __str__(self):
        return f"{self.numero_dia} - {self.nombre_dia}"

class AdministrativoRRHHDiasHorario(models.Model):
    dias = models.ForeignKey(AdministrativoRRHHDias, on_delete=models.PROTECT, related_name="dias_de_periodo")
    personal = models.ForeignKey(AdministrativoRRHHPersonal, on_delete=models.PROTECT, related_name="personal_dias")
    horas_guardia = models.CharField(max_length=15, null=True, blank=True)
    horas_horario = models.CharField(max_length=15, null=True, blank=True)
    rango_horario = models.CharField(max_length=15, null=True, blank=True)
    rango_guardia = models.CharField(max_length=15, null=True, blank=True)
    tipo = models.CharField(max_length=15, null=True, blank=True)
    he_25 = models.CharField(max_length=15, null=True, blank=True)
    he_35 = models.CharField(max_length=15, null=True, blank=True)
    es_jefe = models.BooleanField(default=False, null=True, blank=True)
    

    class Meta:
        db_table = "Administrativo_rrhhPlanillaDiasHorario"

    def __str__(self):
        return f"{self.horas_guardia} - {self.horas_horario}"