import re

tcp_packet = re.compile(
    r"sport\s+=\s+(?P<source_port>\w+).*dport\s+=\s+(?P<dest_port>\w+).*seq\s+=\s+(?P<seq_num>\d+).*ack\s+=\s+(?P<ack_num>\d+)",
    re.DOTALL,
)

udp_packet = re.compile(
    r"sport\s+=\s+(?P<source_port>\w+).*dport\s+=\s+(?P<dest_port>\w+)",
    re.DOTALL,
)

icmp_packet = re.compile(
    r"type\s+=\s+(?P<type>\d+).*code\s+=\s+(?P<code>\d+).*chksum\s+=\s+(?P<checksum>\w+)",
    re.DOTALL,
)

dns_packet = re.compile(
    r"qd\s+qname\s+=\s+(?P<query_name>[\w\.]+).*an\s+rdata\s+=\s+(?P<response_data>[\w\.]+)?",
    re.DOTALL,
)

http_packet = re.compile(
    r"Method\s+=\s+(?P<method>\w+).*Path\s+=\s+(?P<uri>[^\s]+).*Http_Version\s+=\s+(?P<version>[^\s]+)",
    re.DOTALL,
)

ftp_packet = re.compile(
    r"Command\s+=\s+(?P<command>\w+).*Field_A\s+=\s+(?P<username>\w+).*Field_B\s+=\s+(?P<password>\w+)",
    re.DOTALL,
)

ssh_packet = re.compile(
    r"kex_algorithms\s+=\s+(?P<version>[\w\-]+).*encryption_algorithms_client_to_server\s+=\s+(?P<algorithm>[\w\-]+).*user\s+=\s+(?P<username>\w+)",
    re.DOTALL,
)