-- German localization.
local locale = GetLocale()
if locale == 'ruRU' then
	local L = INL_Addon.strings;

L["Chat"] = {
	["Loaded"] = "Загружен |cffff0000%s|r язык.",
	["ReloadUI"] = "Перезагрузить пользовательский интерфейс для загрузки |cffff0000%s|r языка.",
	["WowheadLink"] = "Wowhead ссылка:",
}
L["Lang"] = {
	["deDE"] = "Немецкий ",
	["enUS"] = "Английский",
	["esES"] = "Испанский (Испания)",
	["esMX"] = "Испанский (Мексика)",
	["frFR"] = "Французский",
	["itIT"] = "Итальянский",
	["koKR"] = "Корейский",
	["ptBR"] = "Португальский",
	["ruRU"] = "Русский",
	["zhTW"] = "Китайский",
}
L["Options"] = {
	["ReloadUIButton"] = "Перезагрузить UI",
	["ResetButton"] = "Сброс по умолчанию",
	["selectedLocale"] = "Язык (требуется перезагрузка UI)",
	["showTooltipLine"] = "Показать локализованную строку на строки в подсказке.",
	["showTooltipTitle"] = "Показать локализованную строку в названии подсказка.",
}
L["Tooltip"] = {
	["MissingLocale"] = "Отсутствует язык",
}

end
