# create-lilypond-files
Python codes that convert the csv output from Sonic Visualizer to lilypond-complible files. <br />
To compile .ly files, download Lilypond from https://lilypond.org/download.html and follow the instructions to create /usr/local/bin/lilypond. <br />

To run on command:
$ cd <br />
$ git clone https://github.com/jessicaycyeh/create-lilypond-files.git <br />
$ cd create-lilypond-files <br />
$ python src/create_ly.py > 'lyfiles/demo.ly' <br />
$ lilypond lyfiles/demo.ly <br />
$ open demo.pdf <br />
