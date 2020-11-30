from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.viewsets import  ViewSet
from .serializer import CuponSerializer, VentaSerializer, DetalleVentaSerializer, ProgramSerializer, HorarioSerializer, UnidadSerializer, SemanaSerializer, PostulanteSerializer,RegisterSerializer, UserSerializer, MatriculaSerializer
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404
from django.utils.timezone import datetime
from .models import Cupon, Programa, Unidad, Horario,  Semana, Postulante, Venta, Detalle_Venta, User, Matricula
from rest_framework import status,generics, permissions
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated


import culqipy

# Create your views here.

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class CuponView(ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def obtener(self, request, *args, **kwargs):
        queryset = Cupon.objects.filter(codigo_cupon=request.query_params.get('codigo_cupon')).filter(fecha_fin__gte=datetime.today()).filter(en_uso=False)
        cupon = get_object_or_404(queryset,codigo_cupon=request.query_params.get('codigo_cupon'))
        serializer = CuponSerializer(cupon)
        return Response(serializer.data)

class ProgramView(viewsets.ModelViewSet):
    queryset = Programa.objects.all()
    serializer_class = ProgramSerializer
    lookup_field = 'slug'
    
    def obtener(self, request, slug=None):
        queryset = Programa.objects.all()
        program = get_object_or_404(queryset, slug=slug)
        serializer = ProgramSerializer(program)
        return Response(serializer.data)

class PostulanteView(viewsets.ModelViewSet):
    queryset = Postulante.objects.all()
    serializer_class = PostulanteSerializer

class UnidadView(ViewSet):
    def list(self,request):
        queryset = Unidad.objects.all()
        serializer = UnidadSerializer(queryset, many=True)
        return Response(serializer.data)

class VentaView(ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        data = request.data
        usuario = get_object_or_404(User, id=data['alumno'])
        cupon = get_object_or_404(Cupon, id=data['cupon'])
        venta = Venta(alumno=usuario, subtotal=data['subtotal'], cupon=cupon, total=data['total'])
        venta.save()

        for programa in data['programas']:
            programa_query = Programa.objects.get(id=programa)
            detalle_venta = Detalle_Venta(venta=venta, programa=programa_query)
            matricula = Matricula(alumno=usuario, programa=programa_query)
            detalle_venta.save()
            matricula.save()

        return Response({
            'message': 'Compra se realizo con exito !'
        })

class ChargeView(ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def pagar(self, request):
        token = request.data.get('token')
        installments = request.data.get('installments')
        amount = request.data.get('amount')
        currency_code = request.data.get('currency_code')
        email = request.data.get('email')

        culqipy.secret_key = 'sk_test_UlRGRO8ZRgMVEmbZ'
        culqipy.public_key = 'pk_test_GYQo25ubIHHzUpOO'

        data_charge = {
            'amount': amount,
            'installments': installments,
            'currency_code': currency_code,
            'email': email,
            'antifraud_details': {
                'dni': 99999999
            },
            'source_id': token
        }

        charge = culqipy.Charge.create(data_charge)

        if charge.get('object') == 'charge':
            return Response({'success' : True})
        
        else:
            message = "Error de pago (code: 1000)"
            return Response({'success': False, 'message': message})

class MatriculaView(viewsets.ModelViewSet):
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer
