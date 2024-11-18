import re

rules = [
    
    #TCP-https
    re.compile(
        r"flags\s*=\s*(?P<flag>(SA|FA|PA|RA|S|F|R|P|C|E|A))",
        re.DOTALL,
    ),
    
    #DNS
    re.compile(
        r"qname\s*=\s*(?P<qname>'[\w\.\-]+')",
        re.DOTALL,
    ),
    
    #ICMP
    re.compile(
        r"type\s*=\s*(?P<type>[a-zA-Z\-]+(?:-[a-zA-Z]+)*)\s*code\s*=\s*(?P<code>\d+)", 
        re.DOTALL,
    ),
    
    #TCP/UDP
    re.compile(
        r"sport\s+=\s+(?P<source_port>\w+).*dport\s+=\s+(?P<dest_port>\w+)",
        re.DOTALL,
    ),
    
]