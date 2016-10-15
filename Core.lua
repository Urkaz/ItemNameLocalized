local defaultSettings = {
	showTooltipTitle = true,
	showTooltipLine = false,
	selectedLocale = "enUS"
}

INL_Addon = {
	settings = defaultSettings,
	strings = {},
	items = {},
	config = {},
	configPanel = nil,
	requireReload = false,
};

local vers	= "1.0"
local INL	= INL_Addon
local L 	= INL_Addon.strings

-- SAVED VARIABLES
local eventFrame = CreateFrame("FRAME"); -- Need a frame to respond to events
eventFrame:RegisterEvent("ADDON_LOADED"); -- Fired when saved variables are loaded
eventFrame:RegisterEvent("PLAYER_LOGIN");
eventFrame:RegisterEvent("PLAYER_LOGOUT"); -- Fired when about to log out
eventFrame:SetScript("OnEvent", function(...) INL.OnEvent(...); end);

-- TOOLTIP
GameTooltip:HookScript("OnTooltipSetItem", function(self) INL.AttachItemTooltip(self, 1); end) -- Mouse over tooltip
ItemRefTooltip:HookScript("OnTooltipSetItem", function(self) INL.AttachItemTooltip(self, 1); end) -- Chat tooltip
ItemRefShoppingTooltip1:HookScript("OnTooltipSetItem", function(self) INL.AttachItemTooltip(self, 2); end) -- Compare chat item with shift
ItemRefShoppingTooltip2:HookScript("OnTooltipSetItem", function(self) INL.AttachItemTooltip(self, 2); end)
ShoppingTooltip1:HookScript("OnTooltipSetItem", function(self) INL.AttachItemTooltip(self, 2); end) -- Compare bag item bith shift
ShoppingTooltip2:HookScript("OnTooltipSetItem", function(self) INL.AttachItemTooltip(self, 2); end)

-- SLASH COMMANDS
SLASH_INL1 = '/inl';
SlashCmdList["INL"] = function(...) INL.CommandHandler(...); end; -- Also a valid assignment strategy

---------------
-- FUNCTIONS --
---------------

-- EVENT & HANDLER FUNCTIONS
INL.OnEvent = function(self, event, name)
	if event == "ADDON_LOADED" and name == "ItemNameLocalized" then
		if not INL_Settings then
			INL_Settings = defaultSettings
		else
			INL.settings = INL_Settings
		end
		self:UnregisterEvent("ADDON_LOADED")
	elseif event == "PLAYER_LOGOUT" then
		INL_Settings = INL.settings
	elseif event == "PLAYER_LOGIN" then
		print("|cffff0000INL|r: version " .. vers);
		INL.CreateConfigPanel();
		INL.SelectLocaleAndFree(INL.settings.selectedLocale)
	end
end

INL.CommandHandler = function(message, editbox)
	local command, rest = message:match("^(%S*)%s*(.-)$");

	if command == "reset" then
		INL.ResetDefaultConfig()
	elseif command == "wowhead" then
		local id = INL.GetItemIDFromLink(rest)
		local color = string.match(rest, "|c(.+)|H")
		if id then
			local itemIndex = INL.FindIndex(id,1,table.maxn(INL.items))
			if itemIndex then
				local whLang = ""
				local locale = INL.settings.selectedLocale
				if locale == "esES" then
					whLang = "es."
				elseif locale == "frFR" then
					whLang = "fr."
				elseif locale == "deDE" then
					whLang = "de."
				elseif locale == "itIT" then
					whLang = "it."
				elseif locale == "ptBR" then
					whLang = "pt."
				elseif locale == "ruRU" then
					whLang = "ru."
				end

				if not color then
					color = "ffffffff"
				end

				print(string.format(L["WowheadLink"], "|c" .. color .. "[" .. INL.items[itemIndex][2] .. "]|r"))
				print("http://" .. whLang .. "wowhead.com/item=" .. id)
			end
		end
	elseif command == "print" then
		local id = INL.GetItemIDFromLink(rest)
		local color = string.match(rest, "|c(.+)|H")
		if id then
			local itemIndex = INL.FindIndex(id,1,table.maxn(INL.items))
			if itemIndex then
				if not color then
					color = "ffffffff"
				end
				print("|c" .. color .. "[" .. INL.items[itemIndex][2] .. "]|r")
			end
		end
	else
		InterfaceOptionsFrame_OpenToCategory(INL.configPanel);
	end
end

