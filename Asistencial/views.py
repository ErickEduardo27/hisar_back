from django.shortcuts import render
from Asistencial.models import incidenciaEnfermeriaDetalle,procedimientoEnfermeria,incidenciaEnfermeriaCabecera,programacionTurno,unidadAtencion,correos,solicitud,movimientoPaciente,pacienteLocalizacion,pacienteGeoTem,ubigeo,asisPacDiarioAdicional,examenLaboratorio,dpDiario,loginAppHisar,serologiaPaciente,baseDatosProduccion,asisPacDiario,asigCuposPac,parameCentroPuesto,parameCentro,docuContratados,listaEspera,parNuticion,maestroMatSap,delegacionBienesEstra, cas, usuario,perfil, paciente, examen, archivo, bienAmbiente, bienImag, presAnemia,admiAnemia, exclusionAnemia, movimientoAnemia, bienPersonal, bienpat, dependencia, ambiente, personal, proveedor, provMaq, incidenciaDsi, maestro, bienHadware, bienSoftware, bienDetalleMonitor, nutricion, personalVpn, personalCertificado, valGlobalSub,formularioCambioClinica
from Asistencial.serializers import incidenciaEnfermeriaDetalleSerializer,procedimientoEnfermeriaSerializer,incidenciaEnfermeriaCabeceraSerializer,programacionTurnoSerializer,unidadAtencionSerializer,correosSerializer,solicitudSerializer,movimientoPacienteSerializer,pacienteLocalizacionSerializer,pacienteGeoTemSerializer,ubigeoSerializer,asisPacDiarioAdicionalSerializer,examenLaboratorioSerializer,dpDiarioSerializer,loginAppHisarSerializer,serologiaPacienteSerializer,baseDatosProduccionSerializer,asisPacDiarioSerializer,asigCuposPacSerializer,parameCentroPuestoSerializer,parameCentroSerializer,docuContratadosSerializer,listaEsperaSerializer,parNuticionSerializer,maestroMatSapSerializer,delegacionBienesEstraSerializer, casSerializer ,usuarioSerializer,perfilSerializer, PacienteSerializer, ExamenSerializer, ArchivoSerializer, presAnemiaSerializer, admiAnemiaSerializer, exclusionAnemiaSerializer, movimientoAnemiaSerializer, bienAmbienteSerializer, bienImagSerializer, bienPersonalSerializer, bienpatSerializer, dependenciaSerializer, ambienteSerializer, personalSerializer, proveedorSerializer, provMaqSerializer, incidenciaDsiSerializer, maestroSerializer, bienHadwareSerializer, bienSoftwareSerializer, bienDetalleMonitorSerializer, nutricionSerializer, personalVpnSerializer, personalCertificadoSerializer, valGlobalSubSerializer,formularioCambioClinicaSerializer
from rest_framework import permissions, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
#servicios externos
from django.http import HttpResponse,JsonResponse
import requests
import json
from decouple import config
# Create your views here.
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from rest_framework.permissions import IsAuthenticated

from django.core.mail import EmailMessage
from django.conf import settings
from datetime import date
from django.db import connection
import openpyxl
import json

