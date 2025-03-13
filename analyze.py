
from xml.etree import ElementTree as ET
import sys

et = ET.parse(sys.argv[1])

totalFlows = 0
lostFlows = 0
totalClients = 0
lostClients = []

for flow in et.findall("FlowStats/Flow"):
    totalFlows += 1
    flowId = flow.get("flowId") 

    for ipv4flow in et.findall("Ipv4FlowClassifier/Flow"):
        if ipv4flow.get("flowId") == flowId:
            break

    srcAdd = ipv4flow.get("sourceAddress")
    srcPrt = ipv4flow.get("sourcePort")
    desAdd = ipv4flow.get("destinationAddress")
    desPrt = ipv4flow.get("destinationPort")
    print(f"FlowID: {flowId} (UDP {srcAdd}/{srcPrt} --> {desAdd}/{desPrt})")
    if srcPrt != "9":
        totalClients += 1

    txBytes = float(flow.get("txBytes"))
    rxBytes = float(flow.get("rxBytes"))

    txDuration = (float(flow.get('timeLastTxPacket')[:-2]) - float(flow.get('timeFirstTxPacket')[:-2]))*1e-9
    rxDuration = (float(flow.get('timeLastRxPacket')[:-2]) - float(flow.get('timeFirstRxPacket')[:-2]))*1e-9

    txBitrate = None if txDuration == 0 else (txBytes*8/txDuration)*1e-3
    rxBitrate = None if rxDuration == 0 else (rxBytes*8/rxDuration)*1e-3
    print("\tTX bitrate: " + (f"{txBitrate:.2f} kbit/s" if txBitrate else "None"))
    print("\tRX bitrate: " + (f"{rxBitrate:.2f} kbit/s" if rxBitrate else "None"))

    txPackets = int(flow.get("txPackets"))
    rxPackets = int(flow.get("rxPackets"))
    print(f"\tTX Packets: {txPackets}")
    print(f"\tRX Packets: {rxPackets}")

    delaySum = float(flow.get("delaySum")[:-2])
    delayMean = None if rxPackets == 0 else delaySum / rxPackets * 1e-9
    print("\tMean Delay: " + (f"{delayMean * 1e3:.2f} ms" if delayMean else "None"))

    lostPackets = int(flow.get("lostPackets"))
    if lostPackets != 0:
        lostFlows += 1
        lostClients.append(srcAdd)
    packetLossRatio = (txPackets - rxPackets) / txPackets * 100
    print(f"\tPacket Loss Ratio: {packetLossRatio:.2f} %")
    
print(f"Lost Flow Ratio: {lostFlows/totalFlows*100:.2f}% ({lostFlows}/{totalFlows})")
print(f"Lost Clients Ratio: {len(lostClients)/totalClients*100:.2f}% ({len(lostClients)}/{totalClients})")
print(f"Lost clients: {lostClients}")

if (len(sys.argv) > 2):
    file = open(f"summarizedData/{sys.argv[2]}.csv", mode = "a" )
    file.write(str(f"{len(lostClients)/totalClients*100:.2f} "))
