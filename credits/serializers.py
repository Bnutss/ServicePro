from rest_framework import serializers
from .models import Credit
from datetime import timedelta


class CreditSerializer(serializers.ModelSerializer):
    monthly_payment = serializers.SerializerMethodField()
    next_payment_date = serializers.SerializerMethodField()

    class Meta:
        model = Credit
        fields = ['id', 'debtor_name', 'car_number', 'debtor_phone', 'price', 'initial_payment', 'fuel_type',
                  'credit_term', 'created_at', 'is_closed', 'closed_at', 'monthly_payment', 'next_payment_date']

    def get_monthly_payment(self, obj):
        total_price = float(obj.price)
        initial_payment = float(obj.initial_payment)
        remaining_amount = total_price - initial_payment
        monthly_payment = remaining_amount / obj.credit_term
        return f"{int(monthly_payment):,}".replace(",", " ")

    def get_next_payment_date(self, obj):
        creation_date = obj.created_at
        next_payment_date = creation_date + timedelta(days=30)
        return next_payment_date.strftime('%Y-%m-%d')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price'] = f"{int(float(instance.price)):,}".replace(",", " ")
        representation['initial_payment'] = f"{int(float(instance.initial_payment)):,}".replace(",", " ")
        return representation
