from scapy.all import sniff
import psutil
from .handlers import handle_packet


def get_interfaces():
    return psutil.net_if_addrs().keys()


def start_sniffer(interface, stop_event):
    def stop_sniffer(packet):
        return stop_event.is_set()

    sniff(prn=handle_packet, iface=interface, stop_filter=stop_sniffer)
