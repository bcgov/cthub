from rest_framework.viewsets import GenericViewSet
from api.token_authentication import CustomTokenAuthentication
from api.models.decoded_vin_record import VpicDecodedVinRecord
from api.services.decoded_vin_record import get_decoded_vins
from rest_framework.decorators import action
from rest_framework.response import Response


class DecodedVinRecordViewset(GenericViewSet):
    authentication_classes = [CustomTokenAuthentication]

    queryset = VpicDecodedVinRecord.objects.all()

    @action(detail=False, methods=["post"])
    def get_decoded_vins(self, request):
        service_name = request.data.get("service_name")
        vins = request.data.get("vins")
        decoded_vins = get_decoded_vins(service_name, vins)
        return Response(decoded_vins)
