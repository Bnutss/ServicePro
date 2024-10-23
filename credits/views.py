from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Credit
from .serializers import CreditSerializer


class CreditListCreateView(APIView):
    def get(self, request):
        credits = Credit.objects.all()
        serializer = CreditSerializer(credits, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreditDetailView(APIView):
    def get(self, request, pk):
        credit = get_object_or_404(Credit, pk=pk)
        serializer = CreditSerializer(credit)
        return Response(serializer.data)

    def put(self, request, pk):
        credit = get_object_or_404(Credit, pk=pk)
        serializer = CreditSerializer(credit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        credit = get_object_or_404(Credit, pk=pk)
        credit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Метод для закрытия кредита
    def patch(self, request, pk):
        credit = get_object_or_404(Credit, pk=pk)
        if not credit.is_closed:
            credit.is_closed = True
            credit.save()
            return Response({'status': 'Кредит закрыт'}, status=status.HTTP_200_OK)
        return Response({'status': 'Кредит уже закрыт'}, status=status.HTTP_400_BAD_REQUEST)
