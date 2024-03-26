from scapy.all import sniff, wrpcap                   # scapy library에서 sniff, wrpcap 함수를 가져옴
import pyshark                                        # pyshark library를 가져옴

def packet_sniffer(packet):                           # packet_sniffer 함수 정의. packet은 함수에 전달되는 매개변수
    print(packet.summary())                           # 받은 패킷의 요약정보를 출력
    wrpcap('captured_packets.pcap', packet, append=True)  # '파일명' 파일에 pcap형식으로 패킷을 저장. true로 하면 파일 끝에 추가됨

def pyshark_sniffer():                                # pyshark_sniffer 함수 정의.
    capture = pyshark.LiveCapture(interface='ethernet')   # '인터페이스명' 인터페이스에서 실시간으로 패킷캡쳐를 위한 LiveCapture 객체 생성
    
    for packet in capture.sniff_continuously():       # capture객체의 sniff_continuously() method를 사용해 패킷을 지속적으로 받음. 패킷은 반복문에서 처리됨
        print(packet)                                 # 받은 패킷의 정보 출력
        
        with open('captured_packets.txt', 'a') as f:  # '파일명'파일을 열고, f라는 이름으로 파일 객체로 사용. a는 파일을 추가 모드로 열고, 이미 파일 존재시 끝에 내용을 추가
            
            f.write(str(packet) + '\n')               # 파일에 받은 패킷을 문자열로 변환하여 씀. 개행문자 '\n'을 사용해 각 패킷을 새로운 줄에 저장

sniff(prn=packet_sniffer)                             # scapy의 sniff()함수를 호출하여 네트워크 감시. packet_sniffer 함수가 각 패킷을 처리하고 출력하도록 지정
