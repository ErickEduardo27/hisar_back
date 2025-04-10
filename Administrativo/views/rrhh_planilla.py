from django.shortcuts import render
from django.shortcuts import get_object_or_404
from Administrativo.models.rrhh_planilla import RrhhPlanillaArea, RrhhPlanillaComponente, RrhhPlanillaRol,RrhhPlanillaUsuario,RrhhPlanillaRolComponentes,AdministrativoRRHHPersonal,AdministrativoRRHHHorario,AdministrativoRRHHPeriodo
from Administrativo.serializers.rrhh_planilla import RrhhPlanillaAreaSerializer, RrhhPlanillaComponenteSerializer, RrhhPlanillaRolSerializer,RrhhPlanillaUsuarioSerializer,RrhhPlanillaRolComponentesSerializer,AdministrativoRRHHPersonalSerializer,AdministrativoRRHHHorarioSerializer,RrhhPlanillaPeriodoSerializer
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response


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

class AdministrativoRRHHPersonalViewSet(viewsets.ModelViewSet):
    queryset = AdministrativoRRHHPersonal.objects.all().order_by('id')
    serializer_class = AdministrativoRRHHPersonalSerializer

class AdministrativoRRHHHorarioViewSet(viewsets.ModelViewSet):
    queryset = AdministrativoRRHHHorario.objects.all()
    serializer_class = AdministrativoRRHHHorarioSerializer

class AdministrativoRRHHPeriodoViewSet(viewsets.ModelViewSet):
    queryset = AdministrativoRRHHPeriodo.objects.all().order_by('id')
    serializer_class = RrhhPlanillaPeriodoSerializer