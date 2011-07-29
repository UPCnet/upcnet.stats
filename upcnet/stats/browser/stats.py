# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from DateTime import DateTime

from zope.app.component.hooks import getSite

from plone.app.controlpanel.mail import IMailSchema

def userLoginHandler (event):
    """
        Handler que captura els events IUserLoggedInEvent i actualitza la data
        de l'ultim login.
    """
    site = getSite()
    properties = getToolByName(site,'portal_properties').site_properties
    if properties.hasProperty('last_login') == 0 :
        properties.manage_addProperty('last_login',str(DateTime().ISO()),'string')
    else:
        properties.manage_changeProperties(last_login=str(DateTime().ISO()))

class StatsView(BrowserView):
    """
        View Controller for rendering the stats
    """

    __call__ = ViewPageTemplateFile('stats.pt')


    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.properties = getToolByName(context,'portal_properties').site_properties
               
    def getContactEmail(self):
        """
            Returns the contact email
        """
        portal = getToolByName(self,'portal_url').getPortalObject()
        mail = IMailSchema(portal)         
        return mail.email_from_address
        
    def getInactivitat(self):
        """
            Returns the days from the last login.
        """
        days = -1
        if self.properties.hasProperty('last_login') == 1 :
            isodate = self.properties.last_login
            dt = DateTime(isodate)
            last_access = dt.timeTime()
            minutes = int((DateTime().timeTime() - last_access)/60.0)
            days = int(minutes/86400.0)

        return  days

    def getTitol(self):
        """
        Retorna el titol del lloc
        """
        titol = self.context.Title()
        return titol

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
        # No s'utilitza en cap lloc, pero pot ser interesant
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0
        return num
