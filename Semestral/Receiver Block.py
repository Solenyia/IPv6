import numpy as np
import pmt
from gnuradio import gr

class blk(gr.sync_block):
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Receiver',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        
        self.delay = 0
        self.enabled = False
        
        self.message_port_register_in(pmt.intern("delay_msg"))
        self.set_msg_handler(pmt.intern("delay_msg"), self.handle_msg)
        
        self.message_port_register_in(pmt.intern("toggle"))
        self.set_msg_handler(pmt.intern("toggle"), self.handle_toggle)

    def handle_toggle(self, msg):
    
        if pmt.is_pair(msg):
        	msg = pmt.cdr(msg)
        	
        self.enabled = not self.enabled
        state = "ON" if self.enabled else "OFF"
        print(f"[Receiver] Correction toggled {state}")
        

    def set_enabled(self, value):
        self.enabled = bool(value)
        print(f"Correction state: {'ON' if self.enabled else 'OFF'}")
    	
    def handle_msg(self, msg):
        if pmt.is_pair(msg):
            msg = pmt.cdr(msg)
        if pmt.is_integer(msg):
            self.delay = pmt.to_long(msg)
            print(f"[Receiver] Delay received: {self.delay}")
        
    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        noutput = len(out)
        
        if not self.enabled:
            out[:] = in0[:noutput].astype(np.uint8)
            return noutput

        delay = max(min(self.delay, len(in0) - 1), -len(in0) + 1)

        if delay >= 0:
            if len(in0) > delay + noutput:
                out[:] = in0[delay:delay + noutput].astype(np.uint8)
            else:
                out[:] = np.zeros(noutput, dtype=np.uint8)
        else:
            advance = abs(delay)
            if len(in0) > noutput:
                out[:] = in0[advance:advance + noutput].astype(np.uint8)
            else:
                out[:] = np.zeros(noutput, dtype=np.uint8)

        return noutput

