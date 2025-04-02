from rest_framework import serializers
from Administrativo.models.auditorio import AuditorioArea,AuditorioComponente,AuditorioRol,AuditorioPersonal, AuditorioRolComponentes

class AuditorioAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditorioArea
        fields = '__all__'

class AuditorioComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditorioComponente
        fields = '__all__'

class AuditorioRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditorioRol
        fields = '__all__'

class AuditorioPersonalSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(source='rol.nombre', read_only=True)
    area = serializers.CharField(source='area.nombre', read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(queryset=AuditorioRol.objects.all(), source="rol")
    area_id = serializers.PrimaryKeyRelatedField(queryset=AuditorioArea.objects.all(), source="area")
    componentes = serializers.SerializerMethodField()

    class Meta:
        model = AuditorioPersonal
        fields = ['id', 'correo', 'estado', 'nombre', 'usuario_id', 'rol', 'area','rol_id','area_id', 'componentes']

    def get_componentes(self, obj):
        componentes = AuditorioRolComponentes.objects.filter(rol=obj.rol).select_related('componente')
        
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

class AuditorioRolComponentesSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(source='rol.nombre', read_only=True)
    componente = serializers.CharField(source='componente.nombre', read_only=True)

    class Meta:
        model = AuditorioRolComponentes
        fields = ['id', 'rol', 'componente']