def extract_packet(packet):
    protocol_info = {}

    if "IP" in packet:
        protocol_info.update(extract_ip_info(packet))
        protocol_info["protocol"] = packet["IP"].proto

    layers = ["TCP", "UDP", "ICMP", "DNS", "HTTP", "FTP", "SSH"]
    extractors = {
        "TCP": extract_transport_info,
        "UDP": extract_transport_info,
        "ICMP": extract_icmp_info,
        "DNS": extract_dns_info,
        "HTTP": extract_http_info,
        "FTP": extract_ftp_info,
        "SSH": extract_ssh_info,
    }

    for layer in layers:
        if packet.haslayer(layer):
            protocol_info["protocol_name"] = layer
            protocol_info.update(extractors[layer](packet))

    protocol_info["packet_data"] = packet.show(dump=True)

    return protocol_info if protocol_info else None


def extract_ip_info(packet):
    return {"source_ip": packet["IP"].src, "target_ip": packet["IP"].dst}


def extract_transport_info(packet):
    transport_info = {}
    if packet.haslayer("TCP"):
        transport_info["source_port"] = packet["TCP"].sport
        transport_info["target_port"] = packet["TCP"].dport
    elif packet.haslayer("UDP"):
        transport_info["source_port"] = packet["UDP"].sport
        transport_info["target_port"] = packet["UDP"].dport
    return transport_info


def extract_icmp_info(packet):
    icmp_layer = packet["ICMP"]
    return {
        "type": icmp_layer.type,
        "code": icmp_layer.code,
        "checksum": icmp_layer.chksum,
        "id": icmp_layer.id,
        "sequence": icmp_layer.seq,
    }


def extract_dns_info(packet):
    dns_info = {}
    if packet["DNS"].qd:
        dns_info["dns_query"] = packet["DNS"].qd.qname.decode("utf-8")
    if packet["DNS"].an:
        # rdata가 이미 문자열인 경우 decode 제거
        dns_info["dns_response"] = str(packet["DNS"].an.rdata)
    return dns_info


def extract_http_info(packet):
    http_layer = packet["HTTP"]
    return {
        "method": http_layer.Method.decode("utf-8"),
        "uri": http_layer.Path.decode("utf-8"),
        "version": http_layer.Http_Version.decode("utf-8"),
    }


def extract_ftp_info(packet):
    ftp_layer = packet["FTP"]
    return {
        "command": ftp_layer.Command.decode("utf-8"),
        "username": ftp_layer.Field_A.decode("utf-8"),
        "password": ftp_layer.Field_B.decode("utf-8"),
    }


def extract_ssh_info(packet):
    ssh_layer = packet["SSH"]
    return {
        "version": ssh_layer.kex_algorithms.decode("utf-8"),
        "algorithm": ssh_layer.encryption_algorithms_client_to_server.decode("utf-8"),
        "username": ssh_layer.user.decode("utf-8"),
    }
