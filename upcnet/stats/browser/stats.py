# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from DateTime import DateTime

from zope.component.hooks import getSite

from plone.app.controlpanel.mail import IMailSchema


def userLoginHandler(event):
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
            # Restem la diferecia de les dates en segons i obtenim els minuts /60
            minutes = int((DateTime().timeTime() - last_access)/60.0)
            # Els dies son els minuts per hora i les hores per dia
            days = int(minutes/60/24)

        return  days

    def getTitol(self):
        """
        Retorna el titol del lloc
        """
        titol = self.context.Title()
        return titol

    def getSize(self):
        """
            Returns the size of the plone instance in bytes
        """
        size = 0
        portal_catalog = getToolByName (self.context, 'portal_catalog')
        type_search = portal_catalog.searchResults(Language='all')
        if type_search:
            size = sum([a.get_size for a in type_search])
        return size

