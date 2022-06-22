from flask import Flask, render_template, request
from pprint import pprint
from lxml import etree

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    error = None
    inputXml = None
    outputXml = None
    success = None
    if request.method == "POST":
        # Extract the xml data from the form
        inputXml = request.form.get('inputXml', None)
        try:
            # process the xml string
            outputXml = process_xml(inputXml)

            # render the data
            error = None
            success = 'Your XML is rendered successfully:'
            return render_template('index.html', error=error, form_data = inputXml, output_data = outputXml, success=success)
        except etree.XMLSyntaxError:
            error="XML error. Please check your document syntax."
    return render_template('index.html', error=error, form_data = inputXml, output_data = outputXml, success=success)

def process_xml(xml_string: str) -> str:
    customParser = etree.XMLParser()
    root = etree.fromstring(xml_string, parser = customParser)
    return etree.tostring(root, pretty_print=True, encoding = str)

'''
# For completeness, I provide a patched process_xml method here:
def process_xml(xml_string):
    customParser = etree.XMLParser(resolve_entities=False)
    root = etree.fromstring(xml_string, parser = customParser)
    return etree.tostring(root, pretty_print=True, encoding = str)
'''