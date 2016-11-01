-- Spanish localization.
local locale = GetLocale()
if locale == 'deDE' then
	local L = INL_Addon.strings;

L.Chat = {
	Loaded = "Geladene Spracheinstellung: |cffff0000%s|r.",
	ReloadUI = "Lade die Benutzeroberfläche neu, um die Spracheinstellung \"|cffff0000%s|r\" zu laden.",
	WowheadLink = "Wowhead-Links:", -- Needs review
}
L.Lang = {
	deDE = "Deutsch",
	enUS = "Englisch",
	esES = "Spanisch",
	frFR = "Französich",
	itIT = "Italienisch",
	koKR = "Koreanisch", -- Needs review
	ptBR = "Portugiesisch",
	ruRU = "Russisch",
	zhTW = "Chinesisch", -- Needs review
}
L.Options = {
	ReloadUIButton = "Benutzeroberfläche neu laden",
	ResetButton = "Standardkonfiguration zurücksetzen",
	selectedLocale = "Sprache (Erfordert ein Neuladen des UIs)",
	showTooltipLine = "Die lokalisierte Zeichenfolge auf eine Linie auf dem Tooltip anzeigen.",
	showTooltipTitle = "Die lokalisierte Zeichenfolge im Tooltip-Titel anzeigen.",
}
L.Tooltip = {
	MissingLocale = "Fehlende Spracheinstellung",
}


end
