# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "ida"
__date__ = "$03/02/2015 12:17:02 PM$"

class Team:
    name = ''
    number = ''
    
    def __init__(self, name, number):
        self.name = name
        self.number = number 
        
    def __str__(self):
        return self.name + '\n' + self.number