# Item Name Localized

[Download it on Curse](https://mods.curse.com/addons/wow/item-name-localized)

ItemNameLocalized is an addon that allows you to see on the item tooltips their name in a different language, always keeping the original name.

Now you can tell to that friend that plays WoW with a different language the name of that item you looted, or find it on AskMrRobot upgrade finder.

The addon uses 20~MB of memory since all the item names of the selected locale are in the memory. The other available locales are "deleted" to free memory after the addon is loaded, so selecting other locale from the options menu will require an UI reload to get the new locale loaded.

All names and IDs are obtained from the official API, if some item is not localized in some language, tell me and I will try to add it as soon as possible.

### Locales supported
* enUS (7.0.3)
* esES (7.0.3)
* frFR (7.0.3)
* deDE (7.0.3)
* itIT (7.0.3)
* ptBR (7.0.3)
* ruRU (7.0.3)

### Locales that will be supported
* koKR (generating db)
* zhTW (generating db)

### Current features
* Add the item name on the tooltip title.
* Add the item name on a single extra line on the tooltip.
* Generate Wowhead URLs of any item with a command (/inl link [shift+click one or more items to add them]).

### Known issues
* [Should be fixed in v1.1] On the recipes the localized name appear on two different lines.
* [Should be fixed in v1.1] For some reason, there is an error saying the addon is unsafe. This should be solved on the next version, but I will continue investigating the cause.
* The new Halloween items don't have localization. Seems like these items are hidden in the battle.net API and can't be retrieved using it (WoWHead shows them as only PTR items for example), I'll try again when we get 7.1.