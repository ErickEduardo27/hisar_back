from rest_framework import serializers
from Administrativo.models.seguridad import SeguridadArea,SeguridadRol,SeguridadArea,SeguridadComponente, SeguridadRolComponentes,SeguridadSystem,SeguridadUsuario

class SeguridadAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguridadArea
        fields = '__all__'

class SeguridadComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguridadComponente
        fields = '__all__'

class SeguridadSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguridadSystem
        fields = '__all__'

class SeguridadRolSerializer(serializers.ModelSerializer):
    system = serializers.CharField(source='system.nombre', read_only=True)
    system_id = serializers.PrimaryKeyRelatedField(queryset=SeguridadSystem.objects.all(), source="system")

    class Meta:
        model = SeguridadRol
        fields = '__all__'

class SeguridadUsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(source='rol.nombre', read_only=True)
    area = serializers.CharField(source='area.nombre', read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(queryset=SeguridadRol.objects.all(), source="rol")
    area_id = serializers.PrimaryKeyRelatedField(queryset=SeguridadArea.objects.all(), source="area")
    componentes = serializers.SerializerMethodField()
    fecha_creacion = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    fecha_edicion = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = SeguridadUsuario
        fields = ['id', 'correo', 'estado', 'nombre', 'usuario_id', 'rol', 'area','rol_id','area_id', 'componentes','fecha_creacion','fecha_edicion']

    def get_componentes(self, obj):
        componentes = SeguridadRolComponentes.objects.filter(rol=obj.rol).select_related('componente')
        
        return [
            {
                "id": comp.componente.id,
                "nombre": comp.componente.nombre,
                "descripcion": comp.componente.descripcion,
                "path": comp.componente.path,
                "padre_id": comp.componente.padre_id,
                "icon": comp.componente.icon
            }
            for comp in componentes
        ]

class SeguridadRolComponentesSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(source='rol.nombre', read_only=True)
    componente = serializers.CharField(source='componente.nombre', read_only=True)

    class Meta:
        model = SeguridadRolComponentes
        fields = ['id', 'rol', 'componente']