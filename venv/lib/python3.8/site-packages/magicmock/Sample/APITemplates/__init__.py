'''
Created on Jun 21, 2013

@author: mxu
'''
version = "1.2"

class StatusCode:
    code_200 = "200 OK"
    code_400 = "400 Bad Request"
    code_401 = "401 Unauthorized"   
    code_403 = "403 Forbidden"
    code_404 = "404 Not Found"
    code_502 = "502 Bad Gateway"
    code_503 = "503 Service Unavailable"
    code_504 = "504 Gateway Timeout"
    code_505 = "505 Internal Server Error"
    code_600 = "600 Invalid app id"    
    code_601 = "601 Invalid uvs access token"
    code_602 = "602 Invalid confirmation code"
    code_603 = "603 The email or password you have provided does not match our records"    
    code_604 = "604 This email already exists"    
    code_605 = "605 Badge does not exist"    
    code_606 = "606 Organization does not exist"    
    code_607 = "607 Password does not meet minimum requirements"    
    code_608 = "608 Invalid facebook access token"    
    code_609 = "609 Invalid email id"    
    code_610 = "610 Connector timeout"    
    code_611 = "611 Connector Access token invalid, ORG:$orgid"    
    code_612 = "612 Invalid data returned by connector"    
    code_613 = "613 The new password is as same as the old one"    
    code_614 = "614 Invalid limit or offset"    
    code_615 = "615 Update badge from connector failed"    
    code_620 = "620 You are not the owner of this asset"    
    code_621 = "621 You are not the administrator of this organization"    
    code_622 = "622 Primary email cannot be deleted"    
    code_623 = "623 Device Name already exists"    
    code_624 = "624 Invalid Tag Params"    
    code_625 = "625 Too many login failures! Please try again in a few minutes."    
    code_626 = "626 Key Not found"    
    code_627 = "627 This device is already activated"    
    code_628 = "628 Device does not exist"    
    code_630 = "630 Badge Permanently Deleted"    
    code_631 = "631 Badge tied to another account"    
    code_640 = "640 The email is not confirmed"    
    code_641 = "641 Usher general configuration error"    
    code_642 = "642 You have no permission to do this operation"    
    code_643 = "643 Failed to disable this code, please try again"    
    code_701 = "701 File permission Denied"    
    code_702 = "702 Document can not be deleted"    
    code_704 = "704 Failed to create a document"    
    code_705 = "705 Wrong device type"    
    code_706 = "706 The type and the token you post does NOT match"    
    code_707 = "707 There is an error from Google Cloud Messaging System"    
    code_708 = "708 You are not the owner of this doc"    
    code_709 = "709 update doc failed"    
    code_710 = "710 doc does not exist"    
    code_711 = "711 You can not share key to yourself"    
    code_712 = "712 Failed to update the sharing, please try it again."    
    code_713 = "713 You can not share doc to yourself"    
    code_801 = "801 DFS upload failed"    
    code_802 = "802 DFS download failed"    
    code_803 = "803 DFS delete failed"    
    code_806 = "806 File does NOT exist"    
    code_807 = "807 recevie files(image) or store files failed"
    code_no_response = "0"
    no_response = "0"
    
class Header:
    @staticmethod
    def getExcpMsg(content):
        default_header = Header.get()
        default_header['X-FW-EXCEPTION'] = content
        return default_header

    @staticmethod
    def get():
        return {'Content-Type': 'application/json'}
    
    @staticmethod
    def jpgimage():
        return {'Content-Type':'image/jpeg'}
