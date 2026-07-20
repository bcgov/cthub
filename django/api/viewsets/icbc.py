from rest_framework.viewsets import GenericViewSet
from api.token_authentication import CustomTokenAuthentication
from api.models.icbc import IcbcRecord
from api.services.icbc import get_icbc_ev_records
from rest_framework.decorators import action
from rest_framework.response import Response


class IcbcRecordViewset(GenericViewSet):
    authentication_classes = [CustomTokenAuthentication]

    queryset = IcbcRecord.objects.all()

    @action(detail=False, methods=["post"])
    def get_icbc_ev_records(self, request):
        vins = request.data.get("vins")
        icbc_records = get_icbc_ev_records(vins)
        return Response(icbc_records)
