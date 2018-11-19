from jwcrypto import jwk
import json
import xml.etree.ElementTree as ET


def generate_signing_secret():
    key = jwk.JWK.generate(kty = 'oct',size = 256)
    return json.loads(key.export()).get("k")


def convert_xml_to_dict(xml):
    root=ET.fromstring(xml.decode())
    it=root.iter()

    d={}
    for i in it:
        if len(i)==0:
            tag=i.tag.strip()
            if '}' in tag:
                tag=(tag.split('}')[1]).strip()
            text=i.text.strip()

            d.update({tag:text})

    return d