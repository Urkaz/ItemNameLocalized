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

local vers	= "1.5.2"
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
SlashCmdList["INL"] = function(...) INL.CommandHandler(...); end;

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
	elseif command == "link" then
		local links = {}
		local pattern = "(%|c.-%|r)"

		local first, last, s = string.find(rest, pattern)
		local i = 1
		while s ~= nil do
			links[i] = s
			i = i + 1
			rest = string.sub(rest, 0, first-1) .. string.sub(rest, last)
			first, last, s = string.find(rest, pattern)
		end

		print("|cffff0000INL:|r " .. L.Chat.WowheadLink)
		for i, link in ipairs(links) do
			local newLink, id = INL.LocalizeHyperlink(link)

			if id then
				local whLang = ""
				local locale = INL.settings.selectedLocale
				if locale == "esES" or locale == "esMX" then
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
				elseif locale == "koKR" then
					whLang = "ko."
				elseif locale == "zhTW" then
					whLang = "cn."
				end

				print("[" .. i .. "] " .. newLink .. ": http://" .. whLang .. "wowhead.com/item=" .. id)
			end
		end
	else
		InterfaceOptionsFrame_OpenToCategory(INL.configPanel);
		InterfaceOptionsFrame_OpenToCategory(INL.configPanel); -- Blizz bug workaround
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
	checkTitle.text:SetText(L.Options.showTooltipTitle)
	checkTitle:SetPoint("TOPLEFT",30,-50)
	checkTitle:SetScript("OnClick", function(self) INL.CheckBoxOnClick(self) end)

	local checkLine = CreateFrame("CheckButton", "INLShowTooltipLineCheck", opt,"UICheckButtonTemplate")
	checkLine.var = "showTooltipLine"
	checkLine.text:SetFontObject("GameFontNormal")
	checkLine.text:SetText(L.Options.showTooltipLine)
	checkLine:SetPoint("TOPLEFT",30,-50-32)
	checkLine:SetScript("OnClick", function(self) INL.CheckBoxOnClick(self) end)

	local dropDown = CreateFrame("Frame", "INLDropDown", opt, "UIDropDownMenuTemplate")
	dropDown:SetPoint("TOPLEFT",30,-70-2*32)

	local dropDownText = dropDown:CreateFontString("INLConfigDropLabelLocale", "BACKGROUND", "GameFontNormal")
	dropDownText:SetPoint("BOTTOMLEFT", dropDown, "TOPLEFT", 16, 3)
	dropDown.Text = dropDownText

	dropDown.Text:SetText(L.Options.selectedLocale)
	dropDown.configKey = "selectedLocale"

	UIDropDownMenu_SetWidth(dropDown, 150)
	UIDropDownMenu_SetText(dropDown, L.Lang[INL.settings.selectedLocale])

	dropDown.initialize = INL.DropDownInit

	local reloadButton = CreateFrame("Button", "INLReloadButton", opt, "UIPanelButtonTemplate")
	reloadButton:SetPoint("TOP",-110,-80-3*32)
	reloadButton:SetText(L.Options.ReloadUIButton)
	reloadButton:SetWidth(200)
	reloadButton:SetScript("OnClick", function(self) ReloadUI() end)

	local resetButton = CreateFrame("Button", "INLResetButton", opt, "UIPanelButtonTemplate")
	resetButton:SetPoint("TOP",110,-80-3*32)
	resetButton:SetText(L.Options.ResetButton)
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

INL.DropDownInit = function()
	local locales = {"enUS", "esES", "esMX", "frFR", "deDE", "itIT", "ptBR", "ruRU", "koKR", "zhTW"}
	local info = {}

	wipe(info)
	info.func = INL.DropDownOnClick

	for i, locale in ipairs(locales) do
		info.text = L.Lang[locale]
		info.arg1 = locale
		info.checked = INL.settings.selectedLocale == locale
		--if locale == "esMX" then
		--	info.disabled = true
		--else
		info.disabled = false
		--end
		UIDropDownMenu_AddButton(info)
	end
end

INL.DropDownOnClick = function(self, arg1, arg2, checked)
	INL.settings.selectedLocale = arg1
	INL.requireReload = true
	INL_Settings = INL.settings
	UIDropDownMenu_SetText(INL.config[2], L.Lang[arg1])
	print("|cffff0000INL|r: " .. string.format(L.Chat.ReloadUI, L.Lang[arg1]));
end

INL.CheckBoxOnClick = function(self)
	INL.settings[self.var] = self:GetChecked()
	INL_Settings = INL.settings
end

-- TOOLTIP
INL.AddTooltipLine = function(tooltip, name, color, label)
	local found = false

	-- Check if we already added to this tooltip.
	for i = 1,15 do
		local frame = _G[tooltip:GetName() .. "TextLeft" .. i]
		local text
		if frame then text = frame:GetText() end
		if text and text == label then found = true break end
	end

	--print(found)
	
	if not found then
		tooltip:AddDoubleLine(label, "|c" .. color .. name)
		tooltip:Show()
	end
end

INL.AppendTooltipTitle = function(tooltip, name, color, index)
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

			if id and color then
				itemIndex = INL.FindIndex(id,1,table.maxn(INL.items))
				if itemIndex then
					if INL.settings.showTooltipLine then
						INL.AddTooltipLine(self, INL.items[itemIndex][2], color, L.Lang[INL.settings.selectedLocale] .. ":")
					end
					if INL.settings.showTooltipTitle then
						INL.AppendTooltipTitle(self, INL.items[itemIndex][2], color, index)
					end
				else
					if INL.settings.showTooltipLine then
						INL.AddTooltipLine(self, L.Tooltip.MissingLocale .. " #".. id, "ffff0000", L.Lang[INL.settings.selectedLocale] .. ":")
					end
					if INL.settings.showTooltipTitle then
						INL.AppendTooltipTitle(self, "|cffff0000" .. L.Tooltip.MissingLocale .. " #".. id .."|r", color, index)
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
	INL.items = INL_Items[locale]

	for k, v in pairs(INL_Items) do
        if k ~= locale then
			wipe(INL_Items[k])
			INL_Items[k] = nil
		end
    end

	wipe(INL_Items)
	INL_Items = nil

	collectgarbage()
	UpdateAddOnMemoryUsage()

	print(string.format(L.Chat.Loaded, L.Lang[locale]));
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

INL.LocalizeHyperlink = function(link)
	local id = INL.GetItemIDFromLink(link)

	if id then
		local itemIndex = INL.FindIndex(id,1,table.maxn(INL.items))
		if itemIndex then
			local newLink = string.gsub(link, "%[.*%]", "[" .. INL.items[itemIndex][2] .. "]")
			return newLink, id
		end
	end
	return link, nil
end