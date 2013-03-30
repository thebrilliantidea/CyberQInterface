.. CyberQInterface documentation master file, created by
   sphinx-quickstart on Tue Mar 12 18:14:42 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

The CyberQInterface is a python library for communicating with the BBQ Guru
CyberQ Wi-fi temperature control system. This system provides accurate
monitoring of both Pit and Food temperature and tight control of the Pit
temperature.

Table of Contents
=================

.. toctree::
    :maxdepth: 2
    
    API
    Exceptions
    XMLs
    

Background
==========

I wrote the CyberQInterface because I love to barbeque. I grew up near Memphis,
Tn which is the home of some darn fine BBQ. The preferred style of BBQ made
in my homeland is pulled pork sandwiches with coleslaw and a thin, pepper hot
sauce. Pulled Pork is generally made with hickory smoke.

I have been in Texas (another area with a strong BBQ heritage) since 1999 and
given that beef smoked with mesquite is the local style I learned a lot about
the 'smoking' process.

I have gone through many grills and smokers over the years. In 2010 I
purchased one of the most popular cooking systems on the market. I invested in a
Large Big Green Egg. http://www.biggreenegg.com This is not the place to expound
on the qualities of the grill/smoker, but I must admit that having the 'Egg' has
made me a better cook and I could not be happier.

One of the best things about the Egg is the consistency of temperature once the
Egg is in the correct configuation for a particular temperature. That coupled
with the large fuel capacity means that you can cook items for 18 or more hours
without touching the smoker. 

However, given the amount of time it takes to smoke a brisket, the food
temperature does require a bit of monitoring. The mechanical temperature guage
on my BGE failed and the actual pit temperature was approximately 50 degrees
warmer than indicated. Needless to say, by the time I had figured out the
problem my wife had grown tired of making 'expensive' beef jerky.

She encouraged me to purchase the CyberQ Wifi from BBQ Guru.
http://store.thebbqguru.com/weborderentry/CyberQ%20WiFi The CyberQ includes
a web service interface which not only allows reading data from the temperature
control, but the ability to change settings via the web service. Ultimately, I
wrote this library to make that communication process easier and to be able to
trigger events programmatically.

Installation
============

You can install the library via easy_install. The command should look like::

    sudo pip install CyberQInterface
    
Source is also available on github. http://github.com/TheBrilliantIdea/CyberQInterface

To install from source, clone the code from github and then execute the setup.py
installer::

    sudo python setup.py install

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

