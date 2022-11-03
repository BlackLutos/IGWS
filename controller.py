# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.topology.api import get_link
from ryu.topology import event, switches
import json


from ryu.app import simple_switch_13
from ryu.app.wsgi import ControllerBase
from ryu.app.wsgi import Response
from ryu.app.wsgi import route
from ryu.app.wsgi import WSGIApplication
from ryu.lib import dpid as dpid_lib

simple_switch_instance_name = 'simple_switch_api_app'
url = '/simpleswitch/mactable/{dpid}'

# sudo ryu-manager --observe-links controller.py ryu.app.ofctl_rest
class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    _CONTEXTS = {'wsgi': WSGIApplication} # rest

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.topology_api_app = self 
        self.link_to_port = {}

        # Rest
        # self.switches = {}
        # wsgi = kwargs['wsgi']
        # wsgi.register(SimpleSwitchController,
        #               {simple_switch_instance_name: self})
        # Rest

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Rest

        # self.switches[datapath.id] = datapath
        # self.mac_to_port.setdefault(datapath.id, {})

        # Rest



        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
    
    # def set_mac_to_port(self, dpid, entry):
    #     mac_table = self.mac_to_port.setdefault(dpid, {})
    #     datapath = self.switches.get(dpid)

    #     entry_port = entry['port']
    #     entry_mac = entry['mac']

    #     if datapath is not None:
    #         parser = datapath.ofproto_parser
    #         if entry_port not in mac_table.values():

    #             for mac, port in mac_table.items():

    #                 # from known device to new device
    #                 actions = [parser.OFPActionOutput(entry_port)]
    #                 match = parser.OFPMatch(in_port=port, eth_dst=entry_mac)
    #                 self.add_flow(datapath, 1, match, actions)

    #                 # from new device to known device
    #                 actions = [parser.OFPActionOutput(port)]
    #                 match = parser.OFPMatch(in_port=entry_port, eth_dst=mac)
    #                 self.add_flow(datapath, 1, match, actions)

    #             mac_table.update({entry_mac: entry_port})
    #     return mac_table

        

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    def get_topo(self):
        links_list = get_link(self.topology_api_app, None)
        for link in links_list:
            self.link_to_port[str(link.src.dpid)] = \
            str(link.dst.dpid)
        # print(self.link_to_port)
    # @set_ev_cls(event.EventSwitchEnter)
    # def switch_enter(self, ev):

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        # if len(self.link_to_port)!=0:
        #     print(self.link_to_port)
        self.get_topo()
        if len(self.link_to_port)!=0:
            print(self.link_to_port)
            print(type(self.link_to_port))
            with open('./wan_detect/link_info.json', 'w') as link_info:
                link_info.write(json.dumps(self.link_to_port))
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = format(datapath.id, "d").zfill(16)
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
        
        # learn a mac address to avoid FLOOD next time.        
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        # datapath.send_msg(out)
# ///
# class SimpleSwitchController(ControllerBase):

#     def __init__(self, req, link, data, **config):
#         super(SimpleSwitchController, self).__init__(req, link, data, **config)
#         self.simple_switch_app = data[simple_switch_instance_name]

#     @route('simpleswitch', url, methods=['GET'],
#            requirements={'dpid': dpid_lib.DPID_PATTERN})
#     def list_mac_table(self, req, **kwargs):

#         simple_switch = self.simple_switch_app
#         dpid = kwargs['dpid']

#         if dpid not in simple_switch.mac_to_port:
#             return Response(status=404)

#         mac_table = simple_switch.mac_to_port.get(dpid, {})
#         body = json.dumps(mac_table)
#         return Response(content_type='application/json', text=body)

#     @route('simpleswitch', url, methods=['PUT'],
#            requirements={'dpid': dpid_lib.DPID_PATTERN})
#     def put_mac_table(self, req, **kwargs):

#         simple_switch = self.simple_switch_app
#         dpid = kwargs['dpid']
#         try:
#             new_entry = req.json if req.body else {}
#         except ValueError:
#             raise Response(status=400)

#         if dpid not in simple_switch.mac_to_port:
#             return Response(status=404)

#         try:
#             mac_table = simple_switch.set_mac_to_port(dpid, new_entry)
#             body = json.dumps(mac_table)
#             return Response(content_type='application/json', text=body)
#         except Exception as e:
#             return Response(status=500)
