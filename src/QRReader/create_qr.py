#!/usr/bin/python
# -*- coding: utf-8 -*-
# requires pip install qrcode
import qrcode
import qr_constants as const

class create_qr:
    """This is the create qr Class

    This is used to generate a qr code
    for a given string.
    """
    __export_path = const.EXPORT_PATH
    
    def __generate(self, message):
        """This function is used to generate qr code.
        :param: (str) message to be embedded in qr code
        return: (boolean)  qr generated
        """
        try:
            qr_code = qrcode.make(message)
            qr_code.save(self.__export_path)
            return True
        except:
            return False    
    
    def start(self, message):
        """This function is used to initaiate the create_qr class.
        :param: (str) message to be embedded in qr code
        :return: (boolean)  qr generated
        """
        is_QR_Ready = self.__generate(message)
        if is_QR_Ready:
            return is_QR_Ready
        else:
            print("Error occurred in QR ")
            return is_QR_Ready

