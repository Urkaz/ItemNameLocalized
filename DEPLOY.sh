#!/bin/bash

ADDON_VERSION="v2.2"
GAME_VERSION="9.0.2"

FOLDERS=("ItemNameLocalized_Core" "ItemNameLocalized_esES" "ItemNameLocalized_deDE" "ItemNameLocalized_esMX" "ItemNameLocalized_frFR" "ItemNameLocalized_itIT" "ItemNameLocalized_ptBR" "ItemNameLocalized_ruRU" "ItemNameLocalized_koKR" "ItemNameLocalized_zhCN" "ItemNameLocalized_zhTW")


echo "--------------------------"
echo "> Deploying final packages"
echo "--------------------------"

rm -f "ItemNameLocalized_Core/ItemLocales/en_US_1.lua"
rm -f "ItemNameLocalized_Core/ItemLocales/en_US_2.lua"
cp "parser/ItemLocales/en_US_1.lua" "ItemNameLocalized_Core/ItemLocales/en_US_1.lua"
cp "parser/ItemLocales/en_US_2.lua" "ItemNameLocalized_Core/ItemLocales/en_US_2.lua"
rm -f "ItemNameLocalized_Core/SpellLocales/en_US_1.lua"
cp "parser/SpellLocales/en_US_1.lua" "ItemNameLocalized_Core/SpellLocales/en_US_1.lua"

rm -f "ItemNameLocalized_esES/ItemLocales/es_ES_1.lua"
rm -f "ItemNameLocalized_esES/ItemLocales/es_ES_2.lua"
cp "parser/ItemLocales/es_ES_1.lua" "ItemNameLocalized_esES/ItemLocales/es_ES_1.lua"
cp "parser/ItemLocales/es_ES_2.lua" "ItemNameLocalized_esES/ItemLocales/es_ES_2.lua"
rm -f "ItemNameLocalized_esES/SpellLocales/es_ES_1.lua"
cp "parser/SpellLocales/es_ES_1.lua" "ItemNameLocalized_esES/SpellLocales/es_ES_1.lua"

rm -f "ItemNameLocalized_itIT/ItemLocales/it_IT_1.lua"
rm -f "ItemNameLocalized_itIT/ItemLocales/it_IT_2.lua"
cp "parser/ItemLocales/it_IT_1.lua" "ItemNameLocalized_itIT/ItemLocales/it_IT_1.lua"
cp "parser/ItemLocales/it_IT_2.lua" "ItemNameLocalized_itIT/ItemLocales/it_IT_2.lua"
rm -f "ItemNameLocalized_itIT/SpellLocales/it_IT_1.lua"
cp "parser/SpellLocales/it_IT_1.lua" "ItemNameLocalized_itIT/SpellLocales/it_IT_1.lua"

rm -f "ItemNameLocalized_frFR/ItemLocales/fr_FR_1.lua"
rm -f "ItemNameLocalized_frFR/ItemLocales/fr_FR_2.lua"
cp "parser/ItemLocales/fr_FR_1.lua" "ItemNameLocalized_frFR/ItemLocales/fr_FR_1.lua"
cp "parser/ItemLocales/fr_FR_2.lua" "ItemNameLocalized_frFR/ItemLocales/fr_FR_2.lua"
rm -f "ItemNameLocalized_frFR/SpellLocales/fr_FR_1.lua"
cp "parser/SpellLocales/fr_FR_1.lua" "ItemNameLocalized_frFR/SpellLocales/fr_FR_1.lua"

rm -f "ItemNameLocalized_deDE/ItemLocales/de_DE_1.lua"
rm -f "ItemNameLocalized_deDE/ItemLocales/de_DE_2.lua"
cp "parser/ItemLocales/de_DE_1.lua" "ItemNameLocalized_deDE/ItemLocales/de_DE_1.lua"
cp "parser/ItemLocales/de_DE_2.lua" "ItemNameLocalized_deDE/ItemLocales/de_DE_2.lua"
rm -f "ItemNameLocalized_deDE/SpellLocales/de_DE_1.lua"
cp "parser/SpellLocales/de_DE_1.lua" "ItemNameLocalized_deDE/SpellLocales/de_DE_1.lua"

