import requests
from bs4 import BeautifulSoup as bs

from django.shortcuts import render_to_response
from rest_framework.views import APIView
from rest_framework.response import Response


def index(request):
    return render_to_response('index.html')


class contentHandler(APIView):

    def post(self, request, format=None, module=None):
        itemDetail = self.getDetail(request.data)

        return Response(itemDetail)

    
    def getDetail(self, url):

        req = requests.get(url['link'])
        raw = bs(req.content, 'lxml')

        itemDetail = {}
        itemDetail['title']     = self.getTitle(raw)
        itemDetail['price']     = self.getPrice(raw)
        itemDetail['option']    = self.getOptions(raw)  

        return itemDetail


    def getTitle(self, raw):
        title = raw.find(class_='cdtl_info_tit')
        return(title.string)


    def getPrice(self, raw):
        rawPrice = raw.find(class_='cdtl_new_price')
        if rawPrice:
            price = rawPrice.find(class_='ssg_price')
            return(price.string)

        else:
            price = raw.find(class_='ssg_price')
            return(price.string)


    def getOptions(self, raw):
        print('>> getting option(s)')
        rawOpt = raw.find_all(class_='cdtl_opt_group')
        if rawOpt:
            options = {}
            for opt in rawOpt:
                optList = opt.find('dd')
                optList = optList.find_all('option')
                value = []
                for i in optList:
                    if i['value'] is not '':
                        value.append(i['value'])

                options[opt.find('dt').string] = value
            
            return options
        
        else:
            return ""





'''
tried URL : 
http://www.ssg.com/item/itemView.ssg?locale=en-US&itemId=1000027096586&siteNo=6009&salestrNo=1018
http://www.ssg.com/item/itemView.ssg?locale=en-US&itemId=1000036993469&siteNo=6009&salestrNo=1002&click=itemMidArea02
http://www.ssg.com/item/itemView.ssg?locale=en-US&itemId=1000022966659&siteNo=6001&salestrNo=2034
'''