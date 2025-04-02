from django.db import models
from django.contrib.gis.db import models as gis_models

# Pacientes geolocalizados Temporalmente
class pacienteGeoTem(models.Model):
    dni = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=150)
    hospital = models.CharField(max_length=50)
    direccion = models.CharField(max_length=250)
    distrito = models.CharField(max_length=50)
    latitud = models.CharField(max_length=50,null=True, blank=True)
    longitud = models.CharField(max_length=50,null=True, blank=True)
    telefono = models.CharField(max_length=50, null=True, blank=True)
    frecuencia = models.CharField(max_length=20, null=True, blank=True)
    turno = models.CharField(max_length=20, null=True, blank=True)
    serologia = models.CharField(max_length=20)
    cordePac = gis_models.PointField("Location in Map", geography=True, blank=True, null=True,srid=4326, help_text="Point(longitude latitude)")
    
    def __str__(self):
        return self.nombre

# Tablas Generales

class ubigeo(models.Model):
    ubigeo_reniec = models.CharField(max_length=10)
    ubigeo_inei = models.CharField(max_length=10)
    codDepartamento_inei = models.CharField(max_length=10)
    departamento = models.CharField(max_length=50)
    codProvincia_inei = models.CharField(max_length=10)
    provincia = models.CharField(max_length=50)
    distrito = models.CharField(max_length=50)
    
    def __str__(self):
        return self.ubigeo_reniec

# Ubicacion usuario

class cas(models.Model):
    codCas = models.CharField(max_length=15, unique=True)
    descripCas = models.CharField(max_length=100)
    tipoCas = models.CharField(max_length=10)
    distrito = models.CharField(max_length=100)
    estado = models.BooleanField()
    latitud = models.CharField(max_length=100, null=True, blank=True)
    longitud = models.CharField(max_length=100, null=True, blank=True)
    cordeCas = gis_models.PointField("Location in Map", geography=True, blank=True, null=True,srid=4326, help_text="Point(longitude latitude)")

    def __str__(self):
        return (self.descripCas)

# Seguridad
class usuario(models.Model):
    num_doc = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=50)
    cas = models.ForeignKey(cas, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=15, unique=True)
    clave = models.CharField(max_length=20)
    perfil_id = models.CharField(max_length=50)
    estadoGeo = models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return (self.usuario)

class perfil(models.Model):
    perfil = models.CharField(max_length=50)
    ruta = models.CharField(max_length=50)
    imagen = models.CharField(max_length=50)

    def __str__(self):
        return (self.perfil)

# Create your models here.
class maestro(models.Model):
    codMaestro = models.CharField(max_length=10)
    descripMaestro = models.CharField(max_length=50)
    detalleMaestro = models.CharField(max_length=50)

    def __str__(self):
        return (self.descripMaestro)

class hospital(models.Model):
    id = models.AutoField(primary_key=True)
    hospital = models.CharField(max_length=100)
    ruc = models.CharField(max_length=100)  # Asumiendo que Paciente es tu modelo de paciente
    tipo_institucion = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    inicio_actividades = models.CharField(max_length=100)
    estado=models.BooleanField(blank=True, null=True)
    

    class Meta:
        db_table = 'Asistencial_hospital'

    def __str__(self):
        return str(self.hospital)

class medico(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=100)  # Asumiendo que Paciente es tu modelo de paciente
    correo = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    

    class Meta:
        db_table = 'Asistencial_medico'

    def __str__(self):
        return str(self.nombre)

class paciente(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_doc = models.ForeignKey(maestro, on_delete=models.CASCADE)
    num_doc = models.CharField(max_length=15, unique=True)
    ape_pat = models.CharField(max_length=40)
    ape_mat = models.CharField(max_length=50)    
    nombres = models.CharField(max_length=50)
    fecha_nac = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True)
    hospital_id = models.ForeignKey(hospital, on_delete=models.PROTECT,db_column='hospital_id')
    medico_id = models.ForeignKey(medico, on_delete=models.PROTECT,db_column='medico_id')
    fecha_ultima_dialisis = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(max_length=5, default=1)
    latitud = models.CharField(max_length=100, null=True, blank=True)
    longitud = models.CharField(max_length=100, null=True, blank=True)
    cordePac = gis_models.PointField("Location in Map", geography=True, blank=True, null=True,srid=4326, help_text="Point(longitude latitude)")
    direccion = models.CharField(max_length=200, null=True, blank=True)
    distrito = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=100, null=True, blank=True)
    telefonoAlterno = models.CharField(max_length=100, null=True, blank=True)
    referencia=models.CharField(max_length=100, null=True, blank=True)
    ubigeo_id  = models.ForeignKey(ubigeo, on_delete=models.PROTECT,db_column='ubigeo_id')
    serologia=models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nombres
        
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.ape_pat} {self.ape_mat}"

