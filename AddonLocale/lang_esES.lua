-- Spanish localization.
local locale = GetLocale()
if locale == 'esES' or locale == 'esMX' then
	local L = INL_Addon.strings;

L = {
	["Chat"] = {
		["Loaded"] = "Cargado idioma |cffff0000%s|r.",
		["ReloadUI"] = "Recarga la interfaz para cargar el idioma |cffff0000%s|r.",
		["WowheadLink"] = "Enlaces de Wowhead:"
	},
	["Lang"] = {
		["deDE"] = "Alemán",
		["enUS"] = "Inglés",
		["esES"] = "Español",
		["frFR"] = "Francés",
		["itIT"] = "Italiano",
		["koKR"] = "Coreano",
		["ptBR"] = "Portugués",
		["ruRU"] = "Ruso",
		["zhTW"] = "Chino"
	},
	["Options"] = {
		["ReloadUIButton"] = "Recargar interfaz",
		["ResetButton"] = "Reiniciar configuración",
		["selectedLocale"] = "Idioma (Requiere reiniciar la interfaz)",
		["showTooltipLine"] = "Muestra el nombre del objeto localizado en una línea extra en el tooltip.",
		["showTooltipTitle"] = "Muestra el nombre del objeto localizado en el título del tooltip."
	},
	["Tooltip"] = {
		["MissingLocale"] = "Sin localización"
	}
}

end
