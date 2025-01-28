from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4

class TrafficRedirector(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(TrafficRedirector, self).__init__(*args, **kwargs)
        
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        print("dans packet_in_handler")
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        ip = pkt.get_protocol(ipv4.ipv4)

        in_port = msg.match['in_port']

        # Vérifier si le paquet vient du port de `s1`

        print("before if in_port")
        if in_port in [1, 2, 3]:
            
            print("in if in_port")
            # Rediriger les paquets venant de `s1` vers la VNF
            if eth:
                vnf_mac = "02:42:ac:11:00:07"
                vnf_port = 4
                print("in if eth")
                actions = [parser.OFPActionSetField(eth_dst=vnf_mac),
                           parser.OFPActionOutput(vnf_port)]
                match = parser.OFPMatch(in_port=in_port, eth_src=eth.src, eth_dst=eth.dst)
                self.add_flow(datapath, 1, match, actions)
                print(f"Redirected packet from port {in_port} (s1) to VNF: {vnf_mac}")
        else:
            # Si le paquet ne vient pas de `s1`, on ne fait rien (on peut aussi l'ignorer)
            print(f"Packet from port {in_port} ignored (not from s1)")

    def add_flow(self, datapath, priority, match, actions):
        print("dans add_flow")
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)
        print(f"Flow added: priority={priority}, match={match}, actions={actions}")