rm -f "ItemNameLocalized_ptBR/ItemLocales/pt_BR_1.lua"
rm -f "ItemNameLocalized_ptBR/ItemLocales/pt_BR_2.lua"
cp "parser/ItemLocales/pt_BR_1.lua" "ItemNameLocalized_ptBR/ItemLocales/pt_BR_1.lua"
cp "parser/ItemLocales/pt_BR_2.lua" "ItemNameLocalized_ptBR/ItemLocales/pt_BR_2.lua"
rm -f "ItemNameLocalized_ptBR/SpellLocales/pt_BR_1.lua"
cp "parser/SpellLocales/pt_BR_1.lua" "ItemNameLocalized_ptBR/SpellLocales/pt_BR_1.lua"

rm -f "ItemNameLocalized_esMX/ItemLocales/es_MX_1.lua"
rm -f "ItemNameLocalized_esMX/ItemLocales/es_MX_2.lua"
cp "parser/ItemLocales/es_MX_1.lua" "ItemNameLocalized_esMX/ItemLocales/es_MX_1.lua"
cp "parser/ItemLocales/es_MX_2.lua" "ItemNameLocalized_esMX/ItemLocales/es_MX_2.lua"
rm -f "ItemNameLocalized_esMX/SpellLocales/es_MX_1.lua"
cp "parser/SpellLocales/es_MX_1.lua" "ItemNameLocalized_esMX/SpellLocales/es_MX_1.lua"

rm -f "ItemNameLocalized_ruRU/ItemLocales/ru_RU_1.lua"
rm -f "ItemNameLocalized_ruRU/ItemLocales/ru_RU_2.lua"
cp "parser/ItemLocales/ru_RU_1.lua" "ItemNameLocalized_ruRU/ItemLocales/ru_RU_1.lua"
cp "parser/ItemLocales/ru_RU_2.lua" "ItemNameLocalized_ruRU/ItemLocales/ru_RU_2.lua"
rm -f "ItemNameLocalized_ruRU/SpellLocales/ru_RU_1.lua"
cp "parser/SpellLocales/ru_RU_1.lua" "ItemNameLocalized_ruRU/SpellLocales/ru_RU_1.lua"

rm -f "ItemNameLocalized_koKR/ItemLocales/ko_KR_1.lua"
rm -f "ItemNameLocalized_koKR/ItemLocales/ko_KR_2.lua"
cp "parser/ItemLocales/ko_KR_1.lua" "ItemNameLocalized_koKR/ItemLocales/ko_KR_1.lua"
cp "parser/ItemLocales/ko_KR_2.lua" "ItemNameLocalized_koKR/ItemLocales/ko_KR_2.lua"
rm -f "ItemNameLocalized_koKR/SpellLocales/ko_KR_1.lua"
cp "parser/SpellLocales/ko_KR_1.lua" "ItemNameLocalized_koKR/SpellLocales/ko_KR_1.lua"

rm -f "ItemNameLocalized_zhCN/ItemLocales/zh_CN_1.lua"
rm -f "ItemNameLocalized_zhCN/ItemLocales/zh_CN_2.lua"
cp "parser/ItemLocales/zh_CN_1.lua" "ItemNameLocalized_zhCN/ItemLocales/zh_CN_1.lua"
cp "parser/ItemLocales/zh_CN_2.lua" "ItemNameLocalized_zhCN/ItemLocales/zh_CN_2.lua"
rm -f "ItemNameLocalized_zhCN/SpellLocales/zh_CN_1.lua"
cp "parser/SpellLocales/zh_CN_1.lua" "ItemNameLocalized_zhCN/SpellLocales/zh_CN_1.lua"

rm -f "ItemNameLocalized_zhTW/ItemLocales/zh_TW_1.lua"
rm -f "ItemNameLocalized_zhTW/ItemLocales/zh_TW_2.lua"
cp "parser/ItemLocales/zh_TW_1.lua" "ItemNameLocalized_zhTW/ItemLocales/zh_TW_1.lua"
cp "parser/ItemLocales/zh_TW_2.lua" "ItemNameLocalized_zhTW/ItemLocales/zh_TW_2.lua"
rm -f "ItemNameLocalized_zhTW/SpellLocales/zh_TW_1.lua"
cp "parser/SpellLocales/zh_TW_1.lua" "ItemNameLocalized_zhTW/SpellLocales/zh_TW_1.lua"

for folder in "${FOLDERS[@]}"
do
	FINAL_FILE="${folder}_${ADDON_VERSION}_wow${GAME_VERSION}.zip"
	7z a -tzip "./packages/${FINAL_FILE}" ./$folder/*
done
echo "--------------------------"
read -p "> Deployment finished. Press [Enter]..."