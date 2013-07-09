#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from LiveAuction.models import *

admin.site.register(Auction)
admin.site.register(Bid)
