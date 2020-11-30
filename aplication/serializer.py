from .models import Cupon, Venta, Detalle_Venta, Unidad, Programa, Semana,Programa, Horario,  Postulante, Matricula
from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.timezone import datetime



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')

# Serializador de registro
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(first_name=validated_data['first_name'], email=validated_data['email'], password=validated_data['password'], username=validated_data['email'])
        return user

    def validate_email(self,data):
        users = User.objects.filter(email = data)
        if len(users)!= 0:
            raise serializers.ValidationError("El correo electrónico ya existe, ingrese uno nuevo")
        else :
            return data
            
class CuponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cupon
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalle_Venta
        fields = '__all__'

class PostulanteSerializer(serializers.ModelSerializer):
    fecha_hora = serializers.DateTimeField(format="%d-%m-%Y / %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = Postulante
        fields = ['id','nombre_postulante','celular','correo','programa','fecha_hora']

class HorarioSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Horario
        fields = ['dias','horario']

class SemanaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semana
        fields = '__all__'

class UnidadSerializer(serializers.ModelSerializer):
    semanas = SemanaSerializer(many=True, read_only=True, source="semana_set")
    class Meta:
        model = Unidad
        fields = ['nombre_unidad','semanas']

class ProgramSerializer(serializers.ModelSerializer):
    unidades = UnidadSerializer(many=True, read_only=True, source="unidad_set")
    horarios = HorarioSerializer(many=True, read_only=True, source='horario_set')
    class Meta:
        model = Programa
        fields = ['portada','horarios','id','nombre_programa','unidades','estado', 'slug','precio']

class MatriculaSerializer(serializers.ModelSerializer):
    programa = ProgramSerializer(many=False, read_only=True)
    alumno = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Matricula
        fields = ['id','alumno','programa']
