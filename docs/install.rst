Getting started with Textract
=============================

This is what worked for me on OSX & Linux:

* Install the `AWS command line tools <https://aws.amazon.com/cli/>`_ and the `AWS SDK for Python (Boto3) <https://aws.amazon.com/sdk-for-python/>`_. As I already use `conda <https://conda.io/en/latest/>`_, I found it easiest to use that. Just `activate` your environment of choice and then add the AWS tools to it with:

  .. code:: bash

    conda install -c conda-forge awscli
    conda install -c conda-forge boto3
    
* `Create an AWS account <https://aws.amazon.com/>`_.
* Configure your AWS account: (Set a default region, because Textract will only work in one region. I used 'eu-west-1').
  
.. code:: bash

    aws configure
  
* `Sign up for the Textract preview <https://pages.awscloud.com/textract-preview.html>`_ and get accepted.
* Configure your AWS account to use Textract:

.. code:: bash

    aws s3 cp s3://amazon-textract-preview2/service-2.json
    aws configure add-model --service-model file://./service-2.json --service-name textract
    
That should be enough to get it working. Test it from the command line by running Textract on a file in S3 (I used `this one <https://s3-eu-west-1.amazonaws.com/textract.samples/Margate_1891_02.png>`_).

.. code:: bash

   aws textract analyze-document --document '{"S3Object":{"Bucket":"textract.samples","Name":"Margate_1891_02.png"}}' --feature-types '["TABLES","FORMS"]'
   
If it works, this will return a load of JSON output. If it produces an error message, something has gone wrong.

The pre-release version of Textract has deliberately limited capacity; it will allow only a small number of simultanious requests across all its users. The practical effect of this is that my calls to the service often failed, throwing a ``ProvisionedThroughputExceededException``. This is a nuisance, but you can just keep running it again until it works. I am assured that the production (paid) version of the service will not have this limitation.

I was most confused by the limitations imposed by the different AWS regions: For the pre-release version, if you run `aws textract` in the wrong region, it won't work. If you run textract in one region, but specify a S3 document in a different region, it won't work. While it took me a long time to work out what was going wrong with my calls to the service, this is a problem with my understanding of AWS rather than a limitation of Textract. Also, the production (paid) version of the service will be available (eventually) across all the regions.



    

    
