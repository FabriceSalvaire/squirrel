####################################################################################################
# 
# Babel - A Bibliography Manager 
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

####################################################################################################

def XByte(x, power):
    return x * 1024**power

def to_XByte(x, power):
    return float(x)/1024**power

def KByte(x):
    return XByte(x, 1)

def to_KByte(x):
    return to_XByte(x, 1)

def MByte(x):
    return XByte(x, 2)

def to_MByte(x):
    return to_XByte(x, 2)

def GByte(x):
    return XByte(x, 3)

def to_GByte(x):
    return to_XByte(x, 3)

def TByte(x):
    return XByte(x, 4)

def to_TByte(x):
    return to_XByte(x, 4)

####################################################################################################
#
# End
#
####################################################################################################
