import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import Slot
from scapy.all import sniff, wrpcap
import pyshark
import psutil

class PacketSnifferGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Packet Sniffer")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.interface_label = QLabel("Select Interface:")
        layout.addWidget(self.interface_label)

        self.interface_combobox = QComboBox()
        layout.addWidget(self.interface_combobox)

        self.method_label = QLabel("Choose the method:")
        layout.addWidget(self.method_label)

        self.method_combobox = QComboBox()
        self.method_combobox.addItems(["Scapy", "PyShark"])
        layout.addWidget(self.method_combobox)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_sniffing)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_sniffing)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        self.log_label = QLabel("Log:")
        layout.addWidget(self.log_label)

        self.log_textedit = QTextEdit()
        layout.addWidget(self.log_textedit)

        self.is_sniffing = False
        self.selected_interface = None
        self.selected_method = None

        self.update_interfaces()

    def update_interfaces(self):
        interfaces = psutil.net_if_addrs().keys()
        self.interface_combobox.addItems(interfaces)

    @Slot()
    def start_sniffing(self):
        if self.is_sniffing:
            self.log_textedit.append("Sniffing is already started.")
            return

        self.selected_interface = self.interface_combobox.currentText()
        self.selected_method = self.method_combobox.currentText()

        if self.selected_method == "Scapy":
            self.start_scapy_sniffing()
        elif self.selected_method == "PyShark":
            self.start_pyshark_sniffing()
        else:
            self.log_textedit.append("Invalid method selected.")

    def start_scapy_sniffing(self):
        self.is_sniffing = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        sniff(prn=self.packet_sniffer, iface=self.selected_interface)

    def start_pyshark_sniffing(self):
        self.is_sniffing = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        capture = pyshark.LiveCapture(interface=self.selected_interface)
        for packet in capture.sniff_continuously():
            self.log_textedit.append(str(packet))

    @Slot()
    def stop_sniffing(self):
        if not self.is_sniffing:
            self.log_textedit.append("Sniffing is not started.")
            return

        self.is_sniffing = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def packet_sniffer(self, packet):
        self.log_textedit.append(packet.summary())
        wrpcap('capscapy_packets.pcap', packet, append=True)

def main():
    app = QApplication(sys.argv)
    window = PacketSnifferGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
