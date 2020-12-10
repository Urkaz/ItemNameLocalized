-- German localization.
local locale = GetLocale()
if locale == 'ptBR' then
	local L = INL_Addon.strings;

L["Chat"] = {
	["Loaded"] = "Carregada linguagem |cffff0000%s|r.",
	["ReloadUI"] = "Recarregue a Interface para aplicar a língua |cffff0000%s|r.",
	["WowheadLink"] = "Link do Wowhead:",
}
L["Lang"] = {
	["deDE"] = "Alemão",
	["enUS"] = "Inglês",
	["esES"] = "Espanhol (Espanha)",
	["esMX"] = "Espanhol (México)",
	["frFR"] = "Francês",
	["itIT"] = "Italiano",
	["koKR"] = "Coreano",
	["ptBR"] = "Português (Brasil)",
	["ruRU"] = "Russo",
	["zhCN"] = "Chinês simplificado",
	["zhTW"] = "Chinês tradicional",
}
L["Options"] = {
	["ReloadUIButton"] = "Recarregar Interface",
	["ResetButton"] = "Voltar à configuração padrão",
	["selectedLocale"] = "Linguagem (Será necessário recarregar)",
	["showTooltipLine"] = "Mostrar a tradução em uma linha no tooltip.",
	["showTooltipTitle"] = "Mostrar a tradução no título do tooltip.",
}
L["Tooltip"] = {
	["MissingLocale"] = "Linguagem em falta.",
}

end
