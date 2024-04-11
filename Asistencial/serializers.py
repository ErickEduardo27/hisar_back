from django.contrib.auth.models import User, Group
from Asistencial.models import procedimientoEnfermeria,incidenciaEnfermeriaCabecera,programacionTurno,unidadAtencion,correos,solicitud,movimientoPaciente,pacienteLocalizacion,pacienteGeoTem,ubigeo,asisPacDiarioAdicional,examenLaboratorio,dpDiario,loginAppHisar,serologiaPaciente,baseDatosProduccion,asisPacDiario,asigCuposPac,parameCentroPuesto,parameCentro,docuContratados,maestroMatSap,parNuticion,delegacionBienesEstra, cas ,usuario,perfil, paciente, examen, archivo, personalCertificado, presAnemia, admiAnemia, exclusionAnemia, movimientoAnemia, bienAmbiente, bienPersonal, bienpat, dependencia, ambiente, personal, bienImag, proveedor, provMaq, maestro, incidenciaDsi, bienHadware, bienSoftware, bienDetalleMonitor, nutricion, personalVpn, personalCertificado, valGlobalSub, listaEspera,formularioCambioClinica
from rest_framework import serializers

from datetime import datetime
from dateutil.relativedelta import relativedelta

# Pacientes geolocalizados Temporalmente
class pacienteGeoTemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = pacienteGeoTem
        fields = '__all__' 

# Tablas Generales

class ubigeoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ubigeo
        fields = '__all__' 

class casSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = cas
        fields = '__all__' 

class usuarioSerializer(serializers.HyperlinkedModelSerializer):
    datosCas = casSerializer(source = "cas", read_only=True)
    class Meta:
        model = usuario
        fields = '__all__' 
        extra_kwargs = {
            'num_doc': {'required': False},
            'nombre': {'required': False},
            'usuario': {'required': False},
            'clave': {'required': False},
            'perfil_id': {'required': False},
            'cas': {'required': False},
        }

class perfilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = perfil
        fields = '__all__' 
        
class maestroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = maestro
        fields = '__all__' 

class PacienteSerializer(serializers.HyperlinkedModelSerializer):
    datosMaestro = maestroSerializer(source = "tipo_doc", read_only=True)
    datosCasOri = casSerializer(source = "cas", read_only=True)
    edad = serializers.SerializerMethodField('obtain_edad') 
    nombre_completo = serializers.SerializerMethodField()

    def obtain_edad(self, mascota):
        age = relativedelta(datetime.now(), mascota.fecha_nac)
        return age.years,age.months,age.days

    def get_nombre_completo(self, obj):
        return obj.nombre_completo
    
    class Meta:
        model = paciente
        fields = '__all__'

class serologiaPacienteSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source = "paciente", read_only=True)
    class Meta:
        model = serologiaPaciente
        fields = '__all__'

class ExamenSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source = "paciente", read_only=True)
    class Meta:
        model = examen
        fields = '__all__'

class ArchivoSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source = "paciente", read_only=True)
    class Meta:
        model = archivo
        fields = '__all__'

class bienpatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bienpat
        fields = '__all__'

class bienImagSerializer(serializers.HyperlinkedModelSerializer):
    datos_bienpat = bienpatSerializer(source = "bienpat", read_only=True)
    class Meta:
        model = bienImag
        fields = '__all__'
        
#Clinicas Anemia

class presAnemiaSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)
    datosUsuario = usuarioSerializer(source="usuario", read_only=True)     
    class Meta:
        model = presAnemia
        fields = '__all__'

class admiAnemiaSerializer(serializers.HyperlinkedModelSerializer):
    datosPres = presAnemiaSerializer(source="presAnemia", read_only=True)  
    datosUsuario = usuarioSerializer(source="usuario", read_only=True)   
    class Meta:
        model = admiAnemia
        fields = '__all__'

class exclusionAnemiaSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True) 
    datosUsuario = usuarioSerializer(source="usuario", read_only=True)
    class Meta:
        model = exclusionAnemia
        fields = '__all__'

class movimientoAnemiaSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)   
    class Meta:
        model = movimientoAnemia
        fields = '__all__'

class nutricionSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True) 
    datosUsuario = usuarioSerializer(source="usuario", read_only=True)   
    class Meta:
        model = nutricion
        fields = '__all__'

# Hospitales Vgs
class valGlobalSubSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)   
    class Meta:
        model = valGlobalSub
        fields = '__all__'
        
#Inventario

class dependenciaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = dependencia
        fields = '__all__'

class ambienteSerializer(serializers.HyperlinkedModelSerializer):
    datosDependencia = dependenciaSerializer(source = "dependencia", read_only=True)
    class Meta:
        model = ambiente
        fields = '__all__'  

class personalSerializer(serializers.HyperlinkedModelSerializer):
    datosDependencia = dependenciaSerializer(source = "dependencia", read_only=True)
    class Meta:
        model = personal
        fields = '__all__'     

class bienPersonalSerializer(serializers.HyperlinkedModelSerializer):
    datos_bienpat = bienpatSerializer(source = "bienpat", read_only=True)
    datosPersonal = personalSerializer(source = "personal", read_only=True)
    class Meta:
        model = bienPersonal
        fields = '__all__'    

class bienAmbienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bienAmbiente
        fields = '__all__'        

class bienHadwareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bienHadware
        fields = '__all__'  

class bienSoftwareSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bienSoftware
        fields = '__all__'  

class bienDetalleMonitorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = bienDetalleMonitor
        fields = '__all__'   

class proveedorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = proveedor
        fields = '__all__'         

class provMaqSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = provMaq
        fields = '__all__' 

class incidenciaDsiSerializer(serializers.HyperlinkedModelSerializer):
    datosPersonal = personalSerializer(source = "personal", read_only=True)
    datosEstado = maestroSerializer(source = "estado", read_only=True)
    class Meta:
        model = incidenciaDsi
        fields = '__all__' 

class personalVpnSerializer(serializers.HyperlinkedModelSerializer):
    datosPersonal = personalSerializer(source = "personal", read_only=True)
    class Meta:
        model = personalVpn
        fields = '__all__' 

class personalCertificadoSerializer(serializers.HyperlinkedModelSerializer):
    datosPersonal = personalSerializer(source = "personal", read_only=True)
    class Meta:
        model = personalCertificado
        fields = '__all__' 

class delegacionBienesEstraSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = delegacionBienesEstra
        fields = '__all__'

class maestroMatSapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = maestroMatSap
        fields = '__all__'

class parNuticionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = parNuticion
        fields = '__all__'

class listaEsperaSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True) 
    class Meta:
        model = listaEspera
        fields = '__all__'

class docuContratadosSerializer(serializers.HyperlinkedModelSerializer):
    datosCas = casSerializer(source = "cas", read_only=True)
    class Meta:
        model = docuContratados
        fields = '__all__'

class parameCentroSerializer(serializers.HyperlinkedModelSerializer):
    datosCas = casSerializer(source = "cas", read_only=True)
    class Meta:
        model = parameCentro
        fields = '__all__'

class parameCentroPuestoSerializer(serializers.HyperlinkedModelSerializer):
    datosCas = casSerializer(source = "cas", read_only=True)
    class Meta:
        model = parameCentroPuesto
        fields = '__all__'

class asigCuposPacSerializer(serializers.HyperlinkedModelSerializer):
    datosPueto = parameCentroPuestoSerializer(source = "parameCentroPuesto", read_only=True)
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)
    class Meta:
        model = asigCuposPac
        fields = '__all__'

class asisPacDiarioSerializer(serializers.HyperlinkedModelSerializer):
    datosAsigCuposPac = asigCuposPacSerializer(source="asigCuposPac", read_only=True)
    class Meta:
        model = asisPacDiario
        fields = '__all__'

class asisPacDiarioAdicionalSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)
    datosCas = casSerializer(source = "cas", read_only=True)
    class Meta:
        model = asisPacDiarioAdicional
        fields = '__all__'

class baseDatosProduccionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = baseDatosProduccion
        fields = '__all__'

#BACK PARA APLICATIVOS MOVIL

class loginAppHisarSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)
    class Meta:
        model = loginAppHisar
        fields = '__all__'

class dpDiarioSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)
    class Meta:
        model = dpDiario
        fields = '__all__'

class examenLaboratorioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = examenLaboratorio
        fields = '__all__'

class pacienteLocalizacionSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)
    datosCas = casSerializer(source = "cas", read_only=True)
    datosUbigeo = ubigeoSerializer(source = "ubigeo", read_only=True)
    class Meta:
        model = pacienteLocalizacion
        fields = '__all__'

class movimientoPacienteSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)
    datosCas = casSerializer(source = "cas", read_only=True)
    class Meta:
        model = movimientoPaciente
        fields = '__all__'

class solicitudSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)
    datosCas = casSerializer(source = "cas", read_only=True)
    class Meta:
        model = solicitud
        fields = '__all__'

class correosSerializer(serializers.HyperlinkedModelSerializer):
    datosUsuario = usuarioSerializer(source="usuario", read_only=True)
    datosCas = casSerializer(source = "cas", read_only=True)
    class Meta:
        model = correos
        fields = '__all__'

class unidadAtencionSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = unidadAtencion
        fields = '__all__'

class programacionTurnoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = programacionTurno
        fields = '__all__'

class incidenciaEnfermeriaCabeceraSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = incidenciaEnfermeriaCabecera
        fields = '__all__'

class procedimientoEnfermeriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = procedimientoEnfermeria
        fields = '__all__'

class incidenciaEnfermeriaDetalleSerializer(serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)
    datosPersonal = personalSerializer(source="personal", read_only=True)
    datosUnidadAtencion = unidadAtencionSerializer(source="unidadAtencion", read_only=True)
    datosProgramacionTurno = programacionTurnoSerializer(source="ProgramacionTurno", read_only=True)
    datosProcedimientoEnfermeria = procedimientoEnfermeriaSerializer(source="procedimientoEnfermeria", read_only=True)
    datosIncidenciaEnfermeriaCabecera = incidenciaEnfermeriaCabeceraSerializer(source="incidenciaEnfermeriaCabecera", read_only=True)

    class Meta:
        model = procedimientoEnfermeria
        fields = '__all__'

class formularioCambioClinicaSerializer (serializers.HyperlinkedModelSerializer):
    datosPaciente = PacienteSerializer(source="paciente", read_only=True)
    datosCas1 = casSerializer(source="descripCas", read_only=True)
    datosCas2 = casSerializer(source="descripCas", read_only=True)

    class Meta:
        model = formularioCambioClinica
        fields = '__all__'