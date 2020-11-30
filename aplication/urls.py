from django.urls import path, include
from rest_framework import routers
from .views import  ChargeView, CuponView, VentaView,  RegisterAPI, LoginAPI, ProgramView, PostulanteView, MatriculaView
from knox import views as knox_views


router = routers.DefaultRouter(trailing_slash=False)

router.register('programas', ProgramView, basename="programa")
router.register('postulantes', PostulanteView, basename="postulante")
router.register('matriculas', MatriculaView, basename="matricula")

urlpatterns = [
    path('cupon-validate',CuponView.as_view({'get':'obtener'}), name = 'cupon.validate'),
    path('purchase',VentaView.as_view({'post':'create'}), name = 'create.venta'),
    path('programas/<str:slug>/', ProgramView.as_view({'get':'obtener'}),name='program.details'),
    
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    #path('culqi-pagar',ChargeView.as_view({'post':'pagar'}), name = 'culqi.pagar'),
]

urlpatterns += router.urls