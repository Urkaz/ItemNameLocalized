-- Spanish localization.
local locale = GetLocale()
if locale == 'esES' then
	local L = INL_Addon.strings;

-- Chat messages
L["Loaded"] = "Cargado idioma |cffff0000%s|r." -- %s is the locale name (enUs, esES, deDE, ... below)
L["ReloadUI_Chat"] = "Recarga la interfaz para cargar el idioma |cffff0000%s|r." -- %s is the locale name (enUs, esES, deDE, ... below)

-- Tooltip
L["Missing locale"] = "Sin localización"

-- Options
L["showTooltipTitle"] = "Muestra el nombre del objeto localizado en el título del tooltip.";
L["showTooltipLine"] = "Muestra el nombre del objeto localizado en una línea extra en el tooltip.";
L["selectedLocale"] = "Idioma (Requiere reiniciar la interfaz)"
L["ReloadUIButton"] = "Recargar interfaz"
L["ResetButton"] = "Reiniciar configuración"
L["enUS"] = "Inglés"
L["esES"] = "Español"
L["frFR"] = "Francés"
L["itIT"] = "Italiano"
L["deDE"] = "Alemán"
L["ptBR"] = "Portugués"
L["ruRU"] = "Ruso"

end