@api_view(['POST'])
@permission_required([IsAuthenticated])
def rep_Informe_Nutricion_Admin(request):
    body=request.body.decode('utf-8')
    objeto_python = json.loads(body)
     #Calculamos la fecha de hoy
    hoy = date.today()
    fecha_formateada = hoy.strftime("%m-%d-%Y")
    if objeto_python["fecha"]==None :
        fecha=fecha_formateada
    else :
        fecha=objeto_python["fecha"]

    # Importar las clases necesarias
    cursor = connection.cursor()
    sql = 'select "descripCas",usu."nombre",to_char("fechaReg",'+"'YYYY-MM-DD'"+') ,concat("ape_pat",'+"' '"+',"ape_mat",'+"' '"+',"nombres") as paciente ,"turno" ,to_char("fechaIngreso",'+"'YYYY-MM-DD'"+'),to_char("fechaEvaluacion",'+"'YYYY-MM-DD'"+'),date_part('+"'year'"+',CURRENT_DATE)-date_part('+"'year'"+',fecha_nac),peso,talla,imc,"porcentajeCMB","porcentajeEPT","albSerica","ValGlobalSub" as "MIS","ingestaCalorica","ingestaProteica","diagNutricional","interveNutricional","obsNutricion","tipoPaciente"from public."Asistencial_nutricion" nut left join public."Asistencial_paciente" pac on nut.paciente_id=pac.id left join public."Asistencial_cas" cas on cas.id=pac.cas_id left join public. "Asistencial_usuario" usu on nut.usuario_id=usu.id where "fechaEvaluacion">= '+"'"+fecha+"'"

    cursor.execute(sql)
    resultados = cursor.fetchall()
    # Convertir la lista a JSON
    datos = []
    for fila in resultados:
        #print(fila)
        datos.append(dict(zip(('descripCas', 'nombre', 'fechaReg', 'paciente', 'turno', 'fechaIngreso', 'fechaEvaluacion', 'fecha_nac', 'peso', 'talla', 'imc', 'porcentajeCMB', 'porcentajeEPT', 'albSerica', 'MIS', 'ingestaCalorica', 'ingestaProteica', 'diagNutricional', 'interveNutricional', 'obsNutricion'), fila)))
    json_data = json.dumps(datos)

    return HttpResponse(json_data)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def rep_Informe_Nutricion(request):
    body=request.body.decode('utf-8')
    objeto_python = json.loads(body)
     #Calculamos la fecha de hoy
    hoy = date.today()
    fecha_formateada = hoy.strftime("%m-%d-%Y")
    if objeto_python["fecha"]==None :
        fecha=fecha_formateada
    else :
        fecha=objeto_python["fecha"]
    # Importar las clases necesarias
    cursor = connection.cursor()
    sql = 'select "descripCas",usu."nombre",to_char("fechaReg",'+"'YYYY-MM-DD'"+') ,concat("ape_pat",'+"' '"+',"ape_mat",'+"' '"+',"nombres") as paciente ,"turno" ,to_char("fechaIngreso",'+"'YYYY-MM-DD'"+'),to_char("fechaEvaluacion",'+"'YYYY-MM-DD'"+'),date_part('+"'year'"+',CURRENT_DATE)-date_part('+"'year'"+',fecha_nac),peso,talla,imc,"porcentajeCMB","porcentajeEPT","albSerica","ValGlobalSub" as "MIS","ingestaCalorica","ingestaProteica","diagNutricional","interveNutricional","obsNutricion","tipoPaciente"from public."Asistencial_nutricion" nut left join public."Asistencial_paciente" pac on nut.paciente_id=pac.id left join public. "Asistencial_usuario" usu on nut.usuario_id=usu.id left join public."Asistencial_cas" cas on cas.id=usu.cas_id where "fechaEvaluacion">= '+"'"+fecha+"'"+' and "descripCas"= '+"'"+objeto_python["descripCas"]+"'"+' and usu.usuario='+"'"+objeto_python["usuario"]+"'"+'order by "fechaEvaluacion" desc'

    #where "fechaReg"='+"'"+fecha+"'"

    cursor.execute(sql)
    resultados = cursor.fetchall()
    # Convertir la lista a JSON
    datos = []
    for fila in resultados:
        #print(fila)
        datos.append(dict(zip(('descripCas', 'nombre', 'fechaReg', 'paciente', 'turno', 'fechaIngreso', 'fechaEvaluacion', 'fecha_nac', 'peso', 'talla', 'imc', 'porcentajeCMB', 'porcentajeEPT', 'albSerica', 'MIS', 'ingestaCalorica', 'ingestaProteica', 'diagNutricional', 'interveNutricional', 'obsNutricion'), fila)))
    json_data = json.dumps(datos)

    return HttpResponse(json_data)



