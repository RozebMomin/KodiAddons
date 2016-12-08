import xbmc
import xbmcvfs
import xbmcgui
import datetime
import time
import os
import resources.lib.utils as utils
from resources.lib.croniter import croniter
from resources.lib.backup import XbmcBackup

class BackupScheduler:
    monitor = None
    enabled = "false"
    next_run = 0
    restore_point = None
    
    def __init__(self):
        self.monitor = UpdateMonitor(update_method = self.settingsChanged)
        self.enabled = utils.getSetting("enable_scheduler")

        if(self.enabled == "true"):
            self.setup()

    def setup(self):
        #scheduler was turned on, find next run time
        utils.log("scheduler enabled, finding next run time")
        self.findNextRun(time.time())
        
    def start(self):

        #check if a backup should be resumed
        resumeRestore = self._resumeCheck()

        if(resumeRestore):
            restore = XbmcBackup()
            restore.selectRestore(self.restore_point)
            #skip the advanced settings check
            restore.skipAdvanced()
            restore.run(XbmcBackup.Restore)
        
        while(not xbmc.abortRequested):
            
            if(self.enabled == "true"):
                #scheduler is still on
                now = time.time()

                if(self.next_run <= now):
                    progress_mode = int(utils.getSetting('progress_mode'))
                    if(progress_mode != 2):
                        utils.showNotification(utils.getString(30053))
                    
                    backup = XbmcBackup()

                    if(backup.remoteConfigured()):

                        if(int(utils.getSetting('progress_mode')) in [0,1]):
                            backup.run(XbmcBackup.Backup,True)
                        else:
                            backup.run(XbmcBackup.Backup,False)

                        #check if this is a "one-off"
                        if(int(utils.getSetting("schedule_interval")) == 0):
                            #disable the scheduler after this run
                            self.enabled = "false"
                            utils.setSetting('enable_scheduler','false')
                    else:
                        utils.showNotification(utils.getString(30045))
                        
                    #check if we should shut the computer down
                    if(utils.getSetting("cron_shutdown") == 'true'):
                        #wait 10 seconds to make sure all backup processes and files are completed
                        time.sleep(10)
                        xbmc.executebuiltin('ShutDown()')
                    else:
                        #find the next run time like normal
                        self.findNextRun(now)

            xbmc.sleep(500)

        #delete monitor to free up memory
        del self.monitor

    def findNextRun(self,now):
        #find the cron expression and get the next run time
        cron_exp = self.parseSchedule()

        cron_ob = croniter(cron_exp,datetime.datetime.fromtimestamp(now))
        new_run_time = cron_ob.get_next(float)

        if(new_run_time != self.next_run):
            self.next_run = new_run_time
            utils.showNotification(utils.getString(30081) + " " + datetime.datetime.fromtimestamp(self.next_run).strftime('%m-%d-%Y %H:%M'))
            utils.log("scheduler will run again on " + datetime.datetime.fromtimestamp(self.next_run).strftime('%m-%d-%Y %H:%M'))
                
    def settingsChanged(self):
        current_enabled = utils.getSetting("enable_scheduler")
        
        if(current_enabled == "true" and self.enabled == "false"):
            #scheduler was just turned on
            self.enabled = current_enabled
            self.setup()
        elif (current_enabled == "false" and self.enabled == "true"):
            #schedule was turn off
            self.enabled = current_enabled

        if(self.enabled == "true"):
            #always recheck the next run time after an update
            self.findNextRun(time.time())

    def parseSchedule(self):
        schedule_type = int(utils.getSetting("schedule_interval"))
        cron_exp = utils.getSetting("cron_schedule")

        hour_of_day = utils.getSetting("schedule_time")
        hour_of_day = int(hour_of_day[0:2])
        if(schedule_type == 0 or schedule_type == 1):
            #every day
            cron_exp = "0 " + str(hour_of_day) + " * * *"
        elif(schedule_type == 2):
            #once a week
            day_of_week = utils.getSetting("day_of_week")
            cron_exp = "0 " + str(hour_of_day) + " * * " + day_of_week
        elif(schedule_type == 3):
            #first day of month
            cron_exp = "0 " + str(hour_of_day) + " 1 * *"

        return cron_exp

    def _resumeCheck(self):
        shouldContinue = False
        if(xbmcvfs.exists(xbmc.translatePath(utils.data_dir() + "resume.txt"))):
            rFile = xbmcvfs.File(xbmc.translatePath(utils.data_dir() + "resume.txt"),'r')
            self.restore_point = rFile.read()
            rFile.close()
            xbmcvfs.delete(xbmc.translatePath(utils.data_dir() + "resume.txt"))
            shouldContinue = xbmcgui.Dialog().yesno(utils.getString(30042),utils.getString(30043),utils.getString(30044))

        return shouldContinue
        

class UpdateMonitor(xbmc.Monitor):
    update_method = None

    def __init__(self,*args, **kwargs):
        xbmc.Monitor.__init__(self)
        self.update_method = kwargs['update_method']

    def onSettingsChanged(self):
        self.update_method()
        
BackupScheduler().start()
