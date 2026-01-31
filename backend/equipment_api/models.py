from django.db import models
import uuid

class EquipmentDataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=500)
    summary_data = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.name} - {self.upload_date.date()}"

class EquipmentData(models.Model):
    dataset = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE, related_name='records')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    class Meta:
        ordering = ['equipment_name']