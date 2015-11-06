#!/usr/bin/python

from datetime import tzinfo, timedelta

class UTC(tzinfo): 
    def utcoffset(self,dt): 
        return timedelta(hours=0) 
    def tzname(self,dt): 
        return "UTC" 
    def dst(self,dt): 
        return timedelta(0) 


class BRST(tzinfo): 
    def utcoffset(self,dt): 
        return timedelta(hours=-3) 
    def tzname(self,dt): 
        return "BRT" 
    def dst(self,dt): 
        return timedelta(0) 

brst = BRST() 
utc = UTC()
