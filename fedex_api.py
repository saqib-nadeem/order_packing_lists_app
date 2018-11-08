import datetime
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

import requests

import util


class FedexAPI:

    def rate_request(self, address, weight):
        values = {
            'TIMESTAMP' :       datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'SERVICE_TYPE' :    ServiceTypes.BUSINESS if weight > 70 else ServiceTypes.RESIDENTIAL,
            'WEIGHT' :          weight,
            'ADDRESS_1' :       escape(address.address_line_1),
            'ADDRESS_2' :       escape(address.address_line_2),
            'CITY' :            escape(address.city),
            'STATE' :           address.state,
            'ZIP' :             address.zip,
            'COUNTRY_CODE' :    address.country_code,
        }

        request = requests.post(
            'https://ws.fedex.com:443/web-services/rate',
            RATE_REQUEST_TEMPLATE.format(**values)
        )
        request.raise_for_status()
        body = ET.fromstring(request.text)[1][0]

        messages = [x.text or '[Unknown error].' for x in body.iter('{http://fedex.com/ws/rate/v22}Message')]
        for severity in body.iter('{http://fedex.com/ws/rate/v22}HighestSeverity'):
            if severity.text not in ('SUCCESS', 'NOTE') :
                raise Exception(' '.join(messages))

        result = RateRequestResult()
        for price_element in body.iter('{http://fedex.com/ws/rate/v22}TotalNetChargeWithDutiesAndTaxes'):
            amount = float(price_element[1].text)
            if amount > result.amount:
                result.amount = amount

        for transit_time_element in body.iter('{http://fedex.com/ws/rate/v22}TransitTime'):
            result.transit_time = transit_time_element.text

        result.messages = messages

        return result


class RateRequestResult():

        def __init__(self, amount=0, transit_time='', messages=None):
            self.amount = amount
            self.transit_time = transit_time
            self.messages = messages or []


class ServiceTypes:

    BUSINESS =      'FEDEX_GROUND'
    RESIDENTIAL =   'GROUND_HOME_DELIVERY'



RATE_REQUEST_TEMPLATE = '''
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://fedex.com/ws/rate/v22">
   <SOAP-ENV:Body>
      <RateRequest>
         <WebAuthenticationDetail>
            <UserCredential>
               <Key>6tUDoLrXFmdGl9dp</Key>
               <Password>QPgGHrYQMEoFsQkWxaYNm37Ro</Password>
            </UserCredential>
         </WebAuthenticationDetail>
         <ClientDetail>
            <AccountNumber>349649926</AccountNumber>
            <MeterNumber>111869129</MeterNumber>
         </ClientDetail>
         <TransactionDetail>
            <CustomerTransactionId>TC023_US_PRIORITY_OVERNIGHT with Your Packaging</CustomerTransactionId>
         </TransactionDetail>
         <Version>
            <ServiceId>crs</ServiceId>
            <Major>22</Major>
            <Intermediate>0</Intermediate>
            <Minor>0</Minor>
         </Version>
         <ReturnTransitAndCommit>true</ReturnTransitAndCommit>
         <RequestedShipment>
            <ShipTimestamp>{TIMESTAMP}</ShipTimestamp>
            <DropoffType>REGULAR_PICKUP</DropoffType>
            <ServiceType>{SERVICE_TYPE}</ServiceType>
            <PackagingType>YOUR_PACKAGING</PackagingType>
            <TotalWeight>
               <Units>LB</Units>
               <Value>{WEIGHT}</Value>
            </TotalWeight>
            <Shipper>
               <Contact>
                  <CompanyName></CompanyName>
                  <PhoneNumber></PhoneNumber>
               </Contact>
               <Address>
                  <StreetLines>1201 Houston St</StreetLines>
                  <StreetLines></StreetLines>
                  <City>Fort Worth</City>
                  <StateOrProvinceCode>TX</StateOrProvinceCode>
                  <PostalCode>76102</PostalCode>
                  <CountryCode>US</CountryCode>
               </Address>
            </Shipper>
            <Recipient>
               <Contact>
                  <PersonName></PersonName>
                  <PhoneNumber></PhoneNumber>
               </Contact>
               <Address>
                  <StreetLines>{ADDRESS_1}</StreetLines>
                  <StreetLines>{ADDRESS_2}</StreetLines>
                  <City>{CITY}</City>
                  <StateOrProvinceCode>{STATE}</StateOrProvinceCode>
                  <PostalCode>{ZIP}</PostalCode>
                  <CountryCode>{COUNTRY_CODE}</CountryCode>
                  <Residential>1</Residential>
               </Address>
            </Recipient>
            <ShippingChargesPayment>
               <PaymentType>SENDER</PaymentType>
               <Payor>
                  <ResponsibleParty>
                     <AccountNumber>349649926</AccountNumber>
                  </ResponsibleParty>
               </Payor>
            </ShippingChargesPayment>
            <RateRequestTypes>LIST</RateRequestTypes>
            <PackageCount>1</PackageCount>
            <RequestedPackageLineItems>
               <SequenceNumber>1</SequenceNumber>
               <GroupNumber>1</GroupNumber>
               <GroupPackageCount>1</GroupPackageCount>
               <Weight>
                  <Units>LB</Units>
                  <Value>{WEIGHT}</Value>
               </Weight>
               <Dimensions>
                  <Length>12</Length>
                  <Width>12</Width>
                  <Height>12</Height>
                  <Units>IN</Units>
               </Dimensions>
               <ContentRecords>
                  <PartNumber>123</PartNumber>
                  <ItemNumber>123</ItemNumber>
                  <ReceivedQuantity>1</ReceivedQuantity>
                  <Description>ContentDescription</Description>
               </ContentRecords>
            </RequestedPackageLineItems>
         </RequestedShipment>
      </RateRequest>
   </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
'''


if __name__ == '__main__':
    address_123 = util.Address()
    address_123.address_line_1 = '3300 X A MEYER RD'
    address_123.city = 'GRANBURY'
    address_123.state = 'TX'
    address_123.zip = '76049'
    address_123.country_code = 'US'

    address_4 = util.Address()
    address_4.address_line_1 = '126 BARBER CT'
    address_4.city = 'BIRMINGHAM'
    address_4.state = 'AL'
    address_4.zip = '35209'
    address_4.country_code = 'US'

    address_5 = util.Address()
    address_5.address_line_1 = '1841 SILVER PALM RD'
    address_5.city = 'NORTH PORT'
    address_5.state = 'FL'
    address_5.zip = '34288'
    address_5.country_code = 'US'

    address_6 = util.Address()
    address_6.address_line_1 = '14623 SAM RD'
    address_6.city = 'LAKEWOOD'
    address_6.state = 'WI'
    address_6.zip = '54138'
    address_6.country_code = 'US'

    address_7 = util.Address()
    address_7.address_line_1 = '5809 WHITEMAN RD SW'
    address_7.city = 'LONGBRANCH'
    address_7.state = 'WA'
    address_7.zip = '98351'
    address_7.country_code = 'US'

    for weight in range(1,65):
        for address in (address_123, address_4, address_5, address_6, address_7):
            result = FedexAPI().rate_request(address, weight)
            text = address.zip + '\t' + str(weight) + '\t' + str(result.amount)
            print(text)
            with open('a.txt', 'a') as f:
                f.write(text + '\n')