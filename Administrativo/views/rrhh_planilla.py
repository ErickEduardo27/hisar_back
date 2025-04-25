from django.shortcuts import render
from django.shortcuts import get_object_or_404
from Administrativo.models.rrhh_planilla import RrhhPlanillaArea, RrhhPlanillaComponente, RrhhPlanillaRol,RrhhPlanillaUsuario,RrhhPlanillaRolComponentes,AdministrativoRRHHPersonal,AdministrativoRRHHHorario,AdministrativoRRHHPeriodo,AdministrativoRRHHDias,AdministrativoRRHHDiasHorario
from Administrativo.serializers.rrhh_planilla import RrhhPlanillaAreaSerializer, RrhhPlanillaComponenteSerializer, RrhhPlanillaRolSerializer,RrhhPlanillaUsuarioSerializer,RrhhPlanillaRolComponentesSerializer,AdministrativoRRHHPersonalSerializer,AdministrativoRRHHHorarioSerializer,RrhhPlanillaPeriodoSerializer,AdministrativoRRHHDiasSerializer,AdministrativoRRHHDiasHorarioSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets, filters


class RrhhPlanillaAreaViewSet(viewsets.ModelViewSet):
    queryset = RrhhPlanillaArea.objects.all()
    serializer_class = RrhhPlanillaAreaSerializer

class RrhhPlanillaComponenteViewSet(viewsets.ModelViewSet):
    queryset = RrhhPlanillaComponente.objects.all()
    serializer_class = RrhhPlanillaComponenteSerializer

class RrhhPlanillaRolViewSet(viewsets.ModelViewSet):
    queryset = RrhhPlanillaRol.objects.all()
    serializer_class = RrhhPlanillaRolSerializer

class RrhhPlanillaUsuarioViewSet(viewsets.ModelViewSet):
    queryset = RrhhPlanillaUsuario.objects.all().order_by('id')
    serializer_class = RrhhPlanillaUsuarioSerializer

    @action(detail=False, methods=['get'], url_path='buscar-usuario')
    def buscar_por_usuario(self, request):
        usuario = request.query_params.get('usuario', None)
        tipo_param = request.query_params.get('tipo', None)
        estado = request.query_params.get('estado', None)
        if usuario:
            try:
                personal = RrhhPlanillaUsuario.objects.get(usuario_id=usuario)
                serializer = self.get_serializer(personal)
            except RrhhPlanillaUsuario.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=404)

        # Si se proporcionó el parámetro "tipo", se verifica el rol
        if tipo_param and estado:
            try:
                personal = RrhhPlanillaUsuario.objects.filter(rol__nombre=tipo_param, estado=estado)
                serializer = self.get_serializer(personal, many=True)
            except RrhhPlanillaUsuario.DoesNotExist:
                return Response({"error": "Tipo de rol no encontrado"}, status=404)
        return Response(serializer.data)

class RrhhPlanillaRolComponentesViewSet(viewsets.ModelViewSet):
    queryset = RrhhPlanillaRolComponentes.objects.all()
    serializer_class = RrhhPlanillaRolComponentesSerializer

""" class AdministrativoRRHHPersonalViewSet(viewsets.ModelViewSet):
    queryset = AdministrativoRRHHPersonal.objects.all().order_by('id')
    serializer_class = AdministrativoRRHHPersonalSerializer """
    
class AdministrativoRRHHPersonalViewSet(viewsets.ModelViewSet):
    serializer_class = AdministrativoRRHHPersonalSerializer

    def get_queryset(self):
        queryset = AdministrativoRRHHPersonal.objects.all().order_by('id')

        estado = self.request.query_params.get('estado')
        if estado is not None:
            # convierte el string 'true'/'false' en booleano
            if estado.lower() == 'true':
                queryset = queryset.filter(estado=True)
            elif estado.lower() == 'false':
                queryset = queryset.filter(estado=False)

        return queryset

    def list(self, request, *args, **kwargs):
        campos = request.query_params.get('campos')
        queryset = self.get_queryset()

        if campos:
            campos_lista = campos.split(',')
            data = queryset.values(*campos_lista)  # Solo devuelve los campos seleccionados
            return Response(data)
        else:
            # Usa el serializer completo si no se especifican campos
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

class AdministrativoRRHHHorarioViewSet(viewsets.ModelViewSet):
    queryset = AdministrativoRRHHHorario.objects.all()
    serializer_class = AdministrativoRRHHHorarioSerializer

class AdministrativoRRHHPeriodoViewSet(viewsets.ModelViewSet):
    queryset = AdministrativoRRHHPeriodo.objects.all().order_by('id')
    serializer_class = RrhhPlanillaPeriodoSerializer

class AdministrativoRRHHDiasViewSet(viewsets.ModelViewSet):
    queryset = AdministrativoRRHHDias.objects.all().order_by('id')
    serializer_class = AdministrativoRRHHDiasSerializer

    @action(detail=False, methods=['get'], url_path='periodo')
    def buscar_por_periodo(self, request):
        periodo = request.query_params.get('periodo', None)
        if periodo:
            dias = AdministrativoRRHHDias.objects.filter(periodo__periodo=periodo).order_by('numero_dia')
            if dias.exists():
                serializer = self.get_serializer(dias, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "No se encontraron días para el periodo"}, status=404)
        else:
            return Response({"error": "Parámetro 'periodo' es requerido"}, status=400)

class AdministrativoRRHHDiasHorarioViewSet(viewsets.ModelViewSet):
    queryset = AdministrativoRRHHDiasHorario.objects.all().order_by('id')
    serializer_class = AdministrativoRRHHDiasHorarioSerializer

    @action(detail=False, methods=['get'], url_path='periodo_personal')
    def buscar_por_periodo(self, request):
        periodo = request.query_params.get('periodo', None)
        personal = request.query_params.get('personal', None)
        if periodo and personal:
            dias = AdministrativoRRHHDiasHorario.objects.filter(dias__periodo__periodo=periodo,personal_id=personal).order_by('dias__numero_dia')
            if dias.exists():
                serializer = self.get_serializer(dias, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "No se encontraron días para el periodo"}, status=404)
        else:
            return Response({"error": "Parámetro 'periodo' es requerido"}, status=400)