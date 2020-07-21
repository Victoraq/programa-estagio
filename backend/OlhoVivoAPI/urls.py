from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api import views

# settings para documentacao
API_TITLE = 'Olho Vivo API'
API_DESCRIPTION = """
    Clone da API Olho Vivo para teste back-end do programa de estágio da AIKO.
    """

schema_view = get_schema_view(
   openapi.Info(
      title=API_TITLE,
      default_version='v1',
      description=API_DESCRIPTION,
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API paths
    path('parada', views.ParadaList.as_view()),
    path('parada/<int:pk>', views.ParadaDetail.as_view()),
    path('parada/linhasPorParada/<int:pk>', views.linhas_por_parada),
    path('parada/paradasPorPosicao/', views.paradas_por_posicao),
    path('linha', views.LinhaList.as_view()),
    path('linha/<int:pk>', views.LinhaDetail.as_view()),
    path('linha/veiculosPorLinha/<int:pk>', views.veiculos_por_linha),
    path('veiculo', views.VeiculoList.as_view()),
    path('veiculo/<int:pk>', views.VeiculoDetail.as_view()),
    path('posicaoVeiculo', views.PosicaoVeiculoList.as_view()),
    path('posicaoVeiculo/<int:pk>', views.PosicaoVeiculoDetail.as_view()),

    url(r'^(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
]
