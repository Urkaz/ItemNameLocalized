#!/bin/bash
ADDON_MAIN_FOLDER="ItemNameLocalized"
ADDON_VERSION="v1.3"
GAME_VERSION="7.1.5"

FOLDERS=("AddonLocale" "ItemLocales")
FILES=("Core.lua" "Preload.lua" "ItemNameLocalized.toc" "CHANGELOG.md" "README.md" "LICENSE")

echo "--------------------------"
echo "> Deploying "$ADDON_MAIN_FOLDER
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
rm -f ./${ADDON_MAIN_FOLDER}_${ADDON_VERSION}_${GAME_VERSION}.zip
echo "> Creating zip"
zip -r ./${ADDON_MAIN_FOLDER}_${ADDON_VERSION}_${GAME_VERSION}.zip ./$ADDON_MAIN_FOLDER/*
echo "> zip created"
echo "--------------------------"
rm -rf ./$ADDON_MAIN_FOLDER
read -p "> Deploy finished. Press [Enter]..."