"""CNSR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path as url

from rest_framework import routers, permissions
from Asistencial import views as viewsAsis

from rest_framework_simplejwt import views as jwt_views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path as url

router = routers.DefaultRouter()
router.register(r'paciente', viewsAsis.PacienteViewSet, basename='paciente')
router.register(r'pacienteIndex', viewsAsis.indexPacienteViewSet, basename='paciente_index')
router.register(r'serologiaPaciente', viewsAsis.serologiaPacienteViewSet)
router.register(r'examen', viewsAsis.ExamenViewSet)
router.register(r'archivo', viewsAsis.ArchivoViewSet)
router.register(r'proveedores', viewsAsis.proveedorViewSet)
router.register(r'provMaq', viewsAsis.provMaqViewSet)

router.register(r'personal', viewsAsis.personalViewSet)
router.register(r'dependencia', viewsAsis.dependenciaViewSet)
router.register(r'ambiente', viewsAsis.ambienteViewSet)
router.register(r'incidenciaDsi', viewsAsis.incidenciaDsiViewSet)
router.register(r'maestro', viewsAsis.maestroViewSet)
router.register(r'bienpat', viewsAsis.bienpatViewSet)
router.register(r'bienPersonal', viewsAsis.bienPersonalViewSet)
router.register(r'presAnemia', viewsAsis.presAnemiaViewSet)
router.register(r'adminAnemia', viewsAsis.admiAnemiaViewSet)
router.register(r'exclusionAnemia', viewsAsis.exclusionAnemiaViewSet)
router.register(r'movimientoAnemia', viewsAsis.movimientoAnemiaViewSet)
router.register(r'bienHadware', viewsAsis.bienHadwareViewSet)
router.register(r'bienSoftware', viewsAsis.bienSoftwareViewSet)
router.register(r'bienDetalleMonitor', viewsAsis.bienDetalleMonitorViewSet)
router.register(r'nutricion', viewsAsis.nutricionViewSet)
router.register(r'personalVpn', viewsAsis.personalVpnViewSet)
router.register(r'personalCertificado', viewsAsis.personalCertificadoViewSet)
router.register(r'valGlobalSub', viewsAsis.valGlobalSubViewSet)
router.register(r'usuario', viewsAsis.usuarioViewSet, basename='usuario')
router.register(r'usuarioIndex', viewsAsis.usuarioIndexViewSet, basename='usuario_index')
router.register(r'perfil', viewsAsis.perfilViewSet)
router.register(r'cas', viewsAsis.casViewSet)
router.register(r'delegaciones', viewsAsis.delegacionBienesEstraViewSet)
router.register(r'mestroSap', viewsAsis.maestroMatSapViewSet)
router.register(r'parNutricion', viewsAsis.parNuticionViewSet)
router.register(r'listaEspera', viewsAsis.listaEsperaViewSet)
router.register(r'docuContratados', viewsAsis.docuContratadosViewSet)
router.register(r'parameCentro', viewsAsis.parameCentroViewSet)
router.register(r'parameCentroPuesto', viewsAsis.parameCentroPuestoViewSet)
router.register(r'asigCuposPac', viewsAsis.asigCuposPacViewSet)
router.register(r'asigCuposPacIndex', viewsAsis.asigCuposPacIndexViewSet, basename='asigCuposPacIndex')
router.register(r'asisPacDiario', viewsAsis.asisPacDiarioViewSet)
router.register(r'asisPacDiarioAdicional', viewsAsis.asisPacDiarioAdicionalViewSet)
router.register(r'ubigeo', viewsAsis.ubigeoViewSet)
router.register(r'pacienteGeoTem', viewsAsis.pacienteGeoTemViewSet)
#Servicios APP Movil Hisar
router.register(r'loginAppHisar', viewsAsis.loginAppHisarViewSet)
router.register(r'dpDiario', viewsAsis.dpDiarioViewSet)
router.register(r'examenLaboratorio', viewsAsis.examenLaboratorioViewSet)
# PACIENTES GEOLOCALIZACION
router.register(r'pacienteLocalizacion', viewsAsis.pacienteLocalizacionViewSet)
router.register(r'movimientoPaciente', viewsAsis.movimientoPacienteViewSet)
router.register(r'solicitud', viewsAsis.solicitudViewSet)
router.register(r'correos', viewsAsis.correosViewSet)
router.register(r'unidadAtencion', viewsAsis.unidadAtencionViewSet)
router.register(r'programacionTurno', viewsAsis.programacionTurnoViewSet)
router.register(r'incidenciaEnfermeriaCabecera', viewsAsis.incidenciaEnfermeriaCabeceraViewSet)
router.register(r'procedimientoEnfermeria', viewsAsis.procedimientoEnfermeriaViewSet)
router.register(r'incidenciaEnfermeriaDetalle', viewsAsis.incidenciaEnfermeriaDetalleViewSet)
router.register(r'formularioCambioClinica', viewsAsis.formularioCambioClinicaViewSet)

urlpatterns = [
    path('seguro/', viewsAsis.SeguroViewSet, name = 'seguro'),
    path('users/', viewsAsis.UsersViewSet, name = 'users'),
    path('login/', viewsAsis.LoginViewSet, name = 'login'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('enviar-correo-adj/', viewsAsis.enviar_correo_con_adjunto, name='enviar_correo_adj'),
    path('repAsistenciaPacientes/', viewsAsis.rep_Asistencia_Pacientes, name='rep_Asistencia_Pacientes'),
    path('repInformeNutricion/', viewsAsis.rep_Informe_Nutricion, name='rep_Informe_Nutricion'),
    path('repInformeNutricionAdmin/', viewsAsis.rep_Informe_Nutricion_Admin, name='rep_Informe_Nutricion_Admin'),
    path('rep_cupos/', viewsAsis.rep_cupos, name='rep_cupos'),
    path('rep_cupos_agrupados/', viewsAsis.rep_cupos_agrupados, name='rep_cupos_agrupados'),
    path('generar_lista_disponible/', viewsAsis.generar_lista_disponible, name='generar_lista_disponible'),
    path('carga_masiva_paciente/', viewsAsis.carga_masiva_paciente, name='carga_masiva_paciente'),
    path('generar_confirmacion_liberacion_cupo/', viewsAsis.generar_confirmacion_liberacion_cupo, name='generar_confirmacion_liberacion_cupo'),
    path('generar_reporte_inasistencia/', viewsAsis.generar_reporte_inasistencia, name='generar_reporte_inasistencia'),
    path('generar_turno_actual/', viewsAsis.generar_turno_actual, name='generar_turno_actual'),
    path('generar_actualizar_turno/', viewsAsis.generar_actualizar_turno, name='generar_actualizar_turno'),
    path('generar_lista_pacientes/', viewsAsis.generar_lista_pacientes, name='generar_lista_pacientes'),
    path('generar_liberacion_cupo/', viewsAsis.generar_liberacion_cupo, name='generar_liberacion_cupo'),
    path('generar_lista_pacientes_nuevos/', viewsAsis.generar_lista_pacientes_nuevos, name='generar_lista_pacientes_nuevos')
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)