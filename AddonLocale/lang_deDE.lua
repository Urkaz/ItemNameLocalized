-- German localization.
local locale = GetLocale()
if locale == 'deDE' then
	local L = INL_Addon.strings;

L["Chat"] = {
	["Loaded"] = "Geladene Spracheinstellung: |cffff0000%s|r.",
	["ReloadUI"] = "Lade die Benutzeroberfläche neu, um die Spracheinstellung \"|cffff0000%s|r\" zu laden.",
	["WowheadLink"] = "Wowhead-Link:"
}
L["Lang"] = {
	["deDE"] = "Deutsch",
	["enUS"] = "Englisch",
	["esES"] = "Spanisch (Spanien)",
	["esMX"] = "Spanisch (Mexiko)",
	["frFR"] = "Französich",
	["itIT"] = "Italienisch",
	["koKR"] = "Koreanisch",
	["ptBR"] = "Portugiesisch",
	["ruRU"] = "Russisch",
	["zhTW"] = "Chinesisch"
}
L["Options"] = {
	["ReloadUIButton"] = "Benutzeroberfläche neu laden",
	["ResetButton"] = "Standardkonfiguration zurücksetzen",
	["selectedLocale"] = "Sprache (Erfordert ein Neuladen des UIs)",
	["showTooltipLine"] = "Die lokalisierte Zeichenfolge auf einer Zeile im Tooltip anzeigen.",
	["showTooltipTitle"] = "Die lokalisierte Zeichenfolge im Tooltip-Titel anzeigen."
}
L["Tooltip"] = {
	["MissingLocale"] = "Fehlende Spracheinstellung"
}

end
