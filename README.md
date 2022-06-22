# XML Documents

XML External Entity attacks exploit vulnerabilities in applications which process eXtensible Markup Language (XML). XML is syntactically similar to Hypertext Markup Language (HTML), but with some differences. While HTML is used to format and display data on websites, XML is used to transport and store data between applications.

# XML External Entity (XXE) Attacks

XXE attacks leverage a feature of many XML parsers which allow the parser to retrieve data from resources outside of the document itself. Specifically, XML allows the definition of custom character sequences which in turn refer to other data. These are called Custom XML Entities. Custom XML Entities are defined within the document type definition (DTD), which is often defined at the start of an xml document. For example, consider initializing a document with the DTD:

```xml
<! DOCTYPE example [<! ENTITY entity_name "some text to insert"> ]>
```

Note the entity definition, formatted as`[<! ENTITY entity_name "some text to insert">]`. If we reference `&entity_name` elsewhere in the document, an XML parser will render the text `some text to insert`.
This entity definition may even lie outside of the DTD in which it is declared. These are called external entity definitions and are declared using the `SYSTEM` keyword and a corresponding Uniform Resource Identifier (URI), which may reference a webpage or a file.  An example DTD containing a enternal entity definition is provided below:

```xml
<! DOCTYPE example2 [<! ENTITY external_entity SYSTEM "http://www.example.com" > ]>
```

We can reference this data using the newly-defined keyword, `&external_entity`. However, the parser will now retrieve data from the external resource to populate the document (in this case, the contents of the `example.com` homepage). In this tutorial we will exploit this behavior to access data on the machine hosting a xml parser website. Many xml parsers are configured to perform these requests for external data by default. In a similar example, the URI can specify a file to read from the local machine, e.g.

```xml
<! DOCTYPE example2 [<! ENTITY external_entity_file SYSTEM "file:///etc/passwd" > ]>
```

Then by referencing `&external_entity_file` later, the xml parser will populate the xml document with the contents of `/etc/passwd`.

## A Complete Example

Suppose an attacker discovers a public website which reformats xml data submitted by the user. In order to test if the backend xml parser is configured to accept external entity definitions in th DTD, the attacker could submit an xml document like this:

```xml
<?xml version="1.0"?>
<!DOCTYPE replace [<!ENTITY external_entity_file SYSTEM "file:///etc/passwd"> ]>
 <aField>&external_entity_file;</aField>
```

Should the website return the contents of  the `/etc/passwd` file successfully, we may surmise that the xml parser is indeed vulnerable to XXE. If the attacker replaces the payload with `"file:///etc/passwd"` and it executes successfully, then the vulnerability is even more severe. In this case the xml parser application is probably running with root permissions, because `/etc/passwd` is usually only accessible to root users. Combining both these responses, the attacker would have enough information to begin cracking the hashed passwords stored in `/etc/passwd`.

Try applying this approach to retrieve the contents of `/etc/passwd` from the web page displayed.

# Patching The Vulnerability

```python
def process_xml(xml_string):
    customParser = etree.XMLParser()
    root = etree.fromstring(xml_string, parser = customParser)
    return etree.tostring(root, pretty_print=True, encoding = str)
```

The vulnerability is associated with the configuration of the xml parser, so the fix will be languae and library specific. Consider the example code above using the `lxml` library in python. The `lxml.etree.XMLParser()` class is configured to resolve external entities by default. This behaviour is inherited by the `lxml.etree.fromstring()` method used to process the raw xml. Can we change the behavior of the `XMLParser()` class?

## Hint

The xml parsers behavior may be changed by passing in keyword arguments when we instantiate the class. The possible options and their default values are enumerated in the [lxml docs page](https://lxml.de/api/lxml.etree.XMLParser-class.html). Can you see an option that could prevent dangerous handling of untrusted external entities?

## Another Hint

Try instantiating the `XMLParser` class while passing in the keyword argument `resolve_entities=False`. Now check if the app still renders data it shouldn't. Congratulations!

# Sources

A good high-level description of the issue:  
https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing  
Useful xxe code snippets taken from:  
https://github.com/payloadbox/xxe-injection-payload-list  
Another helpful toy project I found, using the `xml.sax` library and `flask`:  
https://github.com/feabell/xxe-demos  
Advice on handling various xml vulnerabilities on the `lxml` package:  
https://lxml.de/FAQ.html#how-do-i-use-lxml-safely-as-a-web-service-endpoint
