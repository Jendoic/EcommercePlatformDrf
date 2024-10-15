from rest_framework import serializers

from payment import Payment
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__' 