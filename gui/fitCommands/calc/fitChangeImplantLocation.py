import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class FitChangeImplantLocation(wx.Command):

    def __init__(self, fitID, source):
        wx.Command.__init__(self, True, 'Change Implant Location')
        self.fitID = fitID
        self.source = source
        self.savedSource = None

    def Do(self):
        pyfalog.debug('Doing changing of implant source to {} for fit {}'.format(self.fitID, self.source))
        fit = Fit.getInstance().getFit(self.fitID)
        if self.source == fit.implantSource:
            return False
        self.savedSource = fit.implantSource
        fit.implantSource = self.source
        eos.db.commit()
        return True

    def Undo(self):
        cmd = FitChangeImplantLocation(self.fitID, self.savedSource)
        return cmd.Do()
