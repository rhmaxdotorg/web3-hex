from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

    stats = anvil.server.call('getHexStats')
    
    # show stats on main page
    self.stats.text =  "name: " + str(stats[0]) + "\n"
    self.stats.text += "decimals: " + str(stats[1]) + "\n"
    self.stats.text += "totalSupply: " + str(int(stats[2])) + "\n"
    self.stats.text += "shareRate: " + str(int(stats[3])) + "\n"
    self.stats.text += "stakeSharesTotal: " + str(int(stats[4])) + "\n"
    self.stats.text += "currentPrice: " + str("{:0.3f}".format(stats[5]))