-- CONFIG
INL.CreateConfigPanel = function()

	local opt = CreateFrame("Frame")
	opt.name = "Item Name Localized"

	INL.configPanel = opt

	local title = opt:CreateFontString(nil, "ARTWORK", "GameFontNormalLarge")
	title:SetPoint("TOPLEFT", 16, -16)
	title:SetJustifyH("LEFT")
	title:SetJustifyV("TOP")
	title:SetText("Item Name Localized")

	local checkTitle = CreateFrame("CheckButton", "INLShowTooltipTitleCheck", opt,"UICheckButtonTemplate")
	checkTitle.var = "showTooltipTitle"
	checkTitle.text:SetFontObject("GameFontNormal")
	checkTitle.text:SetText(L["showTooltipTitle"])
	checkTitle:SetPoint("TOPLEFT",30,-50)
	checkTitle:SetScript("OnClick", function(self) INL.CheckBoxOnClick(self) end)

	local checkLine = CreateFrame("CheckButton", "INLShowTooltipLineCheck", opt,"UICheckButtonTemplate")
	checkLine.var = "showTooltipLine"
	checkLine.text:SetFontObject("GameFontNormal")
	checkLine.text:SetText(L["showTooltipLine"])
	checkLine:SetPoint("TOPLEFT",30,-50-32)
	checkLine:SetScript("OnClick", function(self) INL.CheckBoxOnClick(self) end)

	local dropDown = CreateFrame("Frame", "INLDropDown", opt, "UIDropDownMenuTemplate")
	dropDown:SetPoint("TOPLEFT",30,-70-2*32)

	local dropDownText = dropDown:CreateFontString("INLConfigDropLabelLocale", "BACKGROUND", "GameFontNormal")
	dropDownText:SetPoint("BOTTOMLEFT", dropDown, "TOPLEFT", 16, 3)
	dropDown.Text = dropDownText

	dropDown.Text:SetText(L["selectedLocale"])
	dropDown.configKey = "selectedLocale"

	UIDropDownMenu_SetWidth(dropDown, 150)
	UIDropDownMenu_Initialize(dropDown, INL.DropDownMenu)

	local reloadButton = CreateFrame("Button", "INLReloadButton", opt, "UIPanelButtonTemplate")
	reloadButton:SetPoint("TOP",-110,-80-3*32)
	reloadButton:SetText(L["ReloadUIButton"])
	reloadButton:SetWidth(200)
	reloadButton:SetScript("OnClick", function(self) ReloadUI() end)

	local resetButton = CreateFrame("Button", "INLResetButton", opt, "UIPanelButtonTemplate")
	resetButton:SetPoint("TOP",110,-80-3*32)
	resetButton:SetText(L["ResetButton"])
	resetButton:SetWidth(200)
	resetButton:SetScript("OnClick", function(self) INL.ResetDefaultConfig() end)

	-- Config items
	INL.config[0] = checkTitle
	INL.config[1] = checkLine
	INL.config[2] = dropDown
	INL.config[3] = reloadButton
	INL.config[4] = resetButton

	opt.refresh = function()
		for i=0,2 do
			INL.config[i]:SetChecked(INL.settings[INL.config[i].var] and true)
		end
	end

	InterfaceOptions_AddCategory(opt)
end

INL.DropDownOnClick = function(self, arg1, arg2, checked)
	INL.settings.selectedLocale = arg1
	INL.requireReload = true
	INL_Settings = INL.settings
	UIDropDownMenu_SetText(INL.config[2], L[arg1])
	print("|cffff0000INL|r: " .. string.format(L["ReloadUI_Chat"], L[arg1]));
end

INL.DropDownMenu = function(frame, level, menuList)
	UIDropDownMenu_SetText(frame, L[INL.settings.selectedLocale])

	local info = UIDropDownMenu_CreateInfo()
	info.func = INL.DropDownOnClick
	info.text, info.arg1, info.checked = L["enUS"], "enUS", INL.settings.selectedLocale == "enUS"
	UIDropDownMenu_AddButton(info)
	info.text, info.arg1, info.checked = L["esES"], "esES", INL.settings.selectedLocale == "esES"
	UIDropDownMenu_AddButton(info)
	info.text, info.arg1, info.checked = L["frFR"], "frFR", INL.settings.selectedLocale == "frFR"
	UIDropDownMenu_AddButton(info)
	info.text, info.arg1, info.checked = L["deDE"], "deDE", INL.settings.selectedLocale == "deDE"
	UIDropDownMenu_AddButton(info)
	info.disabled = true
	info.text, info.arg1, info.checked = L["itIT"], "itIT", INL.settings.selectedLocale == "itIT"
	UIDropDownMenu_AddButton(info)
	info.text, info.arg1, info.checked = L["ptBR"], "ptBR", INL.settings.selectedLocale == "ptBR"
	UIDropDownMenu_AddButton(info)
	info.text, info.arg1, info.checked = L["ruRU"], "ruRU", INL.settings.selectedLocale == "ruRU"
	UIDropDownMenu_AddButton(info)
