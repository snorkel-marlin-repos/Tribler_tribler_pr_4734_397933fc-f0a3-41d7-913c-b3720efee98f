from __future__ import absolute_import

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from TriblerGUI.utilities import get_gui_setting
from TriblerGUI.widgets.tablecontentmodel import ChannelsContentModel
from TriblerGUI.widgets.triblertablecontrollers import ChannelsTableViewController


class DiscoveredPage(QWidget):
    """
    The DiscoveredPage shows an overview of all discovered channels in Tribler.
    """

    def __init__(self):
        QWidget.__init__(self)
        self.initialized = False
        self.model = None
        self.controller = None
        self.gui_settings = None

    def initialize_discovered_page(self, gui_settings):
        if not self.initialized:
            self.initialized = True
            self.gui_settings = gui_settings
            self.window().core_manager.events_manager.discovered_channel.connect(self.on_discovered_channel)
            self.model = ChannelsContentModel(hide_xxx=get_gui_setting(self.gui_settings, "family_filter", True,
                                                                       is_bool=True) if self.gui_settings else True)
            self.window().core_manager.events_manager.node_info_updated.connect(self.model.update_node_info)
            # Set the default sorting column/order to num_torrents/descending
            default_sort_column = self.model.columns.index(u'votes')
            self.window().discovered_channels_list.horizontalHeader().setSortIndicator(
                default_sort_column, Qt.AscendingOrder)
            self.controller = ChannelsTableViewController(self.model, self.window().discovered_channels_list,
                                                          self.window().num_discovered_channels_label,
                                                          self.window().discovered_channels_filter_input)

    def load_discovered_channels(self):
        self.controller.model.reset()
        self.controller.perform_query(first=1, last=50)  # Load the first 50 discovered channels

    def on_discovered_channel(self, channels):
        self.controller.on_query_results(channels, remote=True)
