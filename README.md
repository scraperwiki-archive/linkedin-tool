For development:

    sudo apt-get install libyaml-dev
    pip install -r devreq.txt
    virtualenv .

For running (as a tool, etc):

    pip install -r requirements.txt

Remember to `. activate`

To run tests:

    . activate
    specloud test/*.py
