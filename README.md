# Simple-AnIML

## Description

Python package for working with AnIML data files.

## Scope

- Create, open & edit AnIML files
- Provide a simple interface to the AnIML schema and to assist users in avoiding common pitfalls
- The package does not check for logical inconsistencies in the files, e.g. missing references, duplicate IDs, etc. Instead this is left to the user and/or schema validation tools.

## Installation

Package is available on PyPI under the name `simple-animl` and can be installed using pip.

## Example

```python
from xml.dom import minidom
from xml.etree import ElementTree as ET
from simple_animl import AnIMLDoc, Sample, SampleSet

doc = AnIMLDoc()
doc.sample_set = SampleSet()
doc.sample_set.add(Sample(name='sample1', sampleID="1"))
doc.sample_set.add(Sample(name='sample2', sampleID="2"))
doc.sample_set.add(Sample(name='sample3', sampleID="3"))

et = doc.dump_xml()
xml_string = minidom.parseString(ET.tostring(et)).toprettyxml(indent="  ")

print(xml_string)
```

```xml
<?xml version="1.0" ?>
<AnIML xmlns="urn:org:astm:animl:schema:core:draft:0.90" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="0.90" xsi:schemaLocation="urn:org:astm:animl:schema:core:draft:0.90 http://schemas.animl.org/current/animl-core.xsd">
  <SampleSet>
    <Sample name="sample1" sampleID="1"/>
    <Sample name="sample2" sampleID="2"/>
    <Sample name="sample3" sampleID="3"/>
  </SampleSet>
</AnIML>
```

## Project Goals

The following MVP (minimum viable product) goals are defined for this project. They're not set in stone and may change as the project progresses but they should give a good idea of what to expect.

### MVP1

- Possible to create, open & edit AnIML xml files.
- The following AnIML document features are supported:
  - Samples
  - Experiment Steps
- Helper function to simplify outputing the xml to a file or string.

### MVP2

- TBC

### Long term goals

- Document signing support
- Document diff feature support

### Long term goals (maybe)

- Document validation
- Technique definitions helper functions
