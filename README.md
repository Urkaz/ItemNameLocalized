# Item Name Localized

[Download it on Curse](https://mods.curse.com/addons/wow/item-name-localized)

ItemNameLocalized is an addon that allows you to see the in item tooltips their name in a different language, always keeping the original name.

Now you can tell to that friend that plays WoW with a different language the name of that item you looted, or find it on AskMrRobot upgrade finder.

The addon uses 25-30 MB of memory since all the item names of the selected locale are in the memory. The other available locales are "deleted" to free memory after the addon is loaded, so selecting another locale from the options menu will require a UI reload to get the new locale loaded.

All names and IDs are obtained from the official API, if some item is not localized in some language, tell me and I will try to add it as soon as possible.

### Locales supported
* enUS (8.0.1)
* esES (8.0.1)
* esMX (8.0.1)
* frFR (8.0.1)
* deDE (8.0.1)
* itIT (8.0.1)
* ptBR (8.0.1)
* ruRU (8.0.1)
* koKR (8.0.1)
* zhTW (8.0.1)

### Current features
* Add the item name on the tooltip title.
* Add the item name on a single extra line on the tooltip.
* Generate Wowhead URLs of any item with a command (/inl link [shift+click one or more items]).

### TODO
* Maybe move each language into a separate add-on module with an individual download to reduce the total size or something like that? 
* Make the parser check if the item name is different than the one we have stored, and if it is, change it.

### Known issues
* Korean items lose the quality color in the tooltip name.