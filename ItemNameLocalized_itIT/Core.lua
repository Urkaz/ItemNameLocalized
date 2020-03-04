-- SAVED VARIABLES
local eventFrame = CreateFrame("FRAME"); -- Need a frame to respond to events
eventFrame:RegisterEvent("ADDON_LOADED"); -- Fired when saved variables are loaded
eventFrame:SetScript("OnEvent", function(...) OnEvent(...); end);

-- EVENT & HANDLER FUNCTIONS
OnEvent = function(self, event, name)
	if event == "ADDON_LOADED" and name == "ItemNameLocalized_itIT" then
		if INL_Addon then
			table.insert(INL_Addon.installedLocales, "itIT")
			self:UnregisterEvent("ADDON_LOADED")
		end
	end
end