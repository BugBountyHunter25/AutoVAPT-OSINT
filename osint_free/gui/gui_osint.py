# import sys
# import os
# current_dir = os.path.dirname(os.path.abspath(__file__))
# project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
# sys.path.insert(0, project_root)

# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout,
#     QLabel, QPushButton, QLineEdit, QTextEdit
# )
# from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
# from osint_free.scripts.run_osint import run_osint_stage
# from pprint import pformat
# from osint_free.core.phone_lookup import lookup_phone_info

# class OSINTWorker(QObject):
#     finished = pyqtSignal(dict)
#     error = pyqtSignal(str)

#     def __init__(self,domain,password,phone):
#         super().__init__()
#         self.domain = domain
#         self.password = password
#         self.phone = phone

#     def run(self):
#         try:
#             result = run_osint_stage(self.domain, self.password if self.password else None)
#             if self.phone:
#                 result["phone_lookup"] = lookup_phone_info(self.phone)
#             self.finished.emit(result)
#         except Exception as e:
#             self.error.emit(str(e))

# class OSINTToolGUI(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("AutoVAPT - Automated OSINT Tool")
#         self.setGeometry(100, 100, 800, 600)

#         self.container = QWidget()
#         self.layout = QVBoxLayout()

#         self.domain_input = QLineEdit()
#         self.domain_input.setPlaceholderText("Enter domain or IP (e.g., www.google.com)")

#         self.password_input = QLineEdit()
#         self.password_input.setPlaceholderText("Enter optional password to test")

#         self.input_phone = QLineEdit()
#         self.input_phone.setPlaceholderText("Enter phone number (e.g., +14155552671)")

#         self.run_button = QPushButton("Run OSINT Scan")
#         self.run_button.clicked.connect(self.run_osint_scan)

#         self.output_area = QTextEdit()
#         self.output_area.setReadOnly(True)

#         self.status_label = QLabel("Status: Ready")

#         self.layout.addWidget(QLabel("Domain/IP:"))
#         self.layout.addWidget(self.domain_input)
#         self.layout.addWidget(QLabel("Password (optional):"))
#         self.layout.addWidget(self.password_input)
#         self.layout.addWidget(QLabel("Phone Number (optional):"))
#         self.layout.addWidget(self.input_phone)
#         self.layout.addWidget(self.run_button)
#         self.layout.addWidget(self.status_label)
#         self.layout.addWidget(QLabel("OSINT Output:"))
#         self.layout.addWidget(self.output_area)

#         self.container.setLayout(self.layout)
#         self.setCentralWidget(self.container)

#     def run_osint_scan(self):
#         domain = self.domain_input.text().strip()
#         password = self.password_input.text().strip()
#         phone = self.input_phone.text().strip()

#         if not domain:
#             self.status_label.setText("Status: Please enter a valid domain or IP.")
#             return

#         self.status_label.setText("Status: Running OSINT scan...")
#         self.output_area.setText("")

#         self.thread = QThread()
#         self.worker = OSINTWorker(domain,password,phone)
#         self.worker.moveToThread(self.thread)

#         self.thread.started.connect(self.worker.run)
#         self.worker.finished.connect(self.display_results)
#         self.worker.error.connect(self.display_error)
#         self.worker.finished.connect(self.thread.quit)
#         self.worker.finished.connect(self.worker.deleteLater)
#         self.thread.finished.connect(self.thread.deleteLater)

#         self.thread.start()

#     def display_results(self, result):
#         formatted = pformat(result)
#         self.output_area.setText(formatted)
#         self.status_label.setText("Status: Scan complete.")

#     def display_error(self, error):
#         self.output_area.setText(f"Error during scan: {error}")
#         self.status_label.setText("Status: Error occurred.")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = OSINTToolGUI()
#     window.show()
#     sys.exit(app.exec())

import sys
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.insert(0, project_root)

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from osint_free.scripts.run_osint import run_osint_stage
from PyQt6.QtGui import QTextCursor
from pprint import pformat
from osint_free.core.phone_lookup import lookup_phone_info

def style_header(title):
    return f"<h2 style='color:#1e90ff;'>{title}</h2>"

def style_item(label, value, color="black"):
    return f"<b>{label}:</b> <span style='color:{color}'>{value}</span><br>"



