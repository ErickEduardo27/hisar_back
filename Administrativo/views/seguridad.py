from django.shortcuts import render
from django.shortcuts import get_object_or_404
from Administrativo.models.seguridad import SeguridadArea, SeguridadComponente, SeguridadRol,SeguridadUsuario,SeguridadRolComponentes,SeguridadSystem
from Administrativo.serializers.seguridad import SeguridadAreaSerializer, SeguridadComponenteSerializer, SeguridadRolSerializer,SeguridadUsuarioSerializer,SeguridadRolComponentesSerializer,SeguridadSystemSerializer
from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response


class SeguridadAreaViewSet(viewsets.ModelViewSet):
    queryset = SeguridadArea.objects.all()
    serializer_class = SeguridadAreaSerializer

class SeguridadComponenteViewSet(viewsets.ModelViewSet):
    queryset = SeguridadComponente.objects.all()
    serializer_class = SeguridadComponenteSerializer

class SeguridadRolViewSet(viewsets.ModelViewSet):
    queryset = SeguridadRol.objects.all()
    serializer_class = SeguridadRolSerializer

class SeguridadUsuarioViewSet(viewsets.ModelViewSet):
    queryset = SeguridadUsuario.objects.all().order_by('id')
    serializer_class = SeguridadUsuarioSerializer

    @action(detail=False, methods=['get'], url_path='buscar-usuario')
    def buscar_por_usuario(self, request):
        usuario = request.query_params.get('usuario', None)
        tipo_param = request.query_params.get('tipo', None)
        estado = request.query_params.get('estado', None)
        if usuario:
            try:
                personal = SeguridadUsuario.objects.get(usuario_id=usuario)
                serializer = self.get_serializer(personal)
            except SeguridadUsuario.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=404)

        # Si se proporcionó el parámetro "tipo", se verifica el rol
        if tipo_param and estado:
            try:
                personal = SeguridadUsuario.objects.filter(rol__nombre=tipo_param, estado=estado)
                serializer = self.get_serializer(personal, many=True)
            except SeguridadUsuario.DoesNotExist:
                return Response({"error": "Tipo de rol no encontrado"}, status=404)
        return Response(serializer.data)


class SeguridadRolComponentesViewSet(viewsets.ModelViewSet):
    queryset = SeguridadRolComponentes.objects.all()
    serializer_class = SeguridadRolComponentesSerializer

class SeguridadSystemViewSet(viewsets.ModelViewSet):
    queryset = SeguridadSystem.objects.all()
    serializer_class = SeguridadSystemSerializer