import re

rules = [
    re.compile(
        r"sport\s+=\s+(?P<source_port>\w+).*dport\s+=\s+(?P<dest_port>\w+).*seq\s+=\s+(?P<seq_num>\d+).*ack\s+=\s+(?P<ack_num>\d+)",
        re.DOTALL,
    )
]
