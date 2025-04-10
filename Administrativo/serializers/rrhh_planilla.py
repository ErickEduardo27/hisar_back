from rest_framework import serializers
from Administrativo.models.rrhh_planilla import RrhhPlanillaUsuario,RrhhPlanillaRol,RrhhPlanillaArea,RrhhPlanillaComponente, RrhhPlanillaRolComponentes,AdministrativoRRHHPersonal,AdministrativoRRHHHorario,AdministrativoRRHHPeriodo

class RrhhPlanillaAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RrhhPlanillaArea
        fields = '__all__'

class RrhhPlanillaComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RrhhPlanillaComponente
        fields = '__all__'

class RrhhPlanillaRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = RrhhPlanillaRol
        fields = '__all__'

class RrhhPlanillaUsuarioSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(source='rol.nombre', read_only=True)
    area = serializers.CharField(source='area.nombre', read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(queryset=RrhhPlanillaRol.objects.all(), source="rol")
    area_id = serializers.PrimaryKeyRelatedField(queryset=RrhhPlanillaArea.objects.all(), source="area")
    componentes = serializers.SerializerMethodField()

    class Meta:
        model = RrhhPlanillaUsuario
        fields = ['id', 'correo', 'estado', 'nombre', 'usuario_id', 'rol', 'area','rol_id','area_id', 'componentes']

    def get_componentes(self, obj):
        componentes = RrhhPlanillaRolComponentes.objects.filter(rol=obj.rol).select_related('componente')
        
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

class RrhhPlanillaRolComponentesSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(source='rol.nombre', read_only=True)
    componente = serializers.CharField(source='componente.nombre', read_only=True)

    class Meta:
        model = RrhhPlanillaRolComponentes
        fields = ['id', 'rol', 'componente']

class AdministrativoRRHHPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativoRRHHPersonal
        fields = '__all__'  # O puedes listar solo los campos específicos

class AdministrativoRRHHHorarioSerializer(serializers.ModelSerializer):
    fecha_creacion = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    fecha_edicion = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    class Meta:
        model = AdministrativoRRHHHorario
        fields = '__all__'

class RrhhPlanillaPeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativoRRHHPeriodo
        fields = '__all__'