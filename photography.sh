#!/bin/zsh
echo "Retrieve the metadata about the images" 
python photography_meta.py
PHOTO_DIR=`jq -r '.folders.directory' "$OLI_LOCAL_DIR/photography/conf.json"`
echo $PHOTO_DIR
if [[ ! -d "$PHOTO_DIR" ]]
then
    echo "$DIRECTORY with images does exists on the filesystem."
    exit 1
fi

echo "Saving js from Elm code in $PHOTO_DIR"
cd photography/webviewer
elm-test
elm make src/Main.elm --output="$PHOTO_DIR/main.js"
cp html/* "$PHOTO_DIR/"