end

INL.CheckBoxOnClick = function(self)
	INL.settings[self.var] = self:GetChecked()
	INL_Settings = INL.settings
end

-- TOOLTIP
INL.AddTooltipLine = function(tooltip, name, color, label)
	--local found = false

	-- Check if we already added to this tooltip.
	--[[for i = 1,15 do
		local frame = _G[tooltip:GetName() .. "TextLeft" .. i]
		local text
		if frame then text = frame:GetText() end
		if text and text == label then found = true break end
	end

	if not found then]]
		if color then
			tooltip:AddDoubleLine(label, "|c" .. color .. name)
		else
			tooltip:AddDoubleLine(label, "|cffffffff" .. name)
		end
		tooltip:Show()
	--end
end

INL.AppendTooltipTitle = function(tooltip, name, index)
	append = "\n[" .. name .. "]"

	local tooltipTitle = _G[tooltip:GetName() .. "TextLeft" .. index]
	if tooltipTitle then
		tooltipTitle:SetJustifyH("LEFT")
		local itemName = tooltipTitle:GetText()
		if itemName then
			if not string.find(itemName, append, 1, true) then
				tooltipTitle:SetText(itemName .. append)
			end
		end
	end
	tooltip:Show()
end

INL.AttachItemTooltip = function(self, index)
	if not INL.requireReload then
		local link = select(2, self:GetItem())

		if link then
			local id = INL.GetItemIDFromLink(link)
			local color = string.match(link, "|c(.+)|H")

			if id then
				itemIndex = INL.FindIndex(id,1,table.maxn(INL.items))
				if itemIndex then
					if INL.settings.showTooltipLine then
						INL.AddTooltipLine(self, INL.items[itemIndex][2], color, L[INL.settings.selectedLocale] .. ":")
					end
					if INL.settings.showTooltipTitle then
						INL.AppendTooltipTitle(self, INL.items[itemIndex][2], index)
					end
				else
					if INL.settings.showTooltipLine then
						INL.AddTooltipLine(self, L["MissingLocale"] .. " #".. id, "ffff0000", L[INL.settings.selectedLocale] .. ":")
					end
					if INL.settings.showTooltipTitle then
						INL.AppendTooltipTitle(self, "|cffff0000" .. L["MissingLocale"] .. " #".. id .."|r", index)
					end
				end
			end
		end
	end
end

-- OPERATION FUNCTIONS
INL.FindIndex = function(id, minI, maxI)
	guess = math.floor(minI + (maxI - minI) / 2)
	if INL.items[guess] ~= nil and maxI >= minI then
		if INL.items[guess][1] == id then
			return guess
		end
		if INL.items[guess][1] < id then
			return INL.FindIndex(id, guess + 1, maxI)
		else
			return INL.FindIndex(id, minI, guess - 1)
		end
	else
		return nil
	end
end

INL.SelectLocaleAndFree = function(locale)
	if locale == "enUS" or not locale then
		INL.items = INL_Items.en_US
	elseif locale == "esES" then
		INL.items = INL_Items.es_ES
	elseif locale == "frFR" then
		INL.items = INL_Items.fr_FR
	elseif locale == "deDE" then
		INL.items = INL_Items.de_DE
	elseif locale == "itIT" then
		INL.items = INL_Items.it_IT
	elseif locale == "ptBR" then
		INL.items = INL_Items.pt_BR
	elseif locale == "ruRU" then
		INL.items = INL_Items.ru_RU
	end

	INL_Items.en_US = nil
	INL_Items.es_ES = nil
	INL_Items.fr_FR = nil
	INL_Items.de_DE = nil
	INL_Items.it_IT = nil
	INL_Items.pt_BR = nil
	INL_Items.ru_RU = nil

	print(string.format(L["Loaded"], L[locale]));
end

INL.ResetDefaultConfig = function()
	INL.settings = default
	INL_Settings = INL.settings
	ReloadUI();
end

INL.GetItemIDFromLink = function(link)
	local id = string.match(link, "item:(%d*)")

	if (id == "" or id == "0") and TradeSkillFrame ~= nil and TradeSkillFrame:IsVisible() and GetMouseFocus().reagentIndex then
		local selectedRecipe = TradeSkillFrame.RecipeList:GetSelectedRecipeID()
		for i = 1, 8 do
			if GetMouseFocus().reagentIndex == i then
				id = C_TradeSkillUI.GetRecipeReagentItemLink(selectedRecipe, i):match("item:(%d+):") or nil
				break
			end
		end
	end
	return tonumber(id)
end
