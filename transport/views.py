from rest_framework import viewsets
from .serializer import *
from .models import *
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.db.models import F, ExpressionWrapper, Func
from django.db.models import FloatField
from django.http import JsonResponse


class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UsersProfileSerializer
    queryset = UsersProfile.objects.all()
    
    def create(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
@api_view(['POST'])
def create_account(request):
    
    request.data['password'] = make_password(request.data['password'])
    serializer = UsersProfileSerializer(data=request.data)
    
    if serializer.is_valid():
        user_profile = serializer.save()

        user_type = request.data.get('user_type')
        if user_type == 'driver':
            driver_serializer = DriverSerializer(data={**request.data, 'user_profile': user_profile.id})
            if driver_serializer.is_valid():
                driver_serializer.save()
            else:
                user_profile.delete()
                return Response(driver_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif user_type == 'passenger':
            passenger_serializer = PassengerSerializer(data={**request.data, 'user_profile': user_profile.id})
            if passenger_serializer.is_valid():
                passenger_serializer.save()
            else:
                user_profile.delete()
                return Response(passenger_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        user_name_rq = request.data.get('user_name')
        password_rq = request.data.get('password')
        
        user = UsersProfile.objects.get(user_name=user_name_rq)
        
        if check_password(password_rq, user.password):
            refresh = RefreshToken.for_user(user)

            user_id = user.id
            user_type = user.user_type
            

            response = JsonResponse({
                'user_id': user_id,
                'user_type': user_type
            },status=status.HTTP_200_OK)
            
            response.set_cookie('token', str(refresh.access_token), httponly=True)
            return response
                        
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@api_view(['POST'])
def create_service(request):
    
    user_name = request.data['user_name']
    user = UsersProfile.objects.get(user_name=user_name)
    passenger = Passenger.objects.get(user_profile_id= user.id)
    
    data = {
        'latitude_origin': request.data.get('latitude_origin'),
        'longitude_origin': request.data.get('longitude_origin'),
        'latitude_destination': request.data.get('latitude_destination'),
        'longitude_destination': request.data.get('longitude_destination'),
        'is_active': True,
        'is_finished': False,
        'is_canceled': False,
        'price': 0,
        'driver': None,
        'passenger': passenger.id
    }

    serializer = ServiceSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
@api_view(['POST'])
def get_available_services(request):
    try:
        id_conductor = int(request.data['id_conductor'])

        driver = Driver.objects.get(user_profile=id_conductor) 
        latitude_conductor = driver.latitude
        longitude_conductor = driver.longitude
        
        services_in_range = Service.objects.filter(
            driver__isnull=True,
            is_active=True,
            is_finished=False,
            is_canceled=False,
            latitude_origin__isnull=False,
            longitude_origin__isnull=False,
            latitude_destination__isnull=False,
            longitude_destination__isnull=False
        )
        
        print(services_in_range) 

        services_in_range = services_in_range.annotate(
            distance=Func(
                Func(
                    ExpressionWrapper(
                        F('latitude_origin') - latitude_conductor,
                        output_field=FloatField()
                    ) ** 2 + ExpressionWrapper(
                        F('longitude_origin') - longitude_conductor,
                        output_field=FloatField()
                    ) ** 2,
                    function='POWER',
                    template='%(expressions)s',
                    output_field=FloatField()
                ),
                function='SQRT'
            )
        ).filter(distance__lte=0.01)

        serializer = ServiceSerializer(services_in_range, many=True)
        return JsonResponse({'services': serializer.data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
@api_view(['POST'])
def accept_service(request):
    try:
        id_conductor = int(request.data['id_conductor'])
        id_service_rq = int(request.data['id_service'])
        user_type = request.data['user_type']
        price = float(request.data['price']) 

        if user_type != 'driver':
            return JsonResponse({'error': 'Only drivers can accept services'}, status=400)

        service = Service.objects.get(id=id_service_rq)
        driver = Driver.objects.get(user_profile=id_conductor)
        passenger = Passenger.objects.get(id=service.passenger.id)

        if service.is_active and service.driver is None:
            service.driver = driver
            service.price = price
            service.save()
            
            driver.availability = False
            driver.save()
            
            passenger.on_ride = True
            passenger.save()

            serializer = ServiceSerializer(service)
            return JsonResponse({'service': serializer.data}, status=200)
        else:
            return JsonResponse({'error': 'Service is not available or has already been accepted'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@api_view(['POST'])
def cancel_service(request):
    try:
        user_id_rq = int(request.data['user_id'])
        id_service_rq = int(request.data['id_service'])
        user_type_rq = request.data['user_type']

        if user_type_rq != 'passenger':
            return JsonResponse({'error': 'Only passengers can cancel services'}, status=400)

        user_profile_rq = UsersProfile.objects.get(id=user_id_rq)
        passenger = Passenger.objects.get(user_profile=user_profile_rq)
        service = Service.objects.get(id=id_service_rq)


        if service.is_active and not service.is_canceled:
            
            service.is_active = False
            service.is_canceled = True
            service.save()
            
            passenger.on_ride = False
            passenger.save()

            if service.driver:
                service.driver.availability = True
                service.driver.save()

            return JsonResponse({'message': 'Service canceled successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Service is not active or has already been canceled'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
