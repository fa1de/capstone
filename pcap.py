import re

# TCP 패킷 정규표현식
tcp_packet = re.compile(
    r"##\#[ TCP ]###.*sport\s+=\s+(?P<source_port>\w+).*dport\s+=\s+(?P<dest_port>\w+).*seq\s+=\s+(?P<seq_num>\d+).*ack\s+=\s+(?P<ack_num>\d+)",
    re.DOTALL,
)

# UDP 패킷 정규표현식
udp_packet = re.compile(
    r"##\#[ UDP ]###.*sport\s+=\s+(?P<source_port>\w+).*dport\s+=\s+(?P<dest_port>\w+)",
    re.DOTALL,
)

# ICMP 패킷 정규표현식
icmp_packet = re.compile(
    r"##\#[ ICMP ]###.*type\s+=\s+(?P<type>\d+).*code\s+=\s+(?P<code>\d+).*chksum\s+=\s+(?P<checksum>\w+)",
    re.DOTALL,
)

# DNS 패킷 정규표현식
dns_packet = re.compile(
    r"##\#[ DNS ]###.*qd\s+qname\s+=\s+(?P<query_name>[\w\.]+).*an\s+rdata\s+=\s+(?P<response_data>[\w\.]+)?",
    re.DOTALL,
)

# HTTP 패킷 정규표현식
http_packet = re.compile(
    r"##\#[ HTTP ]###.*Method\s+=\s+(?P<method>\w+).*Path\s+=\s+(?P<uri>[^\s]+).*Http_Version\s+=\s+(?P<version>[^\s]+)",
    re.DOTALL,
)

# FTP 패킷 정규표현식
ftp_packet = re.compile(
    r"##\#[ FTP ]###.*Command\s+=\s+(?P<command>\w+).*Field_A\s+=\s+(?P<username>\w+).*Field_B\s+=\s+(?P<password>\w+)",
    re.DOTALL,
)

# SSH 패킷 정규표현식
ssh_packet = re.compile(
    r"##\#[ SSH ]###.*kex_algorithms\s+=\s+(?P<version>[\w\-]+).*encryption_algorithms_client_to_server\s+=\s+(?P<algorithm>[\w\-]+).*user\s+=\s+(?P<username>\w+)",
    re.DOTALL,
)
