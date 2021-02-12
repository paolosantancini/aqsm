"""
HTTP/HTTPS CALLER OBJECT CLASS
Created on Thu Feb 11 18:51:23 2021

@author: Paolo Santancini
"""

import requests

class Caller:
    
    def __init__(self, content):
        self.content = content
        
    def Call(self, url):
        return (url)