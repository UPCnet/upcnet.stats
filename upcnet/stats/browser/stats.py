# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from DateTime import DateTime

from zope.app.component.hooks import getSite



def userLoginHandler (event):
    """
        Handler que captura els events IUserLoggedInEvent i actualitza la data
        de l'ultim login.
    """
    site = getSite()

    properties = getToolByName(site,'portal_properties').site_properties
    if properties.hasProperty('last_login') == 0 :
        properties.manage_addProperty('last_login',DateTime(),'date')
    else:
        properties.manage_changeProperties({'last_login':DateTime().ISO()})

class StatsView(BrowserView):
    """
        View Controller for rendering the stats
    """

    __call__ = ViewPageTemplateFile('stats.pt')


    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.properties = getToolByName(context,'portal_properties').site_properties
        if self.properties.hasProperty('last_login') == 0 :
            self.properties.manage_addProperty('last_login','','string')

    def getInactivitat(self):
        """
            Retunrs the days from the last login.
        """
        isodate = self.properties.last_login
        if isodate == '' :
            days = -1
        else:
            dt = DateTime(isodate)
            last_access = dt.timeTime()
            minutes = int((DateTime().timeTime() - last_access)/60.0)
            days = int(minutes/86400.0)
        return  days


    def getSize(self):
        """
            Returns the size of the plone instance
        """

        size = 0
        portal_catalog = getToolByName (self.context, 'portal_catalog')
        type_filter = ['Folder', 'Large Plone Folder']
        type_search = portal_catalog.searchResults()
        if type_search:
            for f in type_search:
                try:
                    o = f.getObject()
                    if hasattr(o, 'get_size'):
                        size += int(o.get_size())
                except:
                    size = 0
        return size

    def human_size(self, num):
        """
            Returns de size in human readable format
        """
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0
        return num
