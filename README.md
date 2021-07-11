# create-lilypond-files
Python codes that convert the csv output from Sonic Visualizer to lilypond-complible files
To compile .ly files, download Lilypond from https://lilypond.org/download.html and follow the instructions to create /usr/local/bin/lilypond.\\

To run on command:
$ cd \n
$ git clone https://github.com/jessicaycyeh/create-lilypond-files.git \n
$ cd create-lilypond-files\\
$ python src/create_ly.py > 'lyfiles/demo.ly' \n
$ lilypond lyfiles/demo.ly \n
$ open demo.pdf \n
