Testing Google Vision for weather data rescue
=============================================

As `AWS Textract looks promising as a tool for data rescue <http://brohan.org/AWS-Textract/>`_, it's worth trying `Google Vision <https://cloud.google.com/vision/>`_ in the same way.


.. toctree::
   :maxdepth: 1

..
   Getting started with Textract <install>
   

I tested Google Vision on sample images from several different documents containing weather observations we need to transcribe. All were somewhat successful, though the level of success varied:
   
.. toctree::
   :maxdepth: 1

   samples/Ben_Nevis/text
   samples/Second_order/text
   samples/Argentine_DWR/text
   samples/Observatories/text
   samples/DWR_1901/text
   samples/DWR_1862/text
   samples/IDWR/text
   samples/US_map/text
   samples/Farragut/text
   samples/Jeannette/text
   

As the systemproduced reasonable results on the :doc:`Ben Nevis project sample <samples/Ben_Nevis/text>`, it was possible to run Google Vision against the `OCR-weatherrescue transcription benchmark <http://brohan.org/OCR-weatherrescue/index.html>`_:


.. toctree::
   :titlesonly:
   :maxdepth: 1

   OCR-weatherrescue/months

Results are qualitatively similar to those from  `AWS Textract <http://brohan.org/AWS-Textract/>`_.

.. toctree::
   :titlesonly:
   :maxdepth: 1

   Small Print <credits>

This document is crown copyright (2019). It is published under the terms of the `Open Government Licence <https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/>`_.
