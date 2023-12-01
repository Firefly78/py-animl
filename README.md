# Simple-AnIML

## Description

Python package for working with AnIML data files.

## Scope

- Create, open & edit AnIML files
- Provide a simple interface to the AnIML schema and to assist users in avoiding common pitfalls
- The package does not check for logical inconsistencies in the files, e.g. missing references, duplicate IDs, etc. Instead this is left to the user and/or schema validation tools.

## Example

```python
from xml.dom import minidom
from xml.etree import ElementTree as ET
from simple_animl import AnIMLDoc, Sample, SampleSet

doc = AnIMLDoc()
doc.add(Sample(name='sample1', sampleID="1"))
doc.add(Sample(name='sample2', sampleID="2"))
doc.add(Sample(name='sample3', sampleID="3"))
```
