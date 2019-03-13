#!/bin/bash
ADDON_MAIN_FOLDER="ItemNameLocalized"
ADDON_VERSION="v1.7"
GAME_VERSION="8.1.5"

FOLDERS=("AddonLocale" "ItemLocales")
FILES=("Core.lua" "Preload.lua" "ItemNameLocalized.toc" "CHANGELOG.md" "README.md" "LICENSE")
FINAL_FILE="${ADDON_MAIN_FOLDER}_${ADDON_VERSION}_wow${GAME_VERSION}.zip"

echo "--------------------------"
echo "> Deploying "$FINAL_FILE
echo "--------------------------"

mkdir -p ./$ADDON_MAIN_FOLDER
for i in "${FOLDERS[@]}"
do
	echo "> Copy folder: "$i
	cp -r ./$i ./$ADDON_MAIN_FOLDER
done
echo "--------------------------"
for i in "${FILES[@]}"
do
	echo "> Copy file: "$i
	cp -r ./$i ./$ADDON_MAIN_FOLDER
done

echo "--------------------------"
echo "> Deleting old zip"
rm -f ./$FINAL_FILE
echo "> Creating zip"
zip -r ./$FINAL_FILE ./$ADDON_MAIN_FOLDER/*
echo "> zip created"
echo "--------------------------"
echo "> Cleaning"
rm -rf ./$ADDON_MAIN_FOLDER
echo "--------------------------"
read -p "> Deploy finished. Press [Enter]..."