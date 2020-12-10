-- German localization.
local locale = GetLocale()
if locale == 'koKR' then
	local L = INL_Addon.strings;


L["Chat"] = {
	["Loaded"] = "|cffff0000%s|r 로케일을 불러왔습니다.",
	["ReloadUI"] = "|cffff0000%s|r 로케일을 불러오려면 UI를 다시 불러와야 합니다.",
	["WowheadLink"] = "Wowhead 링크:",
}
L["Lang"] = {
	["deDE"] = "독일어",
	["enUS"] = "영어",
	["esES"] = "스페인어 (스페인)",
	["esMX"] = "스페인어 (멕시코)",
	["frFR"] = "프랑스어",
	["itIT"] = "이탈리아어",
	["koKR"] = "한국어",
	["ptBR"] = "포르투갈어",
	["ruRU"] = "러시아어",
	["zhCN"] = "중국어 간체",
	["zhTW"] = "중국어 번체",
}
L["Options"] = {
	["ReloadUIButton"] = "UI 다시 불러오기",
	["ResetButton"] = "기본 설정 초기화",
	["selectedLocale"] = "언어 (UI 다시 불러오기 필요)",
	["showTooltipLine"] = "툴팁에 현지화된 문자열 줄을 표시합니다.",
	["showTooltipTitle"] = "툴팁 제목에 현지화된 문자열을 표시합니다.",
}
L["Tooltip"] = {
	["MissingLocale"] = "누락된 로케일",
}

end
