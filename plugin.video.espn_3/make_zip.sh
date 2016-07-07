#!/bin/bash
DIR=plugin.video.espn_3
VERSION=`grep "version" < addon.xml | tail -n+2 | head -n1 | sed 's/ *version="//' | sed 's/"//' | tr -d '[[:space:]]'`
echo "Making zip of $VERSION"
cd ..
zip -r plugin.video.espn_3-$VERSION.zip $DIR -x $DIR/.git/\* -x $DIR/bugs/\* -x $DIR/\*.pyo -x $DIR/\*.pyc -x $DIR/.idea/\*
cp plugin.video.espn_3-$VERSION.zip repo.kodi-addons/plugin.video.espn_3/
cp plugin.video.espn_3/addon.xml repo.kodi-addons/plugin.video.espn_3/
cd repo.kodi-addons
python2 addons_xml_generator.py
