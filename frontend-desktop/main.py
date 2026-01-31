import sys
import requests
import traceback
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QTableWidget,
                             QTableWidgetItem, QLabel, QMessageBox, QTabWidget,
                             QGroupBox, QListWidget, QProgressBar, QHeaderView, 
                             QGridLayout, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette, QPainter
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis
from PyQt5.QtChart import QPieSeries, QLineSeries, QValueAxis, QCategoryAxis
from datetime import datetime

class WorkerThread(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, url, file_path, auth):
        super().__init__()
        self.url = url
        self.file_path = file_path
        self.auth = auth
    
    def run(self):
        try:
            with open(self.file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    self.url,
                    files=files,
                    auth=self.auth,
                    timeout=30
                )
                response.raise_for_status()
                self.finished.emit(response.json())
        except Exception as e:
            self.error.emit(str(e))

class EquipmentVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_dataset = None
        self.history = []
        self.auth = ('admin', 'password123')
        self.base_url = 'http://localhost:8000/api'
        self.init_ui()
        self.load_history()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Parameter Visualizer - Desktop')
        self.setGeometry(100, 100, 1400, 800)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #333;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:hover {
                background-color: #f0f7ff;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
            }
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        # Upload section
        upload_group = QGroupBox("📤 Upload CSV")
        upload_layout = QVBoxLayout()
        
        self.upload_btn = QPushButton("📁 Select CSV File")
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        upload_layout.addWidget(self.upload_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        upload_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready to upload")
        self.status_label.setStyleSheet("color: #666; padding: 5px; font-size: 12px;")
        upload_layout.addWidget(self.status_label)
        
        upload_group.setLayout(upload_layout)
        left_layout.addWidget(upload_group)
        
        # History section
        history_group = QGroupBox("📋 Recent Datasets")
        history_layout = QVBoxLayout()
        
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.select_dataset)
        history_layout.addWidget(self.history_list)
        
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_history)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #607d8b;
                color: white;
            }
            QPushButton:hover {
                background-color: #546e7a;
            }
        """)
        button_layout.addWidget(self.refresh_btn)
        
        self.report_btn = QPushButton("📄 Generate PDF")
        self.report_btn.clicked.connect(self.generate_report)
        self.report_btn.setEnabled(False)
        self.report_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
            }
            QPushButton:hover:enabled {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        button_layout.addWidget(self.report_btn)
        
        history_layout.addLayout(button_layout)
        history_group.setLayout(history_layout)
        left_layout.addWidget(history_group)
        
        left_layout.addStretch()
        
        # Main content area
        self.tab_widget = QTabWidget()
        
        # Summary tab
        summary_tab = QWidget()
        summary_layout = QVBoxLayout()
        
        # Summary statistics
        self.summary_group = QGroupBox("📊 Summary Statistics")
        self.summary_layout = QVBoxLayout()
        self.summary_content = QLabel("Upload a CSV file to see summary statistics")
        self.summary_content.setFont(QFont("Arial", 10))
        self.summary_content.setStyleSheet("padding: 20px; color: #666;")
        self.summary_layout.addWidget(self.summary_content)
        self.summary_group.setLayout(self.summary_layout)
        summary_layout.addWidget(self.summary_group)
        
        # Charts container
        self.charts_container = QWidget()
        self.charts_layout = QGridLayout()
        self.charts_container.setLayout(self.charts_layout)
        summary_layout.addWidget(self.charts_container)
        
        summary_tab.setLayout(summary_layout)
        
        # Data table tab
        table_tab = QWidget()
        table_layout = QVBoxLayout()
        
        self.table = QTableWidget()
        table_layout.addWidget(self.table)
        
        table_tab.setLayout(table_layout)
        
        self.tab_widget.addTab(summary_tab, "📈 Summary & Charts")
        self.tab_widget.addTab(table_tab, "📋 Data Table")
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(self.tab_widget, 3)
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.status_label.setText("Uploading...")
            self.upload_btn.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            
            self.worker = WorkerThread(
                f"{self.base_url}/datasets/",
                file_path,
                self.auth
            )
            self.worker.finished.connect(self.on_upload_success)
            self.worker.error.connect(self.on_upload_error)
            self.worker.start()
    
    def on_upload_success(self, data):
        self.current_dataset = data
        self.status_label.setText("✓ Upload successful!")
        self.status_label.setStyleSheet("color: #4CAF50; padding: 5px; font-weight: bold; font-size: 12px;")
        self.upload_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.display_data()
        self.load_history()
        QMessageBox.information(self, "Success", "File uploaded and analyzed successfully!")
    
    def on_upload_error(self, error):
        self.status_label.setText("✗ Upload failed")
        self.status_label.setStyleSheet("color: #f44336; padding: 5px; font-size: 12px;")
        self.upload_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Upload Error", f"Error: {str(error)}")
    
    def load_history(self):
        try:
            response = requests.get(
                f"{self.base_url}/history/",
                auth=self.auth,
                timeout=10
            )
            response.raise_for_status()
            self.history = response.json()
            self.history_list.clear()
            
            for dataset in self.history:
                date_str = datetime.fromisoformat(dataset['upload_date'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
                item_text = f"{dataset['name']}\nUploaded: {date_str}\nRecords: {dataset['summary_data']['total_count']}"
                self.history_list.addItem(item_text)
                
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to load history: {e}")
    
    def select_dataset(self, item):
        index = self.history_list.currentRow()
        if index < len(self.history):
            self.current_dataset = self.history[index]
            self.display_data()
            self.report_btn.setEnabled(True)
    
    def display_data(self):
        if not self.current_dataset:
            return
        
        # Update summary
        summary = self.current_dataset['summary_data']
        summary_text = f"""
        <div style='font-size: 12px;'>
        <b>📊 Dataset Summary</b><br><br>
        
        <b>📈 Equipment Overview:</b><br>
        • Total Equipment: <b>{summary['total_count']}</b><br>
        • Equipment Types: <b>{len(summary['equipment_types'])}</b><br><br>
        
        <b>⚖️ Type Distribution:</b><br>
        """
        
        for eq_type, count in summary['equipment_types'].items():
            summary_text += f"• {eq_type}: {count} units<br>"
        
        summary_text += f"""<br>
        <b>📏 Average Values:</b><br>
        • Flowrate: <b>{summary['averages']['flowrate']:.2f}</b><br>
        • Pressure: <b>{summary['averages']['pressure']:.2f}</b><br>
        • Temperature: <b>{summary['averages']['temperature']:.2f}</b><br><br>
        
        <b>📊 Value Ranges:</b><br>
        • Flowrate: {summary['ranges']['flowrate']['min']:.2f} - {summary['ranges']['flowrate']['max']:.2f}<br>
        • Pressure: {summary['ranges']['pressure']['min']:.2f} - {summary['ranges']['pressure']['max']:.2f}<br>
        • Temperature: {summary['ranges']['temperature']['min']:.2f} - {summary['ranges']['temperature']['max']:.2f}<br>
        </div>
        """
        
        self.summary_content.setText(summary_text)
        
        # Update charts
        self.update_charts()
        
        # Update table
        self.update_table()
    
    def update_charts(self):
        # Clear existing charts
        for i in reversed(range(self.charts_layout.count())): 
            widget = self.charts_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        summary = self.current_dataset['summary_data']
        
        # Create Bar Chart
        bar_chart = QChart()
        bar_chart.setTitle("Equipment Type Distribution")
        bar_chart.setAnimationOptions(QChart.SeriesAnimations)
        
        bar_set = QBarSet("Count")
        categories = []
        
        for eq_type, count in summary['equipment_types'].items():
            bar_set.append(count)
            categories.append(eq_type)
        
        bar_series = QBarSeries()
        bar_series.append(bar_set)
        bar_chart.addSeries(bar_series)
        
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        bar_chart.addAxis(axis_x, Qt.AlignBottom)
        bar_series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        bar_chart.addAxis(axis_y, Qt.AlignLeft)
        bar_series.attachAxis(axis_y)
        
        bar_chart_view = QChartView(bar_chart)
        bar_chart_view.setRenderHint(QPainter.Antialiasing)
        
        # Create Parameter Chart
        line_chart = QChart()
        line_chart.setTitle("Parameter Analysis")
        line_chart.setAnimationOptions(QChart.SeriesAnimations)
        
        parameters = ['Flowrate', 'Pressure', 'Temperature']
        min_values = [
            summary['ranges']['flowrate']['min'],
            summary['ranges']['pressure']['min'],
            summary['ranges']['temperature']['min']
        ]
        max_values = [
            summary['ranges']['flowrate']['max'],
            summary['ranges']['pressure']['max'],
            summary['ranges']['temperature']['max']
        ]
        avg_values = [
            summary['averages']['flowrate'],
            summary['averages']['pressure'],
            summary['averages']['temperature']
        ]
        
        # Min series
        min_series = QLineSeries()
        min_series.setName("Min")
        for i, value in enumerate(min_values):
            min_series.append(i, value)
        
        # Max series
        max_series = QLineSeries()
        max_series.setName("Max")
        for i, value in enumerate(max_values):
            max_series.append(i, value)
        
        # Avg series
        avg_series = QLineSeries()
        avg_series.setName("Average")
        for i, value in enumerate(avg_values):
            avg_series.append(i, value)
        
        line_chart.addSeries(min_series)
        line_chart.addSeries(max_series)
        line_chart.addSeries(avg_series)
        
        axis_x_line = QCategoryAxis()
        for i, param in enumerate(parameters):
            axis_x_line.append(param, i)
        axis_x_line.setRange(0, len(parameters)-1)
        line_chart.addAxis(axis_x_line, Qt.AlignBottom)
        min_series.attachAxis(axis_x_line)
        max_series.attachAxis(axis_x_line)
        avg_series.attachAxis(axis_x_line)
        
        axis_y_line = QValueAxis()
        line_chart.addAxis(axis_y_line, Qt.AlignLeft)
        min_series.attachAxis(axis_y_line)
        max_series.attachAxis(axis_y_line)
        avg_series.attachAxis(axis_y_line)
        
        line_chart_view = QChartView(line_chart)
        line_chart_view.setRenderHint(QPainter.Antialiasing)
        
        # Add charts to layout
        self.charts_layout.addWidget(bar_chart_view, 0, 0)
        self.charts_layout.addWidget(line_chart_view, 0, 1)
    
    def update_table(self):
        records = self.current_dataset['records']
        self.table.setRowCount(len(records))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
        ])
        
        for row, record in enumerate(records):
            self.table.setItem(row, 0, QTableWidgetItem(record['equipment_name']))
            self.table.setItem(row, 1, QTableWidgetItem(record['equipment_type']))
            self.table.setItem(row, 2, QTableWidgetItem(f"{record['flowrate']:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{record['pressure']:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{record['temperature']:.2f}"))
        
        self.table.resizeColumnsToContents()
    
    def generate_report(self):
        if not self.current_dataset:
            return
        
        try:
            response = requests.get(
                f"{self.base_url}/datasets/{self.current_dataset['id']}/generate_report/",
                auth=self.auth,
                stream=True,
                timeout=30
            )
            response.raise_for_status()
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save PDF Report", 
                f"equipment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", 
                "PDF Files (*.pdf)"
            )
            
            if file_path:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                QMessageBox.information(self, "Success", f"PDF report saved to:\n{file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report:\n{str(e)}")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(245, 247, 250))
    palette.setColor(QPalette.WindowText, QColor(33, 33, 33))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(245, 247, 250))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(33, 33, 33))
    palette.setColor(QPalette.Text, QColor(33, 33, 33))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(33, 33, 33))
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(102, 126, 234))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = EquipmentVisualizer()
    window.show()
    
    # Check backend connection
    try:
        requests.get('http://localhost:8000/api/history/', auth=('admin', 'password123'), timeout=2)
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Backend Server Not Found")
        msg.setInformativeText("Please ensure the Django backend is running on http://localhost:8000")
        msg.setWindowTitle("Connection Error")
        msg.exec_()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()