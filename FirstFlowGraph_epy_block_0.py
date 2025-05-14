"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import pmt
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Custom Difference Block',   # so we may modify it if needed
            in_sig=[np.float32, np.float32],
            out_sig=[np.float32] 
        )
        self.message_port_register_out(pmt.intern("delay_msg"))

    def work(self, input_items, output_items):
        """example: multiply with constant"""
       	main_stream = input_items[0]
        delay_stream = input_items[1]
        
        #when you multiply the arrays, one "rotates"
        correlation = np.correlate(main_stream, delay_stream, mode='full')
        u_index = np.argmax(correlation)
        
        delay = u_index - (len(delay_stream) - 1)
        # bug fix ----- random source samples na 2k, nakolko sa rozdeluju na dva prudy moze
        # blbnut
        msg = pmt.cons(pmt.PMT_NIL, pmt.from_long(delay))
        self.message_port_pub(pmt.intern("delay_msg"), msg)
        
        print("delay value:", delay)
	
        output_items[0][:] = np.full_like(output_items[0], delay)
        return len(output_items[0])
        