class OSINTWorker(QObject):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, domain, password, phone):
        super().__init__()
        self.domain = domain
        self.password = password
        self.phone = phone

    def run(self):
        try:
            result = run_osint_stage(self.domain, self.password if self.password else None)
            if self.phone:
                result["phone_lookup"] = lookup_phone_info(self.phone)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class OSINTToolGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoVAPT - Automated OSINT Tool")
        self.setGeometry(100, 100, 800, 600)

        self.container = QWidget()
        self.layout = QVBoxLayout()

        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("Enter domain or IP (e.g., www.google.com)")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter optional password to test")

        self.input_phone = QLineEdit()
        self.input_phone.setPlaceholderText("Enter phone number (e.g., +14155552671)")

        self.run_button = QPushButton("Run OSINT Scan")
        self.run_button.clicked.connect(self.run_osint_scan)

        self.download_button = QPushButton("Download Report as PDF")
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.download_pdf)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)

        self.status_label = QLabel("Status: Ready")

        self.layout.addWidget(QLabel("Domain/IP:"))
        self.layout.addWidget(self.domain_input)
        self.layout.addWidget(QLabel("Password (optional):"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(QLabel("Phone Number (optional):"))
        self.layout.addWidget(self.input_phone)
        self.layout.addWidget(self.run_button)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(QLabel("OSINT Output:"))
        self.layout.addWidget(self.output_area)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        self.latest_result = None

    def run_osint_scan(self):
        domain = self.domain_input.text().strip()
        password = self.password_input.text().strip()
        phone = self.input_phone.text().strip()

        if not domain:
            self.status_label.setText("Status: Please enter a valid domain or IP.")
            return

        self.status_label.setText("Status: Running OSINT scan...")
        self.output_area.setText("")
        self.download_button.setEnabled(False)

        self.thread = QThread()
        self.worker = OSINTWorker(domain, password, phone)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.display_results)
        self.worker.error.connect(self.display_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def display_results(self, result):
        self.latest_result = result
        self.download_button.setEnabled(True)

        # Format the output as HTML
        html_output = ""
        html_output += style_header("🔎 Domain & IP Info")
        html_output += style_item("Domain", result.get("domain", "N/A"))

    # Domain/IP section
        html_output += style_header("🔎 Domain & IP Info")
        html_output += style_item("Domain", result.get("domain", "N/A"))
        html_output += style_item("Resolved IP", result.get("resolved_ip", "N/A"))
        html_output += style_item("DNS Error", result.get("dns_error", "None"), color="red" if result.get("dns_error") else "green")

    # Phone Lookup
        phone_info = result.get("phone_lookup", {})
        if phone_info:
            html_output += style_header("📱 Phone Number Lookup")
            html_output += style_item("Valid", phone_info.get("valid", False), "green" if phone_info.get("valid") else "red")
            html_output += style_item("Carrier", phone_info.get("carrier", "Unknown"))
            html_output += style_item("Country", phone_info.get("country", "N/A"))
            html_output += style_item("Intl Format", phone_info.get("international", "N/A"))
            html_output += style_item("Timezones", ", ".join(phone_info.get("timezone", [])))

    # IP Location Info
        ip_loc = result.get("ip_location", {})
        if ip_loc:
            html_output += style_header("🌐 IP Geolocation")
            html_output += style_item("Country", ip_loc.get("country", "N/A"))
            html_output += style_item("City", ip_loc.get("city", "N/A"))
            html_output += style_item("ISP", ip_loc.get("isp", "N/A"))
            html_output += style_item("Latitude", ip_loc.get("lat", ""))
            html_output += style_item("Longitude", ip_loc.get("lon", ""))
            html_output += style_item("Organization", ip_loc.get("org", "N/A"))

    # Password Check
        html_output += style_header("🔑 Password Pwn Check")
        pwned = result.get("password_pwned", False)
        html_output += style_item("Password Breach", "Yes" if pwned else "No", "red" if pwned else "green")

    # Nmap Port Scan
        html_output += style_header("📡 Nmap Port Scan")
        html_output += f"<pre style='background-color:#f8f8f8;border:1px solid #ccc;padding:5px;'>{result.get('nmap_scan', 'N/A')}</pre>"

    # Whois Info
        whois = result.get("whois", {})
        if whois:
            html_output += style_header("📃 Whois Information")
            html_output += style_item("Registrar", whois.get("registrar", "N/A"))
            html_output += style_item("Org", whois.get("org", "N/A"))
            html_output += style_item("Country", whois.get("country", "N/A"))
            html_output += style_item("Emails", ", ".join(whois.get("emails", [])))
            html_output += style_item("DNSSEC", whois.get("dnssec", "N/A"))

    # Shodan Errors
        shodan = result.get("shodan_data", {})
        if "error" in shodan:
            html_output += style_header("💀 Shodan Error")
            html_output += style_item("Error", shodan["error"], color="red")

    # Subdomains
        subs = result.get("subdomains", [])
        if subs:
            html_output += style_header("🧩 Subdomains")
            html_output += "<ul>" + "".join(f"<li>{s}</li>" for s in subs) + "</ul>"

   # Set styled HTML into output area
        self.output_area.setHtml(html_output)
        self.output_area.moveCursor(QTextCursor.MoveOperation.Start)
        self.status_label.setText("Status: Scan complete.")

    def display_error(self, error):
        self.output_area.setText(f"Error during scan: {error}")
        self.status_label.setText("Status: Error occurred.")

    def download_pdf(self):
        if not self.latest_result:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "osint_report.pdf", "PDF Files (*.pdf)")
        if not file_path:
            return

        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica", 12)
        y = height - 40

        def draw_line(title, value, color="black"):
            nonlocal y
            if y < 50:
                c.showPage()
                y = height - 40
                c.setFont("Helvetica", 12)
            if color == "red":
                c.setFillColorRGB(1, 0, 0)
            elif color == "green":
                c.setFillColorRGB(0, 0.6, 0)
            else:
                c.setFillColorRGB(0, 0, 0)
            c.drawString(40, y, f"{title}: {value}")
            y -= 20

        r = self.latest_result

        c.setTitle("AutoVAPT OSINT Report")
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, y, "AutoVAPT OSINT Report")
        y -= 40
        c.setFont("Helvetica", 12)

        draw_line("Scan Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        draw_line("Domain", r.get("domain", "N/A"))
        draw_line("Resolved IP", r.get("resolved_ip", "N/A"))
        draw_line("DNS Error", r.get("dns_error", "None"), "red" if r.get("dns_error") else "green")

        phone = r.get("phone_lookup", {})
        if phone:
            draw_line("Phone Valid", phone.get("valid", False), "green" if phone.get("valid") else "red")
            draw_line("Carrier", phone.get("carrier", "Unknown"))
            draw_line("Country", phone.get("country", "N/A"))
            draw_line("Intl Format", phone.get("international", "N/A"))

        ip_loc = r.get("ip_location", {})
        if ip_loc:
            draw_line("Country", ip_loc.get("country", "N/A"))
            draw_line("City", ip_loc.get("city", "N/A"))
            draw_line("ISP", ip_loc.get("isp", "N/A"))
            draw_line("Latitude", ip_loc.get("lat", ""))
            draw_line("Longitude", ip_loc.get("lon", ""))
            draw_line("Organization", ip_loc.get("org", "N/A"))

        draw_line("Password Breach", "Yes" if r.get("password_pwned") else "No", "red" if r.get("password_pwned") else "green")
        draw_line("Nmap Scan", "See full text below")

        for line in r.get("nmap_scan", "").splitlines():
            draw_line("", line)

        whois = r.get("whois", {})
        if whois:
            draw_line("Registrar", whois.get("registrar", "N/A"))
            draw_line("Org", whois.get("org", "N/A"))
            draw_line("Country", whois.get("country", "N/A"))
            draw_line("Emails", ", ".join(whois.get("emails", [])))
            draw_line("DNSSEC", whois.get("dnssec", "N/A"))

        shodan = r.get("shodan_data", {})
        if "error" in shodan:
            draw_line("Shodan Error", shodan["error"], "red")

        c.save()
        self.status_label.setText("Status: PDF report saved successfully.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OSINTToolGUI()
    window.show()
    sys.exit(app.exec())
