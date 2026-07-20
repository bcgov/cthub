from rest_framework.viewsets import GenericViewSet
from api.token_authentication import CustomTokenAuthentication
from api.models.icbc import IcbcRecord
from api.services.icbc import get_icbc_ev_records, temp1, temp2, temp3
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

    @action(detail=False, methods=["post"])
    def temp(self, request):
        vins = request.data.get("vins")
        selection = request.data.get("selection")
        if selection == "temp1":
            icbc_records = temp1(vins)
        elif selection == "temp2":
            icbc_records = temp2(vins)
        elif selection == "temp3":
            icbc_records = temp3(vins)
        return Response(icbc_records)
