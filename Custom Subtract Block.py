"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Custom Subtract Block',   # so we may modify it if needed
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.complex64]
        )

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[:] = input_items[0] - input_items[1]
        return len(output_items[0])
