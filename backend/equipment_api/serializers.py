from rest_framework import serializers
from .models import EquipmentDataset, EquipmentData

class EquipmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentData
        fields = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class EquipmentDatasetSerializer(serializers.ModelSerializer):
    records = EquipmentDataSerializer(many=True, read_only=True)
    
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'name', 'upload_date', 'summary_data', 'records']