class instaladores(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    fecha_modificacion = models.DateField(null=True, blank=True)
    imagen = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = 'Administrativa_instaladores'
    def __str__(self):
        return self.nombre

class serologiaPaciente(models.Model):
    paciente = models.OneToOneField(paciente, on_delete=models.CASCADE, unique=True)
    tipoSerologia = models.CharField(max_length=40)
    serologia = models.CharField(max_length=40)
    
    def __str__(self):
        return (self.tipoSerologia)

class examen(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    tipo_exam = models.CharField(max_length=50, null=True)
    archivo_exam = models.FileField(upload_to='media/', null=True)
    estado_lectura = models.CharField(max_length=30, null=True)
    estado = models.CharField(max_length=5, default='1')
    fecha_reg = models.DateTimeField(auto_now_add=True)
    user_reg = models.CharField(max_length=40, null=True)
    fecha_mod = models.DateTimeField(null=True)
    user_mod = models.CharField(max_length=50, null=True)
    fecha_eli = models.DateTimeField(null=True)
    user_eli = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.tipo_exam

class archivo(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    numHisCli = models.CharField(max_length=30, null=True)
    numBalda = models.CharField(max_length=30, null=True)
    estado = models.CharField(max_length=5, default='1')
    user_reg = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.numHisCli
# Tabla Clinicas     

class presAnemia(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    fechaPres = models.DateField()
    nomNefro = models.CharField(max_length=30)
    medPres = models.CharField(max_length=30)
    dosisPres = models.IntegerField()
    medHiePres = models.CharField(max_length=30)
    dosisHiePres = models.IntegerField()
    viaAdmPres = models.CharField(max_length=10)
    viaAdmHiePres = models.CharField(max_length=10)
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomNefro

class admiAnemia(models.Model):
    presAnemia = models.ForeignKey(presAnemia, on_delete=models.CASCADE)
    fechaAdmi = models.DateField()
    nomEnfer = models.CharField(max_length=30)
    medAdmi = models.CharField(max_length=30)
    dosisAdmi = models.IntegerField()
    medHieAdmi = models.CharField(max_length=30)
    dosisHieAdmi = models.IntegerField()
    viaAdm = models.CharField(max_length=10)
    viaAdmHierro = models.CharField(max_length=10)
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomEnfer

class exclusionAnemia(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    fechaExclu = models.DateField()
    razonExclu = models.CharField(max_length=30)
    ObservaExclu = models.CharField(max_length=30)
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.razonExclu

class movimientoAnemia(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    fechaMotivo = models.DateField()
    razonMotivo = models.CharField(max_length=30)
    obserMotivo = models.CharField(max_length=30)

    def __str__(self):
        return self.razonMotivo

class nutricion(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    turno = models.CharField(max_length=30, null=True, blank=True)
    frecuencia = models.CharField(max_length=30, null=True, blank=True)
    fechaIngreso = models.DateField(null=True, blank=True)
    tipoPaciente = models.CharField(max_length=40, null=True, blank=True)
    fechaEvaluacion = models.DateField(null=True, blank=True)
    peso = models.CharField(max_length=30, null=True, blank=True)
    talla = models.CharField(max_length=30, null=True, blank=True)
    imc = models.CharField(max_length=30, null=True, blank=True)
    circuBra = models.CharField(max_length=30, null=True, blank=True)
    porcentajeCMB = models.CharField(max_length=30, null=True, blank=True)
    medCali = models.CharField(max_length=30, null=True, blank=True)
    porcentajeEPT = models.CharField(max_length=30, null=True, blank=True)
    albSerica = models.CharField(max_length=30, null=True, blank=True)
    ValGlobalSub = models.CharField(max_length=30, null=True, blank=True, default="NA")
    ingestaCalorica = models.CharField(max_length=60, null=True, blank=True)
    ingestaProteica = models.CharField(max_length=60, null=True, blank=True)
    ingestaCaloricaT = models.CharField(max_length=60, null=True, blank=True)
    ingestaProteicaT = models.CharField(max_length=60, null=True, blank=True)
    diagNutricional = models.CharField(max_length=60, null=True, blank=True)
    interveNutricional = models.CharField(max_length=60, null=True, blank=True)
    obsNutricion = models.CharField(max_length=100, null=True, blank=True)
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
    fechaReg = models.DateTimeField(auto_now_add=True)
    pacNuevo = models.BooleanField()

    def __str__(self):
        return self.frecuencia

# Tabla Hospitales (VGS)     

class valGlobalSub(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    fechaEval = models.DateField()
    ganPerPeso = models.CharField(max_length=15) # Ganancia o perdida de Peso  
    camPesoCorp = models.CharField(max_length=15) # Cambio de peso corporal 
    # Cambios en la dieta, en relación con lo normal 
    duraDieta = models.CharField(max_length=15) # Duración 
    resultDieta = models.CharField(max_length=15) # Resultado
    tipoDieta = models.CharField(max_length=40) # Tipo de Dieta
    sintoGastro = models.CharField(max_length=15) # Sintomas gastrointestinales
    disfuncion = models.CharField(max_length=15) # Capacidad funcional 
    cambioCapFun = models.CharField(max_length=15) # Cambio capacidad Funcional
    # Examen Fisico
    grasaSubcu = models.CharField(max_length=15) # Pérdida de grasa subcutánea 
    atrofiaMusc = models.CharField(max_length=15) # Atrofia muscular 
    EdemaTobi = models.CharField(max_length=15) # Edema de tobillos
    edemaSacro = models.CharField(max_length=15) # Edema sacro
    ascitis = models.CharField(max_length=15) # Ascitis
    # Diagnostico de Valoracion Global Subjestiva
    resultadoVGS = models.CharField(max_length=25) # Ascitis
    fechaReg = models.DateField()
    userReg = models.CharField(max_length=20)

    def __str__(self):
        return self.resultadoVGS

# Inventario Mantenimiento

class dependencia(models.Model):
    codDep = models.CharField(max_length=20, unique=True)
    descDep = models.CharField(max_length=50)

    def __str__(self):
        return self.descDep


class ambiente(models.Model):
    codAmb = models.CharField(max_length=11)
    descAmb = models.CharField(max_length=50)
    dependencia = models.ForeignKey(dependencia, on_delete=models.CASCADE)

    def __str__(self):
        return self.descAmb

class personal(models.Model):
    dniPer = models.CharField(max_length=8, unique=True)
    apePatPer = models.CharField(max_length=50)
    apeMatPer = models.CharField(max_length=50)
    nomPer = models.CharField(max_length=50)
    sexo = models.CharField(max_length=50)
    fecNacPer = models.DateField(null=True)
    codPlaPer = models.CharField(max_length=50)
    regPer = models.CharField(max_length=50)
    cargoPer = models.CharField(max_length=50)
    nivelPer = models.CharField(max_length=50)
    telefoPer = models.CharField(max_length=50)
    correoPer = models.CharField(max_length=50)
    direcPer = models.CharField(max_length=50)
    estPer = models.CharField(max_length=5, default=1)
    dependencia = models.ForeignKey(dependencia, on_delete=models.CASCADE)

    def __str__(self):
        return (self.dniPer + " | " + self.apePatPer + " " + self.apeMatPer + " " + self.nomPer)

class bienpat(models.Model):
    codEti = models.CharField(max_length=30, unique=True)
    propBien = models.CharField(max_length=50, default='ESSALUD')
    desBien = models.CharField(max_length=100)    
    serBien = models.CharField(max_length=50)
    modBien = models.CharField(max_length=15)
    marBien = models.CharField(max_length=15)
    situBien = models.CharField(max_length=5, default='B')
    valBien = models.IntegerField(default=0)
    estBien = models.CharField(max_length=5, default=1)

    
    def __str__(self):
        return (self.codEti + " | " + self.desBien)

#Mantenimiento de Maquina

class proveedor(models.Model):
    rucProveedor = models.CharField(max_length=30, unique=True)
    nombreProveedor = models.CharField(max_length=50)
    telefProveedor = models.CharField(max_length=20)
    direcProveedor = models.CharField(max_length=20, null=True)
    estadoProveedor = models.CharField(max_length=5, default=1)

    def __str__(self):
        return self.nombreProveedor

class provMaq(models.Model):
    usobien = models.CharField(max_length=5)
    bienpat = models.ForeignKey(bienpat, on_delete=models.CASCADE)

    def __str__(self):
        return self.usobien

class bienImag(models.Model):
    imagen = models.ImageField(upload_to='fotos/')
    bienpat = models.ForeignKey(bienpat, on_delete=models.CASCADE)

class bienPersonal(models.Model):
    personal = models.ForeignKey(personal, on_delete=models.CASCADE)
    bienpat = models.OneToOneField(bienpat, on_delete=models.CASCADE, unique=True)

class bienAmbiente(models.Model):
    ambiente = models.ForeignKey(ambiente, on_delete=models.CASCADE)
    bienpat = models.OneToOneField(bienpat, on_delete=models.CASCADE, unique=True)
    personal = models.ForeignKey(personal, on_delete=models.CASCADE)

class bienHadware(models.Model):
    bienpat = models.ForeignKey(bienpat, on_delete=models.CASCADE)
    procesador = models.CharField(max_length=20)
    numeroIp = models.CharField(max_length=20)
    numeroIpMv = models.CharField(max_length=20)
    numeroMac = models.CharField(max_length=20)
    memoriaRam = models.CharField(max_length=20)
    capAlmacenamiento = models.CharField(max_length=20)
    uso = models.CharField(max_length=20)
    condicion = models.CharField(max_length=20)

class bienSoftware(models.Model):
    bienpat = models.ForeignKey(bienpat, on_delete=models.CASCADE)
    sistemaOperativo = models.CharField(max_length=20)
    ofimatica = models.CharField(max_length=20)
    antivirus = models.CharField(max_length=20)

class bienDetalleMonitor(models.Model):
    bienpat = models.ForeignKey(bienpat, on_delete=models.CASCADE)
    pulgadas = models.CharField(max_length=20)

class incidenciaDsi(models.Model): 
    personal = models.ForeignKey(personal, on_delete=models.CASCADE)
    problema = models.CharField(max_length=1000)
    clasiSolu = models.CharField(max_length=50, null=True)
    solucion = models.CharField(max_length=1000, null=True)
    userReg = models.CharField(max_length=200)
    fecha_reg = models.DateTimeField(auto_now=True)
    numTicket = models.CharField(max_length=20)
    estado = models.ForeignKey(maestro, on_delete=models.CASCADE)

class personalVpn(models.Model): 
    personal = models.ForeignKey(personal, on_delete=models.CASCADE)
    ip = models.CharField(max_length=30, null=True, blank=True)
    usuario = models.CharField(max_length=30)
    clave = models.CharField(max_length=30)
    personalAutoriza = models.CharField(max_length=40)
    fechaHabilita = models.DateField(null=True, blank=True)
    fechaInstalacion = models.DateField(null=True, blank=True)
    observacion = models.CharField(max_length=200,null=True, blank=True)
    fecha_reg = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.usuario
    
class personalCertificado(models.Model):
    personal = models.ForeignKey(personal, on_delete=models.CASCADE)
    fechaSolicita = models.DateField()
    tipoCertificado = models.CharField(max_length=30)
    fechaInstalacion = models.DateField(null=True, blank=True)
    perosnalInstala =  models.CharField(max_length=40, null=True, blank=True)
    observacion = models.CharField(max_length=200, null=True, blank=True)
    fecha_reg = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tipoCertificado

class delegacionBienesEstra(models.Model):
    solPed = models.CharField(max_length=30, null=True, blank=True)
    codigoSap = models.CharField(max_length=30, null=True, blank=True)
    producto = models.CharField(max_length=200, null=True, blank=True)
    unidadMedida = models.CharField(max_length=15, null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    fechaDelegacion = models.DateField(null=True, blank=True)
    pediodoDelegacion = models.CharField(max_length=100, null=True, blank=True)
    fechaDerivacion = models.DateField(null=True, blank=True)
    fechaRequerimiento = models.DateField(null=True, blank=True)
    periodoSolicitado = models.CharField(max_length=100, null=True, blank=True)
    fechaLogistica = models.DateField(null=True, blank=True)
    numOrdenCompra = models.CharField(max_length=50, null=True, blank=True)
    monto = models.CharField(max_length=50, null=True, blank=True)
    fechaIngresoAlmacen = models.DateField(null=True, blank=True)
    fechaPago = models.DateField(null=True, blank=True)
    anulacionPedido = models.CharField(max_length=200, null=True, blank=True)
    fecha_reg = models.DateTimeField(auto_now=True)
    userOpc = models.CharField(max_length=50, null=True, blank=True)
    userUsuario = models.CharField(max_length=50, null=True, blank=True)
    userLogistica = models.CharField(max_length=50, null=True, blank=True)
    userFinanzas = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(max_length=10, null=True, blank=True)
    posiFinaciera = models.CharField(max_length=50, null=True, blank=True)
    tipoBienEstra = models.CharField(max_length=50, null=True, blank=True)
    valorTotal = models.CharField(max_length=50, null=True, blank=True)
    fechaEmiOrden = models.DateField(null=True, blank=True)
    observaLogistica = models.CharField(max_length=200, null=True, blank=True)
    tipoDoc = models.CharField(max_length=50, null=True, blank=True)
    numDoc = models.CharField(max_length=150, null=True, blank=True)
    cantiRequeridaUsu = models.IntegerField(null=True, blank=True)
    obsUsu = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.solPed

class maestroMatSap(models.Model):
    codSap = models.CharField(max_length=30)
    tipoBienes = models.CharField(max_length=70)
    desProducto = models.CharField(max_length=200)

    def __str__(self):
        return self.codSap

class parNuticion(models.Model):
    edad = models.IntegerField()
    pt = models.DecimalField(max_digits = 10, decimal_places = 2)
    cb = models.DecimalField(max_digits = 10, decimal_places = 2)
    cmb = models.DecimalField(max_digits = 10, decimal_places = 2)
    sexo = models.CharField(max_length=30)

    def __str__(self):
        return self.sexo

class listaEspera(models.Model):
    fechaSoli = models.DateField(null=True, blank=True)
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    telefonoDos = models.CharField(max_length=30, null=True, blank=True)
    casOrigen = models.CharField(max_length=100, null=True, blank=True)
    casDestino = models.CharField(max_length=100, null=True, blank=True)
    #casDestino = models.ForeignKey(cas, on_delete=models.CASCADE)
    distrito = models.CharField(max_length=120, null=True, blank=True)
    turno = models.CharField(max_length=30, null=True, blank=True)
    referencia = models.CharField(max_length=60, null=True, blank=True)
    observaciones = models.CharField(max_length=120, null=True, blank=True)
    estado = models.BooleanField()
    fecha_reg = models.DateTimeField(auto_now=True)
    user_reg = models.CharField(max_length=150, null=True, blank=True)
    fecha_mod = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.telefono

class docuContratados(models.Model):
    cas = models.ForeignKey(cas, on_delete=models.CASCADE)
    formato = models.CharField(max_length=100, null=True, blank=True)
    archivo = models.FileField(upload_to='formato/', null=True)
    estado = models.CharField(max_length=5, null=True, blank=True)
    fecha_reg = models.DateField(auto_now=True)
    usuario_reg = models.CharField(max_length=40, null=True, blank=True)
    fecha_edit = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.formato

class parameCentro(models.Model):
    cas = models.ForeignKey(cas, on_delete=models.CASCADE)
    turno = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    estado = models.BooleanField()
    fecha_reg = models.DateField(auto_now=True)
    usuario_reg = models.CharField(max_length=150, null=True, blank=True)
   
    def __str__(self):
        return self.turno

class parameCentroPuesto(models.Model):
    cas = models.ForeignKey(cas, on_delete=models.CASCADE)
    turno = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=100)
    tipoPuesto = models.CharField(max_length=50)
    numeroPuesto = models.IntegerField()
    estado = models.BooleanField()
    fecha_reg = models.DateField(auto_now=True)
    usuario_reg = models.CharField(max_length=150, null=True, blank=True)
   
    def __str__(self):
        return self.cas.descripCas+"/"+self.turno +"/"+self.frecuencia

class asigCuposPac(models.Model):
    parameCentroPuesto = models.ForeignKey(parameCentroPuesto, on_delete=models.CASCADE)
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    fechaAsigCupo = models.CharField(max_length=50, null=True, blank=True)
    fecha_reg = models.DateField(auto_now=True)
    usuario_reg = models.CharField(max_length=150, null=True, blank=True)
    fechaTerminoCupo = models.DateField(null=True, blank=True)
    usuario_reg_termino = models.CharField(max_length=150, null=True, blank=True)
    estado = models.BooleanField()
    sustento = models.FileField(upload_to='archivos_pdf/', null=True)
    motivo_liberacion = models.CharField(max_length=200, null=True, blank=True)
    tipo_paciente = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.parameCentroPuesto.cas.descripCas+"/"+self.parameCentroPuesto.turno+"/"+self.parameCentroPuesto.frecuencia+"/"+self.paciente.nombres

class asisPacDiario(models.Model):
    asigCuposPac = models.ForeignKey(asigCuposPac, on_delete=models.CASCADE)
    estadoAsistencia = models.CharField(max_length=30)
    observaFalta = models.CharField(max_length=150, null=True, blank=True)
    usuario_reg = models.CharField(max_length=150)
    fecha_reg = models.DateField(auto_now=True)
    validacionAsistencia = models.CharField(max_length=150, unique=True)
    casAsd = models.CharField(max_length=150, null=True, blank=True)
    vigSeguro = models.CharField(max_length=15, null=True, blank=True)
    estadoAcredi = models.CharField(max_length=45, null=True, blank=True)  
    def __str__(self):
        return self.usuario_reg

class asisPacDiarioAdicional(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    cas = models.ForeignKey(cas, on_delete=models.CASCADE)
    sala = models.CharField(max_length=50, null=True, blank=True)
    turno = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=100)
    estadoAsistencia = models.CharField(max_length=30)
    usuario_reg = models.CharField(max_length=150)
    fecha_reg = models.DateField(auto_now=True)
    validacionAsistencia = models.CharField(max_length=150, unique=True)
    motivo = models.CharField(max_length=150)
    casAsd = models.CharField(max_length=150, null=True, blank=True)
    vigSeguro = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.usuario_reg

#HISAR CUADRO DE MANDO INTEGRAL

class baseDatosProduccion(models.Model):
    periodo = models.DateField()
    serie = models.CharField(max_length=12)
    servicio = models.CharField(max_length=20)
    actividad = models.CharField(max_length=50)
    subactividad = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    meta = models.IntegerField()

    def __str__(self):
        return self.serie

#BACK PARA APLICATIVOS MOVIL

class loginAppHisar(models.Model):
    paciente = models.OneToOneField(paciente, on_delete=models.CASCADE, unique=True)
    contra = models.CharField(max_length=200)
    estado = models.CharField(max_length=5, default=1)
    tipoTrataPac = models.CharField(max_length=5)

class dpDiario(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    ultrafil = models.IntegerField()
    presArtSis = models.IntegerField()
    presArtDias = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    userReg = models.CharField(max_length=40)
    fechaReg = models.DateField(auto_now_add=True)
    imagenOriSalida = models.FileField(upload_to='media/imgOriSal', null=True, blank=True)

class examenLaboratorio(models.Model):
    centro = models.CharField(max_length=100, null=True, blank=True)
    periodo = models.CharField(max_length=100, null=True, blank=True)    
    area = models.CharField(max_length=100, null=True, blank=True)  
    servicio = models.CharField(max_length=100, null=True, blank=True)  
    actividad = models.CharField(max_length=100, null=True, blank=True)  
    subactividad = models.CharField(max_length=100, null=True, blank=True)  
    acto_medico = models.CharField(max_length=100, null=True, blank=True)  
    fecha_atencion = models.CharField(max_length=100, null=True, blank=True)  
    fecha_solicitud = models.CharField(max_length=100, null=True, blank=True)  
    fecha_cita = models.CharField(max_length=100, null=True, blank=True)  
    fecha_resultado = models.CharField(max_length=100, null=True, blank=True)  
    num_solicitud = models.CharField(max_length=100, null=True, blank=True)  
    dni_solicita  = models.CharField(max_length=100, null=True, blank=True)
    prof_solicita = models.CharField(max_length=100, null=True, blank=True)
    tipexamen = models.CharField(max_length=100, null=True, blank=True)
    arealab = models.CharField(max_length=100, null=True, blank=True)
    sede = models.CharField(max_length=100, null=True, blank=True)
    examen = models.CharField(max_length=100, null=True, blank=True)
    descexamen = models.CharField(max_length=200, null=True, blank=True)
    dni_profesional = models.CharField(max_length=100, null=True, blank=True)
    profesional = models.CharField(max_length=100, null=True, blank=True)
    dni_paciente = models.CharField(max_length=100, null=True, blank=True)
    h_c = models.CharField(max_length=100, null=True, blank=True)
    paciente = models.CharField(max_length=100, null=True, blank=True)
    telefonos = models.CharField(max_length=100, null=True, blank=True)
    annos = models.CharField(max_length=100, null=True, blank=True)
    meses = models.CharField(max_length=100, null=True, blank=True)
    dias = models.CharField(max_length=100, null=True, blank=True)
    sexo = models.CharField(max_length=100, null=True, blank=True)
    tipo_paciente = models.CharField(max_length=100, null=True, blank=True)
    cas_adscripcion = models.CharField(max_length=100, null=True, blank=True)
    diagnostico = models.CharField(max_length=100, null=True, blank=True)
    des_diagn = models.CharField(max_length=100, null=True, blank=True)
    tip_diagn = models.CharField(max_length=100, null=True, blank=True)
    resultado = models.CharField(max_length=100, null=True, blank=True)
    categoria_resul = models.CharField(max_length=100, null=True, blank=True)
    fecha_registro = models.CharField(max_length=100, null=True, blank=True)  
    usuario_registro = models.CharField(max_length=100, null=True, blank=True)
    informe_resultado = models.CharField(max_length=200, null=True, blank=True)
    orden_plantilla = models.CharField(max_length=100, null=True, blank=True)
    desc_plantilla = models.CharField(max_length=100, null=True, blank=True)
    valor_resultado = models.CharField(max_length=100, null=True, blank=True)
    unidadvalor = models.CharField(max_length=100, null=True, blank=True)
    observresultado = models.CharField(max_length=100, null=True, blank=True)
    usario_modifica = models.CharField(max_length=100, null=True, blank=True)
    fecha_modifica = models.CharField(max_length=100, null=True, blank=True)  
    centro_origen_solicitud = models.CharField(max_length=4, null=True, blank=True)
    codresul_covid = models.CharField(max_length=100, null=True, blank=True)
    resultado_covid = models.CharField(max_length=40, null=True, blank=True)
    hora_registro = models.CharField(max_length=100, null=True, blank=True)
    autogenerado = models.CharField(max_length=100, null=True, blank=True)
    desc_topico = models.CharField(max_length=100, null=True, blank=True)


# PACIENTES GEOLOCALIZACION

class pacienteLocalizacion(models.Model):
    cas = models.ForeignKey(cas, on_delete=models.CASCADE)
    paciente = models.OneToOneField(paciente, on_delete=models.CASCADE, unique=True)
    ubigeo = models.ForeignKey(ubigeo, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=150)
    referencia = models.CharField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=20)
    telefonoAlterno = models.CharField(max_length=20 ,null=True, blank=True)
    latitud = models.CharField(max_length=100)
    longitud = models.CharField(max_length=100)
    cordePac = gis_models.PointField("Location in Map", geography=True, blank=True, null=True,srid=4326, help_text="Point(longitude latitude)")
    userReg = models.CharField(max_length=150)
    fechaReg = models.DateField(auto_now_add=True)

    def __str__(self):
        return (self.direccion)

class movimientoPaciente(models.Model):
    cas = models.ForeignKey(cas, on_delete=models.CASCADE)
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    numSolicitud = models.CharField(max_length=20)
    fechaSolicitud = models.DateField()
    tipoSolicitud = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    userReg = models.CharField(max_length=150)
    fechaReg = models.DateField(auto_now_add=True)

    def __str__(self):
        return (self.numSolicitud)

class solicitud(models.Model):
    cas = models.ForeignKey(cas, on_delete=models.CASCADE)
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    tipoSolicitud = models.CharField(max_length=50)
    respuesta = models.CharField(max_length=50,null=True, blank=True)
    fechaSolicitud = models.DateField()
    fechaRespuesta = models.DateField(null=True, blank=True)
    nuevoTurno = models.CharField(max_length=20,null=True, blank=True)
    fechaReg = models.DateField(auto_now_add=True)
    userReg = models.CharField(max_length=150)
    fechaEdit = models.DateField(null=True, blank=True)
    userEdit = models.CharField(max_length=150, null=True, blank=True)
    motivo = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return (self.tipoSolicitud)

class correos(models.Model):
    cas = models.ForeignKey(cas, on_delete=models.CASCADE)
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
    correo = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return (self.correo)


class unidadAtencion(models.Model):
    codUnidadAtencion = models.CharField(max_length=50)
    UnidadAtencion = models.CharField(max_length=50)

    def __str__(self):
        return (self.codUnidadAtencion)

class programacionTurno(models.Model):
    codProgramacionTurno = models.CharField(max_length=50)
    programacionTurno = models.CharField(max_length=50)
    dias = models.CharField(max_length=20)
    horario = models.TimeField()
    horarioFin = models.TimeField()

    def __str__(self):
        return (self.codProgramacionTurno)

class incidenciaEnfermeriaCabecera(models.Model):
    fechaReg = models.DateField()
    horaReg = models.TimeField()
    usuarioReg = models.CharField(max_length=50)
    fechaEdit = models.DateField()
    usuarioEdit = models.CharField(max_length=50)
    sala = models.CharField(max_length=50)
    descripcionIncidencia = models.CharField(max_length=1000)
    
    def __str__(self):
        return (self.usuarioReg)

class procedimientoEnfermeria(models.Model):
    codProcedimientoEnfermeria = models.CharField(max_length=50)
    procedimientoEnfermeria = models.CharField(max_length=50)
    tipoProcedimientoEnfermeria = models.CharField(max_length=50)
    
    def __str__(self):
        return (self.codProcedimientoEnfermeria)

class incidenciaEnfermeriaDetalle(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    personal = models.ForeignKey(personal, on_delete=models.CASCADE)
    unidadAtencion = models.ForeignKey(unidadAtencion, on_delete=models.CASCADE)
    programacionTurno = models.ForeignKey(programacionTurno, on_delete=models.CASCADE)
    procedimientoEnfermeria = models.ForeignKey(procedimientoEnfermeria, on_delete=models.CASCADE)
    incidenciaEnfermeriaCabecera = models.CharField(max_length=1000)
    
    def __str__(self):
        return (self.incidenciaEnfermeriaCabecera)

class formularioCambioClinica(models.Model):
    fecha = models.CharField(max_length=100)
    paciente_id = models.ForeignKey(paciente, on_delete=models.PROTECT, db_column='paciente_id')  # Asumiendo que Paciente es tu modelo de paciente
    motivo = models.CharField(max_length=200)
    id_cas_1 = models.ForeignKey(cas, on_delete=models.PROTECT, db_column='id_cas_1',related_name='id_cas_1')
    id_cas_2 = models.ForeignKey(cas, on_delete=models.PROTECT, db_column='id_cas_2',related_name='id_cas_2', blank=True, null=True)
    es_titular = models.BooleanField()
    num_doc = models.CharField(max_length=100, blank=True, null=True)
    parentesco = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    id_cambio_clinica = models.AutoField(primary_key=True)
    nombre_parentesco=models.CharField(max_length=100, blank=True, null=True)
    correo=models.CharField(max_length=100, blank=True, null=True)
    tratamiento_datos=models.BooleanField()
    estado=models.BooleanField(blank=True, null=True)
    fecha_resolucion=models.CharField(max_length=100, blank=True, null=True)
    usuario_resolucion=models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Formulario_Cambio_Clinicas'

    def __str__(self):
        return str(self.num_doc)

class formularioCapacitacion(models.Model):
    id_capacitacion = models.AutoField(primary_key=True)
    paciente_id = models.ForeignKey(paciente, on_delete=models.PROTECT, db_column='paciente_id')  # Asumiendo que Paciente es tu modelo de paciente
    telefono_paciente = models.CharField(max_length=100, null=True, blank=True)
    documento_cuidador = models.CharField(max_length=100, null=True, blank=True)
    nombre_cuidador = models.CharField(max_length=100, null=True, blank=True)
    correo_cuidador = models.CharField(max_length=100, null=True, blank=True)
    telefono_cuidador = models.CharField(max_length=100, null=True, blank=True)
    certificado = models.BooleanField()
    fecha_registro = models.CharField(max_length=100)

    class Meta:
        db_table = 'Formulario_capacitacion'

    def __str__(self):
        return str(self.certificado)

class laboratorio(models.Model):
    num_doc=models.CharField(max_length=300, primary_key=True, null=False)
    periodo=models.CharField(max_length=300, null=True)
    ktv=models.CharField(max_length=300, null=True)

    class Meta:
        db_table = 'Asistencial_laboratorio'
    def __str__(self):
        return self.num_doc

class laboratorioKtv(models.Model):
    num_doc=models.CharField(max_length=300, null=False)
    periodo=models.CharField(max_length=300, null=True)
    ktv=models.CharField(max_length=300, null=True)
    tru=models.CharField(max_length=300, null=True)

    class Meta:
        db_table = 'Asistencial_lab_ktv'
    def __str__(self):
        return self.num_doc

class laboratorioTemp(models.Model):
    subactividad = models.CharField(max_length=50, null=True)
    fecha_atencion = models.CharField(max_length=50, null=True)
    fecha_solicitud = models.CharField(max_length=50, null=True)
    fecha_resultado = models.CharField(max_length=30, null=True)
    num_solicitud = models.CharField(max_length=30, null=True)
    dni_paciente = models.CharField(max_length=30, null=True)
    desc_plantilla = models.CharField(max_length=40, null=True)
    unidadvalor = models.CharField(max_length=40, null=True)
    valor_resultado = models.CharField(max_length=40, null=True)
    otrosvalores = models.CharField(max_length=255, null=True)
    descexamen = models.CharField(max_length=350, null=True)
    informe_resultado = models.CharField(max_length=300, null=True)
    autogenerado=models.CharField(max_length=300, null=True)

    class Meta:
        db_table = 'Temp_laboratorio'
    def __str__(self):
        return self.subactividad

class protocoloAnemia(models.Model):
    num_doc = models.CharField(max_length=50, null=True)
    fecha_resultado = models.CharField(max_length=50, null=True)
    hemoglobina = models.CharField(max_length=100, null=True)
    dosis_epo = models.CharField(max_length=50, null=True)
    via = models.CharField(max_length=30, null=True)
    dosis_hierro = models.CharField(max_length=30, null=True)
    observaciones = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = 'Asistencial_protocolo_anemia'
    def __str__(self):
        return self.num_doc

class protocoloTmo(models.Model):
    num_doc = models.CharField(max_length=50, null=True)
    fecha_resultado = models.CharField(max_length=50, null=True)
    calcio = models.CharField(max_length=100, null=True)
    fosforo = models.CharField(max_length=50, null=True)
    paratohormona = models.CharField(max_length=30, null=True)
    carbonato_calcio = models.CharField(max_length=30, null=True)
    sevelamero = models.CharField(max_length=100, null=True)
    calcitriol_ev = models.CharField(max_length=100, null=True)
    calcitriol_vo = models.CharField(max_length=100, null=True)
    paricalcitol = models.CharField(max_length=100, null=True)
    cinacalcet = models.CharField(max_length=100, null=True)
    calcio_endializado = models.CharField(max_length=100, null=True)
    observaciones = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = 'Asistencial_protocolo_tmo'
    def __str__(self):
        return self.num_doc

class protocoloNutricion(models.Model):
    num_doc = models.CharField(max_length=50, null=True)
    fecha_resultado = models.CharField(max_length=50, null=True)
    albumina = models.CharField(max_length=100, null=True)
    masa_corporal = models.CharField(max_length=50, null=True)
    masa_muscular = models.CharField(max_length=30, null=True)
    ingesta_prot_cal = models.CharField(max_length=30, null=True)
    bioquimica = models.CharField(max_length=100, null=True)
    total_criterios = models.CharField(max_length=100, null=True)
    diagnostico = models.CharField(max_length=100, null=True)
    sno = models.CharField(max_length=100, null=True)
    administracion = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = 'Asistencial_protocolo_nutricion'
    def __str__(self):
        return self.num_doc
        
class formularioCenso(models.Model):
    id_censo = models.AutoField(primary_key=True) 
    id_paciente = models.CharField(max_length=50, null=True)
    dni = models.CharField(max_length=50, null=True)
    nombres = models.CharField(max_length=100, null=True)
    ape_pat = models.CharField(max_length=50, null=True)
    ape_mat = models.CharField(max_length=30, null=True)
    telefono = models.CharField(max_length=30, null=True)
    telefono_alterno = models.CharField(max_length=100, null=True)
    latitud = models.CharField(max_length=100, null=True)
    longitud = models.CharField(max_length=100, null=True)
    direccion = models.CharField(max_length=100, null=True)
    id_ubigeo = models.CharField(max_length=100, null=True)
    id_clinica = models.CharField(max_length=100, null=True)
    serologia = models.CharField(max_length=100, null=True)
    frecuencia = models.CharField(max_length=100, null=True)
    turno = models.CharField(max_length=100, null=True)
    fecha_registro = models.CharField(max_length=100, null=True)
    host = models.CharField(max_length=100, null=True)
    usuario = models.CharField(max_length=100, null=True)
    pregunta_1 = models.CharField(max_length=100, null=True)
    pregunta_2 = models.CharField(max_length=100, null=True)
    pregunta_3 = models.CharField(max_length=100, null=True)
    pregunta_4 = models.CharField(max_length=100, null=True)
    pregunta_5 = models.CharField(max_length=100, null=True)
    pregunta_6 = models.CharField(max_length=100, null=True)
    pregunta_7 = models.CharField(max_length=100, null=True)
    pregunta_8 = models.CharField(max_length=100, null=True)
    pregunta_9 = models.CharField(max_length=100, null=True)
    pregunta_10 = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'Formulario_censo'
    def __str__(self):
        return self.dni

class registroCarga(models.Model):
    nombre_archivo = models.CharField(max_length=255, verbose_name='Nombre del Archivo')
    tamano_archivo = models.IntegerField(verbose_name='Tamaño del Archivo (bytes)')
    tipo_archivo = models.CharField(max_length=50, verbose_name='Tipo de Archivo')
    fecha_carga = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga')
    estado = models.CharField(max_length=50, default='Pendiente', verbose_name='Estado de la Carga')
    detalles = models.TextField(blank=True, null=True, verbose_name='Detalles de la Carga')
    usuario = models.CharField(max_length=255, verbose_name='Nombre del usuario')

    class Meta:
        db_table = 'reg_lab_ktv'
    def __str__(self):
        return self.nombre_archivo
