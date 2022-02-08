import unittest
import requests


class Corpora(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Corpora, self).__init__(*args, **kwargs)

    def setUp(self) -> None:
        return

    def test_001_corpora_downloader(self):
        url = "https://eur-lex.europa.eu/EURLexWebService"
        headers = {'content-type': 'application/soap+xml'}
        body = (
            "<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\" xmlns:sear=\"http://eur-lex.europa.eu/search\">\n"
            "    <soap:Header>\n"
            "        <wsse:Security soap:mustUnderstand=\"true\" xmlns:wsse=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd\">\n"
            "            <wsse:UsernameToken wsu:Id=\"UsernameToken-3\" xmlns:wsu=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd\">\n"
            "                <wsse:Username>n008j19f</wsse:Username>\n"
            "                <wsse:Password Type=\"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText\">CKZNYdSty5t</wsse:Password>\n"
            "            </wsse:UsernameToken>\n"
            "        </wsse:Security>\n"
            "    </soap:Header> \n"
            "    <soap:Body>\n"
            "    <sear:searchRequest>\n"
            "      <sear:expertQuery><![CDATA[DTS_SUBDOM = \"TREATIES\" OR \"INTER_AGREE\" OR \"LEGISLATION\" OR \"EFTA\" OR \"EU_LAW_ALL\" AND PD >= 01/01/2012 <= 07/02/2022]]></sear:expertQuery>\n"
            "      <sear:page>1</sear:page>\n"
            "      <sear:pageSize>10</sear:pageSize>\n"
            "      <sear:searchLanguage>en</sear:searchLanguage>\n"
            "    </sear:searchRequest>\n"
            "    </soap:Body>\n"
            "</soap:Envelope>")

        response = requests.post(url, data=body, headers=headers)

        return response
