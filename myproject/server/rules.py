import re
from cap import extract_protocol_info

p = re.match ('TCP', extract_protocol_info)