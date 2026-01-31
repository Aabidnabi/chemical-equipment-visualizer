import os
import csv
from django.conf import settings
from django.http import JsonResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import EquipmentDataset, EquipmentData
from .serializers import EquipmentDatasetSerializer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io
import datetime
from collections import Counter

class EquipmentDatasetViewSet(viewsets.ModelViewSet):
    queryset = EquipmentDataset.objects.all().order_by('-upload_date')
    serializer_class = EquipmentDatasetSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        all_datasets = EquipmentDataset.objects.all().order_by('upload_date')
        if all_datasets.count() >= 5:
            datasets_to_delete = all_datasets[:all_datasets.count() - 4]
            for dataset in datasets_to_delete:
                dataset.delete()
        
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        filename = fs.save(file.name, file)
        file_path = fs.path(filename)
        
        try:
            # Read CSV using Python's built-in csv module
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
            
            if not rows:
                return Response({'error': 'CSV file is empty'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract data
            equipment_types = []
            flowrates = []
            pressures = []
            temperatures = []
            equipment_records_data = []
            
            for row in rows:
                equipment_types.append(row.get('Equipment Type', ''))
                flowrate = float(row.get('Flowrate', 0))
                pressure = float(row.get('Pressure', 0))
                temperature = float(row.get('Temperature', 0))
                
                flowrates.append(flowrate)
                pressures.append(pressure)
                temperatures.append(temperature)
                
                equipment_records_data.append({
                    'equipment_name': row.get('Equipment Name', ''),
                    'equipment_type': row.get('Equipment Type', ''),
                    'flowrate': flowrate,
                    'pressure': pressure,
                    'temperature': temperature
                })
            
            # Calculate statistics
            type_counter = Counter(equipment_types)
            
            summary = {
                'total_count': len(rows),
                'equipment_types': dict(type_counter),
                'averages': {
                    'flowrate': sum(flowrates) / len(flowrates) if flowrates else 0,
                    'pressure': sum(pressures) / len(pressures) if pressures else 0,
                    'temperature': sum(temperatures) / len(temperatures) if temperatures else 0
                },
                'ranges': {
                    'flowrate': {'min': min(flowrates) if flowrates else 0, 'max': max(flowrates) if flowrates else 0},
                    'pressure': {'min': min(pressures) if pressures else 0, 'max': max(pressures) if pressures else 0},
                    'temperature': {'min': min(temperatures) if temperatures else 0, 'max': max(temperatures) if temperatures else 0}
                }
            }
            
            # Create dataset record
            dataset = EquipmentDataset.objects.create(
                name=filename,
                file_path=file_path,
                summary_data=summary
            )
            
            # Create equipment records
            equipment_records = []
            for data in equipment_records_data:
                equipment_records.append(EquipmentData(
                    dataset=dataset,
                    equipment_name=data['equipment_name'],
                    equipment_type=data['equipment_type'],
                    flowrate=data['flowrate'],
                    pressure=data['pressure'],
                    temperature=data['temperature']
                ))
            
            EquipmentData.objects.bulk_create(equipment_records)
            
            serializer = self.get_serializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        dataset = self.get_object()
        return Response(dataset.summary_data)
    
    @action(detail=True, methods=['get'])
    def generate_report(self, request, pk=None):
        dataset = self.get_object()
        
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(1*inch, height-1*inch, f"Equipment Analysis Report: {dataset.name}")
        
        pdf.setFont("Helvetica", 10)
        pdf.drawString(1*inch, height-1.25*inch, f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(1*inch, height-1.75*inch, "Summary Statistics:")
        
        pdf.setFont("Helvetica", 10)
        y = height - 2*inch
        summary = dataset.summary_data
        
        pdf.drawString(1.5*inch, y, f"Total Equipment: {summary['total_count']}")
        y -= 0.25*inch
        
        pdf.drawString(1.5*inch, y, "Equipment Type Distribution:")
        y -= 0.2*inch
        
        for eq_type, count in summary['equipment_types'].items():
            pdf.drawString(2*inch, y, f"{eq_type}: {count}")
            y -= 0.2*inch
        
        y -= 0.1*inch
        pdf.drawString(1.5*inch, y, "Average Values:")
        y -= 0.2*inch
        
        for param, value in summary['averages'].items():
            pdf.drawString(2*inch, y, f"{param.capitalize()}: {value:.2f}")
            y -= 0.2*inch
        
        pdf.save()
        buffer.seek(0)
        
        return FileResponse(buffer, as_attachment=True, filename=f"report_{dataset.name}.pdf")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_datasets(request):
    datasets = EquipmentDataset.objects.all().order_by('-upload_date')[:5]
    serializer = EquipmentDatasetSerializer(datasets, many=True)
    return Response(serializer.data)