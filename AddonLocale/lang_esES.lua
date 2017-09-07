-- Spanish localization.
local locale = GetLocale()
if locale == 'esES' or locale == 'esMX' then
	local L = INL_Addon.strings;

L["Chat"] = {
	["Loaded"] = "Cargado idioma |cffff0000%s|r.",
	["ReloadUI"] = "Recarga la interfaz para cargar el idioma |cffff0000%s|r.",
	["WowheadLink"] = "Enlaces de Wowhead:",
}
L["Lang"] = {
	["deDE"] = "Alemán",
	["enUS"] = "Inglés",
	["esES"] = "Español (España)",
	["esMX"] = "Español (México)",
	["frFR"] = "Francés",
	["itIT"] = "Italiano",
	["koKR"] = "Coreano",
	["ptBR"] = "Portugués",
	["ruRU"] = "Ruso",
	["zhTW"] = "Chino",
}
L["Options"] = {
	["ReloadUIButton"] = "Recargar interfaz",
	["ResetButton"] = "Reiniciar configuración",
	["selectedLocale"] = "Idioma (Requiere recargar la interfaz)",
	["showTooltipLine"] = "Muestra el nombre del objeto localizado en una línea extra en el tooltip.",
	["showTooltipTitle"] = "Muestra el nombre del objeto localizado en el título del tooltip.",
}
L["Tooltip"] = {
	["MissingLocale"] = "Sin localización",
}

end
