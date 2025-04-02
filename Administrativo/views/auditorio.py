from django.shortcuts import render
from django.shortcuts import get_object_or_404
from Administrativo.models.auditorio import AuditorioArea, AuditorioComponente, AuditorioRol,AuditorioPersonal,AuditorioRolComponentes
from Administrativo.serializers.auditorio import AuditorioAreaSerializer, AuditorioComponenteSerializer, AuditorioRolSerializer,AuditorioPersonalSerializer,AuditorioRolComponentesSerializer
from rest_framework import permissions, viewsets, filters
from django.db import transaction
import re
from datetime import datetime
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
import xlrd
import json
import os
import socket
import time
from decimal import Decimal
from rest_framework.decorators import action
from rest_framework.response import Response


class AuditorioAreaViewSet(viewsets.ModelViewSet):
    queryset = AuditorioArea.objects.all()
    serializer_class = AuditorioAreaSerializer

class AuditorioComponenteViewSet(viewsets.ModelViewSet):
    queryset = AuditorioComponente.objects.all()
    serializer_class = AuditorioComponenteSerializer

class AuditorioRolViewSet(viewsets.ModelViewSet):
    queryset = AuditorioRol.objects.all()
    serializer_class = AuditorioRolSerializer

""" class AuditorioPersonalViewSet(viewsets.ModelViewSet):
    queryset = AuditorioPersonal.objects.all()
    serializer_class = AuditorioPersonalSerializer

    @action(detail=False, methods=['get'], url_path='buscar-usuario')
    def buscar_por_usuario(self, request):
        usuario = request.query_params.get('usuario', None)
        tipo = request.query_params.get('tipo', None)
        if usuario:
            try:
                personal = AuditorioPersonal.objects.get(usuario_id=usuario)
                tipo = AuditorioRol.objects.get(nombre=tipo)
                serializer = self.get_serializer(personal)
                return Response(serializer.data)
            except AuditorioPersonal.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=404)
        return Response({"error": "Debe proporcionar un usuario"}, status=400) """

class AuditorioPersonalViewSet(viewsets.ModelViewSet):
    queryset = AuditorioPersonal.objects.all().order_by('id')
    serializer_class = AuditorioPersonalSerializer

    @action(detail=False, methods=['get'], url_path='buscar-usuario')
    def buscar_por_usuario(self, request):
        usuario = request.query_params.get('usuario', None)
        tipo_param = request.query_params.get('tipo', None)
        estado = request.query_params.get('estado', None)
        if usuario:
            try:
                personal = AuditorioPersonal.objects.get(usuario_id=usuario)
                serializer = self.get_serializer(personal)
            except AuditorioPersonal.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=404)

        # Si se proporcionó el parámetro "tipo", se verifica el rol
        if tipo_param and estado:
            try:
                personal = AuditorioPersonal.objects.filter(rol__nombre=tipo_param, estado=estado)
                serializer = self.get_serializer(personal, many=True)
            except AuditorioPersonal.DoesNotExist:
                return Response({"error": "Tipo de rol no encontrado"}, status=404)
        return Response(serializer.data)


class AuditorioRolComponentesViewSet(viewsets.ModelViewSet):
    queryset = AuditorioRolComponentes.objects.all()
    serializer_class = AuditorioRolComponentesSerializer