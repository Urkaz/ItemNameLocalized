local defaultSettings = {
	showTooltipTitle = true,
	showTooltipLine = false,
	selectedLocale = "enUS"
}

INL_Addon = {
	settings = defaultSettings,
	strings = {},
	items = {},
	spells = {},
	config = {},
	installedLocales = {"enUS"},
	configPanel = nil,
	requireReload = false,
};

local tipType = {
  spell = "spell",
  item = "item",
}

local vers	= "2.1"
local INL	= INL_Addon
local L 	= INL_Addon.strings

-- SAVED VARIABLES
local eventFrame = CreateFrame("FRAME"); -- Need a frame to respond to events
eventFrame:RegisterEvent("ADDON_LOADED"); -- Fired when saved variables are loaded
eventFrame:RegisterEvent("PLAYER_LOGIN");
eventFrame:RegisterEvent("PLAYER_LOGOUT"); -- Fired when about to log out
eventFrame:SetScript("OnEvent", function(...) INL.OnEvent(...); end);

-- ITEM HOOKS
GameTooltip:HookScript("OnTooltipSetItem", function(self) INL.AttachTooltip(self, nil, 1, tipType.item); end) -- Mouse over tooltip
ItemRefTooltip:HookScript("OnTooltipSetItem", function(self) INL.AttachTooltip(self, nil, 1, tipType.item); end) -- Chat tooltip
ItemRefShoppingTooltip1:HookScript("OnTooltipSetItem", function(self) INL.AttachTooltip(self, nil, 2, tipType.item); end) -- Compare chat item with shift
ItemRefShoppingTooltip2:HookScript("OnTooltipSetItem", function(self) INL.AttachTooltip(self, nil, 2, tipType.item); end)
ShoppingTooltip1:HookScript("OnTooltipSetItem", function(self) INL.AttachTooltip(self, nil, 2, tipType.item); end) -- Compare bag item with shift
ShoppingTooltip2:HookScript("OnTooltipSetItem", function(self) INL.AttachTooltip(self, nil, 2, tipType.item); end)

-- SPELLS HOOKS
hooksecurefunc(GameTooltip, "SetUnitBuff", function(self, ...)
	local id = select(10, UnitBuff(...))
	INL.AttachTooltip(self, id, 1, tipType.spell)
end)

hooksecurefunc(GameTooltip, "SetUnitDebuff", function(self, ...)
	local id = select(10, UnitDebuff(...))
	INL.AttachTooltip(self, id, 1, tipType.spell)
end)

hooksecurefunc(GameTooltip, "SetUnitAura", function(self, ...)
	local id = select(10, UnitAura(...))
	INL.AttachTooltip(self, id, 1, tipType.spell)
end)

hooksecurefunc(GameTooltip, "SetSpellByID", function(self, id)
	INL.AttachTooltip(self, id, 1, tipType.spell)
end)

hooksecurefunc("SetItemRef", function(link, text, button)
	local id = tonumber(link:match("spell:(%d+)"))
	INL.AttachTooltip(GameTooltip, id, 1, tipType.spell)
end)

GameTooltip:HookScript("OnTooltipSetSpell", function(self)
	local id = select(2, self:GetSpell())
	INL.AttachTooltip(self, id, 1, tipType.spell)
end)

ItemRefTooltip:HookScript("OnTooltipSetSpell", function(self)
	local id = select(2, self:GetSpell())
	INL.AttachTooltip(self, id, 1, tipType.spell);
end) -- Chat tooltip

hooksecurefunc("SpellButton_OnEnter", function(self)
	local slot = SpellBook_GetSpellBookSlot(self)
	local spellID = select(2, GetSpellBookItemInfo(slot, SpellBookFrame.bookType))
	INL.AttachTooltip(GameTooltip, spellID, 1, tipType.spell)
end)

-- SLASH COMMANDS
SLASH_INL1 = '/inl';
SlashCmdList["INL"] = function(...) INL.CommandHandler(...); end;

-- EVENT & HANDLER FUNCTIONS
INL.OnEvent = function(self, event, name)
	if event == "ADDON_LOADED" and name == "ItemNameLocalized_Core" then
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
		--for i,v in ipairs(INL.installedLocales) do print(i,v) end
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
			local newLink, id, kind = INL.LocalizeHyperlink(link)

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

				print("[" .. i .. "] " .. newLink .. ": http://" .. whLang .. "wowhead.com/" .. kind .. "=" .. id)
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
	dropDown.initialize = INL.DropDownInit

	local dropDownText = dropDown:CreateFontString("INLConfigDropLabelLocale", "BACKGROUND", "GameFontNormal")
	dropDownText:SetPoint("BOTTOMLEFT", dropDown, "TOPLEFT", 16, 3)
	dropDownText:SetText(L.Options.selectedLocale)

	dropDown.configKey = "selectedLocale"

	UIDropDownMenu_SetWidth(dropDown, 150)
	UIDropDownMenu_SetText(dropDown, L.Lang[INL.settings.selectedLocale])

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
	local locales = {"enUS", "esES", "esMX", "frFR", "deDE", "itIT", "ptBR", "ruRU"}
	local info = {}

	wipe(info)
	info.func = INL.DropDownOnClick

	for i, locale in ipairs(locales) do
		info.text = L.Lang[locale]
		info.arg1 = locale
		info.checked = INL.settings.selectedLocale == locale
		
		info.disabled = true
		for i2, loc in ipairs(INL.installedLocales) do
			if locale == loc then
				info.disabled = false
				break
			end
		end
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