@api_view(['POST'])
@permission_required([IsAuthenticated])
def rep_Asistencia_Pacientes(request):
    body=request.body.decode('utf-8')
    objeto_python = json.loads(body)
    #Calculamos la fecha de hoy
    hoy = date.today()
    fecha_formateada = hoy.strftime("%m-%d-%Y")

    if objeto_python["fecha"]==None :
        fecha=fecha_formateada
    else :
        fecha=objeto_python["fecha"]
    # Importar las clases necesarias
    cursor = connection.cursor()
    sql = 'select * from generar_reporte_asistencia(%s)'

    cursor.execute(sql, [fecha])

    # Obtener todos los resultados
    resultados = cursor.fetchall()
    # Convertir la lista a JSON
    datos = []
    for fila in resultados:
        #print(fila)
        datos.append(dict(zip(('descripCas', 'frecuencia','turno', 'tipoPuesto', 'sala','estadoAsistencia','observaFalta','fechaReg','paciente','numero','vigSeguro'), fila)))
    json_data = json.dumps(datos)

    return HttpResponse(json_data)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def rep_cupos(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)
            
            # Obtener los valores de la solicitud y asegurarse de que sean del tipo esperado
            clinica_id = objeto_python.get("clinica_id")
            estado = objeto_python.get("estado")
            # Verificar si los valores son None o no están presentes
            

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from generar_reporte_cupos_detalles(%s, %s)'
            cursor.execute(sql, [clinica_id, estado])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('dni', 'pacienteNombre','fecha','usuario','clinica','turno','frecuencia','parameCentroPuesto_id','paciente_id','distrito','numero_totales','numero_asignado','numero_liberado','tipoPuesto'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def rep_cupos_agrupados(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)
            
            # Obtener los valores de la solicitud y asegurarse de que sean del tipo esperado
            clinica_id = objeto_python.get("clinica_id")
            estado = objeto_python.get("estado")
            # Verificar si los valores son None o no están presentes
            

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from generar_reporte_cupos(%s, %s)'
            cursor.execute(sql, [clinica_id, estado])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('distrito','clinica', 'turno','frecuencia','tipoPuesto','numero_totales','numero_asignado','numero_liberado','cas_id'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def generar_confirmacion_liberacion_cupo(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)
            
            # Obtener los valores de la solicitud y asegurarse de que sean del tipo esperado
            asigCuposPac_id = objeto_python.get("asigCuposPac_id")
            perfil = objeto_python.get("perfil")
            # Verificar si los valores son None o no están presentes
            

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from generar_confirmacion_liberacion_cupo(%s,%s)'
            cursor.execute(sql, [asigCuposPac_id,perfil])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('dias'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def generar_reporte_inasistencia(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)
            
            # Obtener los valores de la solicitud y asegurarse de que sean del tipo esperado
            cas_id = objeto_python.get("cas_id")
            # Verificar si los valores son None o no están presentes
            

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from generar_reporte_inasistencia(%s)'
            cursor.execute(sql, [cas_id])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('paciente','frecuencia','turno','clinica','fecha','telefono','telefono_alterno','observacion'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def generar_turno_actual(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)
            
            # Obtener los valores de la solicitud y asegurarse de que sean del tipo esperado
            paciente_id = objeto_python.get("paciente_id")
            # Verificar si los valores son None o no están presentes
            

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from generar_turno_actual(%s)'
            cursor.execute(sql, [paciente_id])

            # Obtener todos los resultados
            resultados = cursor.fetchall()
            print(resultados)
            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('frecuencia','turno','numeroPuesto','tipoPuesto','asigCupoId'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)


@api_view(['POST'])
@permission_required([IsAuthenticated])
def generar_liberacion_cupo(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)
            
            # Obtener los valores de la solicitud y asegurarse de que sean del tipo esperado
            asigcupospac_id = objeto_python.get("asigcupospac_id")
            usuario = objeto_python.get("usuario")
            motivo = objeto_python.get("motivo")

            # Verificar si los valores son None o no están presentes
            

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from generar_liberacion_cupo(%s,%s,%s)'
            cursor.execute(sql, [asigcupospac_id,usuario,motivo])
            
            # Obtener todos los resultados
            resultados = cursor.fetchall()
            print(resultados)
            # Convertir los resultados a formato JSON
            datos = []
            
            for fila in resultados:
                datos.append(dict(zip(('nombres'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def generar_actualizar_turno(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)
            
            # Obtener los valores de la solicitud y asegurarse de que sean del tipo esperado
            id_parameCentroPuesto = objeto_python.get("id_parameCentroPuesto")
            id_asignacioncupo = objeto_python.get("id_asignacioncupo")
            # Verificar si los valores son None o no están presentes
            

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from generar_actualizar_turno(%s,%s)'
            cursor.execute(sql, [id_parameCentroPuesto,id_asignacioncupo])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('frecuencia'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def generar_lista_disponible(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)
            
            # Obtener los valores de la solicitud y asegurarse de que sean del tipo esperado
            clinica_id = objeto_python.get("clinica_id")
            # Verificar si los valores son None o no están presentes

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from generar_lista_disponible(%s)'
            cursor.execute(sql, [clinica_id])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('turno','frecuencia','tipoPuesto','numeroPuesto','id_ParametroCentro'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def generar_lista_pacientes(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)
            
            # Obtener los valores de la solicitud y asegurarse de que sean del tipo esperado
            clinica_id = objeto_python.get("clinica_id")
            # Verificar si los valores son None o no están presentes

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from generar_lista_pacientes(%s)'
            cursor.execute(sql, [clinica_id])

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('nombreCompleto','paciente_id','dni'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

def carga_masiva_paciente(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        try:
            # Aquí procesas los datos del archivo Excel y los guardas en la base de datos
            # Por ejemplo, puedes iterar sobre las filas y guardar cada una como un registro en la base de datos
            workbook = openpyxl.load_workbook(file, read_only=True, data_only=True)
            sheet = workbook.active
            for row in sheet.iter_rows(min_row=2, values_only=True):
                tipo_doc, num_doc, ape_pat, ape_mat, nombres, fecha_nac, sexo, cas_id ,cordePac,direccion,distrito = row

                # Verificar si el paciente ya existe en la base de datos
                paciente_existente = paciente.objects.filter(num_doc=num_doc).first()
                srid = 4326 
                if paciente_existente:
                    # Actualizar los datos del paciente existente
                    paciente_existente.tipo_doc = maestro.objects.get(id=tipo_doc)
                    paciente_existente.num_doc = num_doc
                    paciente_existente.ape_pat = ape_pat
                    paciente_existente.ape_mat = ape_mat
                    paciente_existente.nombres = nombres
                    paciente_existente.fecha_nac = fecha_nac
                    paciente_existente.sexo = sexo
                    paciente_existente.cas = cas.objects.get(id=cas_id)
                    paciente_existente.latitud = cordePac.split(',')[0].strip()
                    paciente_existente.longitud = cordePac.split(',')[1].strip()
                    paciente_existente.cordePac = f"SRID={srid};POINT ({cordePac.split(',')[1].strip()} {cordePac.split(',')[0].strip()})"
                    paciente_existente.direccion = direccion
                    paciente_existente.distrito = distrito
                    paciente_existente.save()
                else:
                    # Crear un nuevo registro de paciente
                    paciente_nuevo = paciente(
                        tipo_doc=maestro.objects.get(id=tipo_doc),
                        num_doc=num_doc,
                        ape_pat=ape_pat,
                        ape_mat=ape_mat,
                        nombres=nombres,
                        fecha_nac=fecha_nac,
                        sexo=sexo,
                        cas=cas.objects.get(id=cas_id),
                        latitud=cordePac.split(',')[0].strip(),
                        longitud=cordePac.split(',')[1].strip(),
                        cordePac = f"SRID={srid};POINT ({cordePac.split(',')[1].strip()} {cordePac.split(',')[0].strip()})",
                        direccion=direccion,
                        distrito=distrito
                    )
                    paciente_nuevo.save()
            return JsonResponse({'message': 'Datos guardados exitosamente.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Debes enviar un archivo.'}, status=400)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def generar_lista_pacientes_nuevos(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud y cargarlo como objeto Python
            body = request.body.decode('utf-8')
            objeto_python = json.loads(body)
            
            # Obtener los valores de la solicitud y asegurarse de que sean del tipo esperado
            

            # Verificar si los valores son None o no están presentes

            # Importar las clases necesarias
            cursor = connection.cursor()
            
            # Definir la consulta SQL y ejecutarla
            sql = 'select * from generar_lista_pacientes_nuevos()'
            cursor.execute(sql)

            # Obtener todos los resultados
            resultados = cursor.fetchall()

            # Convertir los resultados a formato JSON
            datos = []

            for fila in resultados:
                datos.append(dict(zip(('paciente','id','num_doc'), fila)))

            # Convertir la lista de diccionarios a formato JSON
            json_data = json.dumps(datos)
            cadena_sin_escape = json.loads(json_data)
            # Devolver la respuesta JSON
            return JsonResponse(cadena_sin_escape, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error al decodificar el cuerpo de la solicitud JSON."}, status=400)
        except KeyError as e:
            return JsonResponse({"error": f"Clave faltante en el cuerpo de la solicitud: {e}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error interno del servidor: {e}"}, status=500)

    return JsonResponse({"error": "Solicitud no permitida."}, status=405)

@api_view(['POST'])
@permission_required([IsAuthenticated])
def enviar_correo_con_adjunto(request):
    # Crear un objeto EmailMessage
    body_unicode = request.body.decode('utf-8')
    result = json.loads(body_unicode)
    subject = result.get("asunto")
    message = result.get("mensaje")
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [result.get("destinatario")]
    #adjunto = result.get("adjunto")
    msg = EmailMessage(subject, message, from_email, recipient_list)
    msg.content_subtype = 'html'
    msg.body = html_message=result.get("html")
    # Adjuntar un archivo
    # archivo = 'D:\Proyectos2023/HISAR/codigo/back/media/media/imgOriSal/docu.pdf'  # Ruta al archivo que deseas adjuntar
    # msg.attach_file(archivo)
    # Enviar el correo
    msg.send()
    return HttpResponse("Correo enviado exitosamente.")   
##########


@api_view(['POST'])
@permission_required([IsAuthenticated])
def UsersViewSet(request):
    body_unicode = request.body.decode('utf-8')
    result = json.loads(body_unicode)
    response = requests.post(config('URL'),auth = (config('USER'), config('PASSWORD')) ,  json = {
                        "codOpcion": result.get("codOpcion"),
                        "codTipDoc": result.get("codTipDoc"),
                        "numDoc": result.get("numDoc"),
                        "fecNacimiento":result.get("fecNacimiento")
                      })
    users = response.json()
    #print(type(result))
    #print(result.get("codOpcion"))

    return JsonResponse(users)
##########

##########
@api_view(['POST'])  
@permission_required([IsAuthenticated])
def SeguroViewSet(request):
    body_unicode = request.body.decode('utf-8')
    result = json.loads(body_unicode)
    response = requests.get(config('URLS004')+'?tpdoc='+result.get("tpdoc")+'&nrdoc='+result.get("nrdoc")+'&codcentro='+result.get("codcentro")+'&login='+config('LOGINS004')+'&user='+config('USERS004')+'&pass='+config('PASSWORD004'))
    Seguro = response.json()
    #print("algo",Seguro)
    return JsonResponse(Seguro)
##########

##########SERVICIO DE ACCESO ESSI - BACKLOCK
@api_view(['POST'])
@permission_required([IsAuthenticated])
def LoginViewSet(request):
    body_unicode = request.body.decode('utf-8')
    result = json.loads(body_unicode)
    response = requests.post(config('URLL001'),auth = (result.get('Username'), result.get('Password')))
    login = response.json()
    #print(type(result))
    #print(result.get("codOpcion"))

    return JsonResponse(login)
##########

# Pacientes geolocalizados Temporalmente

class pacienteGeoTemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = pacienteGeoTem.objects.all()
    serializer_class = pacienteGeoTemSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=dni']


# Tablas Generales

class ubigeoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ubigeo.objects.all()
    serializer_class = ubigeoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=ubigeo_reniec']

class casViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = cas.objects.all()
    serializer_class = casSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=tipoCas','^estado','=distrito']


class usuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = usuario.objects.all()
    serializer_class = usuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=usuario','=id']

class usuarioIndexViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = usuario.objects.all()
    serializer_class = usuarioSerializer  # Asigna la clase serializadora correspondiente
    
    permission_classes = [permissions.IsAuthenticated]    
    # filter_backends = [filters.SearchFilter]
    search_fields = ['']

class perfilViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = perfil.objects.all()
    serializer_class = perfilSerializer  # Asigna la clase serializadora correspondiente
    
    permission_classes = [permissions.IsAuthenticated]    
    # filter_backends = [filters.SearchFilter]
    search_fields = ['']

# Create your views here.
class maestroViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = maestro.objects.all()
    serializer_class = maestroSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=codMaestro']

class PacienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=num_doc']

class indexPacienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = PacienteSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['num_doc', 'nombres', 'ape_pat', 'ape_mat']

    def get_queryset(self):
        queryset = paciente.objects.all()

        num_doc = self.request.query_params.get('num_doc')
        nombre = self.request.query_params.get('nombre')

        # Aplicar filtros
        if num_doc:
            queryset = queryset.filter(num_doc__icontains=num_doc)
        if nombre:
            queryset = queryset.filter(nombres__icontains=nombre)
            

        # Tomar una rebanada del queryset
        queryset = queryset[:100]

        return queryset

class serologiaPacienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = serologiaPaciente.objects.all()
    serializer_class = serologiaPacienteSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__num_doc']
    
class ExamenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = examen.objects.all().order_by('-id')
    serializer_class = ExamenSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['tipo_exa']

class ArchivoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = archivo.objects.all().order_by('-id')
    serializer_class = ArchivoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id']

class presAnemiaViewSet(viewsets.ModelViewSet):
    queryset = presAnemia.objects.all().order_by('-id')
    serializer_class = presAnemiaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id','=usuario__cas__codCas']

class admiAnemiaViewSet(viewsets.ModelViewSet):
    queryset = admiAnemia.objects.all().order_by('-id')
    serializer_class = admiAnemiaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=presAnemia__paciente__id','=usuario__cas__codCas']

class exclusionAnemiaViewSet(viewsets.ModelViewSet):
    queryset = exclusionAnemia.objects.all().order_by('-id')
    serializer_class = exclusionAnemiaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id','=usuario__cas__codCas']

class movimientoAnemiaViewSet(viewsets.ModelViewSet):
    queryset = movimientoAnemia.objects.all().order_by('-id')
    serializer_class = movimientoAnemiaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id']

class nutricionViewSet(viewsets.ModelViewSet):
    queryset = nutricion.objects.all().order_by('-id')
    serializer_class = nutricionSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id','=usuario__cas__codCas','=pacNuevo']

class valGlobalSubViewSet(viewsets.ModelViewSet):
    queryset = valGlobalSub.objects.all().order_by('-id')
    serializer_class = valGlobalSubSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__id']


class bienpatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienpat.objects.all()
    serializer_class = bienpatSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['codEti']

class dependenciaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = dependencia.objects.all()
    serializer_class = dependenciaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['codDep']

class ambienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ambiente.objects.all()
    serializer_class = ambienteSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=dependencia__id']

class personalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = personal.objects.all()
    serializer_class = personalSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=dniPer']

class bienImagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienImag.objects.all()
    serializer_class = bienImagSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=bienpat__id']

class bienPersonalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienPersonal.objects.all()
    serializer_class = bienPersonalSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=bienpat__id']

class bienAmbienteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienAmbiente.objects.all()
    serializer_class = bienAmbienteSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=bienpat__id']

class bienHadwareViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienHadware.objects.all()
    serializer_class = bienHadwareSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id']

class bienSoftwareViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienSoftware.objects.all()
    serializer_class = bienSoftwareSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id']

class bienDetalleMonitorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = bienDetalleMonitor.objects.all()
    serializer_class = bienDetalleMonitorSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id']

class proveedorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = proveedor.objects.all()
    serializer_class = proveedorSerializer
    permission_classes = [permissions.IsAuthenticated]  
    filter_backends = [filters.SearchFilter]
    search_fields = ['=rucProveedor']

class provMaqViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = provMaq.objects.all()
    serializer_class = provMaqSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']

class incidenciaDsiViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = incidenciaDsi.objects.all().order_by('-id')
    serializer_class = incidenciaDsiSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=personal__dniPer','=estado__descripMaestro']

class personalVpnViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = personalVpn.objects.all().order_by('-id')
    serializer_class = personalVpnSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=personal__dniPer']

class personalCertificadoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = personalCertificado.objects.all().order_by('-id')
    serializer_class = personalCertificadoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=personal__dniPer']

class delegacionBienesEstraViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = delegacionBienesEstra.objects.all().order_by('-id')
    serializer_class = delegacionBienesEstraSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id']

class maestroMatSapViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = maestroMatSap.objects.all().order_by('-id')
    serializer_class = maestroMatSapSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=codSap']

class parNuticionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = parNuticion.objects.all().order_by('-id')
    serializer_class = parNuticionSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    #filter_fields = ['=edad','=sexo']
    search_fields = ['=edad','^sexo']

class listaEsperaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = listaEspera.objects.all().order_by('-id')
    serializer_class = listaEsperaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=distrito','=estado']

class docuContratadosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = docuContratados.objects.all().order_by('-id')
    serializer_class = docuContratadosSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=cas__id','^estado']
class parameCentroViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = parameCentro.objects.all().order_by('-id')
    serializer_class = parameCentroSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=cas__id','^estado']

class parameCentroPuestoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = parameCentroPuesto.objects.all().order_by('-id')
    serializer_class = parameCentroPuestoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=cas__id','^estado']

class asigCuposPacViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = asigCuposPac.objects.all().order_by('-id')
    serializer_class = asigCuposPacSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=parameCentroPuesto__cas__id','=paciente__num_doc','^estado']

class asigCuposPacIndexViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = asigCuposPacSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=parameCentroPuesto__cas_id','=paciente__num_doc','^estado']

    def get_queryset(self):
        queryset = asigCuposPac.objects.all()

        cas = self.request.query_params.get('cas_id')
        nombres = self.request.query_params.get('nombres')
        num_doc = self.request.query_params.get('num_doc')
        # Aplicar filtros
        if cas:
            queryset = queryset.filter(parameCentroPuesto__cas__id=cas)
        if nombres:
            queryset = queryset.filter(paciente__nombres__icontains=nombres)
        if num_doc:
            queryset = queryset.filter(paciente__num_doc__icontains=num_doc)

        # Tomar una rebanada del queryset
        queryset = queryset[:100]

        return queryset


class asisPacDiarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = asisPacDiario.objects.all().order_by('-id')
    serializer_class = asisPacDiarioSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=asigCuposPac__parameCentroPuesto__cas__id','=validacionAsistencia']

class asisPacDiarioAdicionalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = asisPacDiarioAdicional.objects.all().order_by('-id')
    serializer_class = asisPacDiarioAdicionalSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=estadoAsistencia','^cas__id','^fecha_reg']


class baseDatosProduccionViewSet(viewsets.ModelViewSet):
    queryset = baseDatosProduccion.objects.all().order_by('-id')
    serializer_class = baseDatosProduccionSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id',]

#BACK PARA APLICATIVOS MOVIL

class loginAppHisarViewSet(viewsets.ModelViewSet):
    queryset = loginAppHisar.objects.all().order_by('-id')
    serializer_class = loginAppHisarSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=paciente__num_doc']

class dpDiarioViewSet(viewsets.ModelViewSet):
    queryset = dpDiario.objects.all().order_by('-id')
    serializer_class = dpDiarioSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=paciente__num_doc']

class examenLaboratorioViewSet(viewsets.ModelViewSet):
    queryset = examenLaboratorio.objects.all().order_by('-id')
    serializer_class = examenLaboratorioSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id',]

class pacienteLocalizacionViewSet(viewsets.ModelViewSet):
    queryset = pacienteLocalizacion.objects.all().order_by('-id')
    serializer_class = pacienteLocalizacionSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['paciente__num_doc','=id','=userReg',]

class movimientoPacienteViewSet(viewsets.ModelViewSet):
    queryset = movimientoPaciente.objects.all().order_by('-id')
    serializer_class = movimientoPacienteSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id','=cas__id']

class solicitudViewSet(viewsets.ModelViewSet):
    queryset = solicitud.objects.all().order_by('-id')
    serializer_class = solicitudSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=paciente__num_doc','=respuesta','^cas__id']

class correosViewSet(viewsets.ModelViewSet):
    queryset = correos.objects.all().order_by('-id')
    serializer_class = correosSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id',]

class unidadAtencionViewSet(viewsets.ModelViewSet):
    queryset = unidadAtencion.objects.all().order_by('-id')
    serializer_class = unidadAtencionSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id',]

class programacionTurnoViewSet(viewsets.ModelViewSet):
    queryset = programacionTurno.objects.all().order_by('-id')
    serializer_class = programacionTurnoSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id',]


class incidenciaEnfermeriaCabeceraViewSet(viewsets.ModelViewSet):
    queryset = incidenciaEnfermeriaCabecera.objects.all().order_by('-id')
    serializer_class = incidenciaEnfermeriaCabeceraSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id',]

class procedimientoEnfermeriaViewSet(viewsets.ModelViewSet):
    queryset = procedimientoEnfermeria.objects.all().order_by('-id')
    serializer_class = procedimientoEnfermeriaSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id',]

class incidenciaEnfermeriaDetalleViewSet(viewsets.ModelViewSet):
    queryset = incidenciaEnfermeriaDetalle.objects.all().order_by('-id')
    serializer_class = incidenciaEnfermeriaDetalleSerializer
    permission_classes = [permissions.IsAuthenticated]    
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id',]

class formularioCambioClinicaViewSet(viewsets.ModelViewSet):
    queryset = formularioCambioClinica.objects.all()
    serializer_class = formularioCambioClinicaSerializer
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [filters.SearchFilter]
    search_fields = ['=id_cambio_clinica',]