-- ITEM TOOLTIP
INL.AddTooltipLine = function(tooltip, name, color, label)
	local found = false

	-- Check if we already added to this tooltip.
	for i = 1,15 do
		local frame = _G[tooltip:GetName() .. "TextLeft" .. i]
		local text
		if frame then text = frame:GetText() end
		if text and text == label then found = true break end
	end
	
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

INL.AttachTooltip = function(self, id, index, kind)
	if not INL.requireReload then
		local color = "ffffffff";
		
		local inId = id
	
		if kind == tipType.item then
			local link = select(2, self:GetItem())

			if link then
				a, inId = INL.GetIDFromLink(link)
				color = string.match(link, "|c(.+)|H")
			end
		end
		
		if inId and color then
			local tableToLook = nil
			if kind == tipType.item then
				tableToLook = INL.items;
			else
				if kind == tipType.spell then
					tableToLook = INL.spells;
				end
			end
			
			local listIndex = INL.FindIndex(inId, 1, table.maxn(tableToLook), tableToLook)
	
			if listIndex then
				if INL.settings.showTooltipLine then
					INL.AddTooltipLine(self, tableToLook[listIndex][2], color, L.Lang[INL.settings.selectedLocale] .. ":")
				end
				if INL.settings.showTooltipTitle then
					INL.AppendTooltipTitle(self, tableToLook[listIndex][2], color, index)
				end
			else
				if INL.settings.showTooltipLine then
					INL.AddTooltipLine(self, L.Tooltip.MissingLocale .. " #".. inId, "ffff0000", L.Lang[INL.settings.selectedLocale] .. ":")
				end
				if INL.settings.showTooltipTitle then
					INL.AppendTooltipTitle(self, "|cffff0000" .. L.Tooltip.MissingLocale .. " #".. inId .."|r", color, index)
				end
			end
		end
	end
end

-- OPERATION FUNCTIONS
INL.FindIndex = function(id, minI, maxI, tableToLook)
	guess = math.floor(minI + (maxI - minI) / 2)
	if tableToLook[guess] ~= nil and maxI >= minI then
		if tableToLook[guess][1] == id then
			return guess
		end
		if tableToLook[guess][1] < id then
			return INL.FindIndex(id, guess + 1, maxI, tableToLook)
		else
			return INL.FindIndex(id, minI, guess - 1, tableToLook)
		end
	else
		return nil
	end
end

INL.SelectLocaleAndFree = function(locale)

	-- Check if the current locale is installed
	local found = false;
	
	for i2, loc in pairs(INL.installedLocales) do
        if loc == locale then
			found = true
		end
    end

	-- if not, reset config
	if not found then
		INL.ResetDefaultConfig()
		locale = "enUS"
	end
	
	-- merge locale splits
	for key,value in pairs(INL_Items[locale]) do
		INL.TableConcat(INL.items, value)
	end
	
	for key,value in pairs(INL_Spells[locale]) do
		INL.TableConcat(INL.spells, value)
	end

	-- free unused locales memory
	for k, v in pairs(INL_Items) do
        if k ~= locale then
			wipe(INL_Items[k])
			INL_Items[k] = nil
		end
    end

	wipe(INL_Items)
	INL_Items = nil
	
	for k, v in pairs(INL_Spells) do
        if k ~= locale then
			wipe(INL_Spells[k])
			INL_Spells[k] = nil
		end
    end

	wipe(INL_Spells)
	INL_Spells = nil

	-- free memory
	collectgarbage()
	UpdateAddOnMemoryUsage()

	print(string.format(L.Chat.Loaded, L.Lang[locale]));
end

INL.ResetDefaultConfig = function()
	INL.settings = default
	INL_Settings = INL.settings
	ReloadUI();
end

INL.GetItemOrSpellFromLink = function(link)
	local itemID = string.match(link, "item:(%d*)")
	local spellID = string.match(link, "spell:(%d*)")
	if spellID then
		return tipType.spell, spellID
	end
	return tipType.item, itemID
end

INL.GetIDFromLink = function(link)
	--local id = string.match(link, "item:(%d*)")
	local kind, id = INL.GetItemOrSpellFromLink(link)
	
	if kind == tipType.item then
		if (id == "" or id == "0") and TradeSkillFrame ~= nil and TradeSkillFrame:IsVisible() and GetMouseFocus().reagentIndex then
			local selectedRecipe = TradeSkillFrame.RecipeList:GetSelectedRecipeID()
			for i = 1, 8 do
				if GetMouseFocus().reagentIndex == i then
					id = C_TradeSkillUI.GetRecipeReagentItemLink(selectedRecipe, i):match("item:(%d+):") or nil
					break
				end
			end
		end
	end
	return kind, tonumber(id)
end

INL.LocalizeHyperlink = function(link)
	local kind, id = INL.GetIDFromLink(link)

	local tableToLook = nil
	if kind == tipType.item then
		tableToLook = INL.items;
	else
		if kind == tipType.spell then
			tableToLook = INL.spells;
		end
	end
	
	if id then
		local listIndex = INL.FindIndex(id, 1, table.maxn(tableToLook), tableToLook)
		if listIndex then
			local newLink = string.gsub(link, "%[.*%]", "[" .. tableToLook[listIndex][2] .. "]")
			return newLink, id, kind
		end
	end
	return link, nil, kind
end

INL.TableConcat = function (t1,t2)
    for i=1,#t2 do
        t1[#t1+1] = t2[i]
    end
    return t1
end