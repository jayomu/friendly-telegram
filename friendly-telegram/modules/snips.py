# -*- coding: future_fstrings -*-

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils

import logging

from telethon import functions, types
from userbot import (BOTLOG_CHATID)
logger = logging.getLogger(__name__)

def register(cb):
    cb(Snips())


class Snips(loader.Module):
    """Provides a message saying that you are unavailable (out of office)"""
    def __init__(self):
        self.name = _("Snips")
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._me = await client.get_me()
        
    async def snipcmd(self, message):
        """ADDS A SNIP INTO THE LIST"""
        snipn = utils.get_args_raw(message)
        getr = await message.get_reply_message()
        if not getr:
        	await message.reply("<code>Reply to a message first!</code>")
        	return
        while snipn.strip() == (""):
        	await message.edit("<code>Please type a name for the snip.</code>")
        	return
        snipv = getr.text
        sniplist = self._db.get(__name__, "sniplist", [])
        if getr.media:
        	fwd = await self._client.forward_messages(BOTLOG_CHATID, getr, message.chat_id)
        	sniplist.update({snipn: fwd.id})
        	self._db.set(__name__, "sniplist", sniplist)
        	await message.edit("<code>Snip '" + snipn + "' successfully saved into the list. Type .getsnip " + snipn + " to call it.</code>"
        	"\n\n<code>Others can access it via $" + snipn + "</code>"
        	)
        	return
        elif not snipv:
        	await message.edit("<code>Please reply to a message to save as snip.</code>")
        	return
        if len(sniplist) != 0:
        	sniplist.update({snipn: snipv})
        	pass
        else:
        	sniplist = {snipn: snipv}
        	pass
        self._db.set(__name__, "sniplist", sniplist)
        await message.edit("<code>Snip '" + snipn + "' successfully saved into the list. Type .getsnip " + snipn + " to call it.</code>"
        "\n\n<code>Others can access it via $" + snipn + "</code>"
        )
        
    async def sniprmcmd(self, message):
        """REMOVES A SNIP FROM THE LIST"""
        snipn = utils.get_args_raw(message)
        get = self._db.get(__name__, "sniplist", [])
        while snipn.strip() == "" or not snipn:
        	await message.edit("<code>Please specify the name of the snip.</code>")
        	return
        if snipn in get:
        	del get[snipn]
        	self._db.get(__name__, "sniplist", get)
        	await message.edit("<code>Snip '" + snipn + "' successfully removed from the list.</code>")
        else:
        	await message.edit("<code>Snip '" + snipn + "' not found in snips list</code>")
        
    async def snipsrmcmd(self, message):
        """CLEARS OUT THE SNIP LIST"""
        get = self._db.get(__name__, "sniplist", [])
        get.clear()
        self._db.set(__name__, "sniplist", get)
        await message.edit("<code>All snips successfully removed from the list.</code>")
        	    	
    async def snipscmd(self, message):
        """SHOWS SAVED SNIPS"""
        snips = ""
        get = self._db.get(__name__, "sniplist", [])
        i = 0
        try:
        	for i in range(len(get)):
        		snips += "   »  <b>" + list(get.keys())[i] + "</b>\n"
        		pass
        except: pass
        snipl = "<code>Snips that you saved: </code>\n\n" + snips
        if snips.strip() != "":
        	await message.edit(snipl)
        else:
        	await message.edit('<code>No snip found in snips list.</code>')
        	
    async def getsnipcmd(self, message):
    	snip = utils.get_args_raw(message)
    	get = self._db.get(__name__, "sniplist", [])
    	val = get.get(snip)
    	if isinstance(val, int) == True:
    		await message.edit("<code>Snip '" + snip + "' has been called.</code>")
    		fwd = await self._client.forward_messages(message.chat_id, val, BOTLOG_CHATID)
    		return
    	if val:
    		await message.edit("<code>Snip '" + snip + "' has been called.</code>")
    		await message.reply(val)
    	else:
    		await message.edit("<code>No snip found in that name.</code>")
    		return
    		
    async def otherscmd(self, message):
    	state = utils.get_args_raw(message)
    	if state == "on":
    		self._db.set("snips", "others", "on")
    		await message.edit("<code>Snips are now open to use for anyone.</code>")
    		return
    	elif state == "off":
    		self._db.set("snips", "others", "off")
    		await message.edit("<code>Snips are now turned off for others.</code>")
    		return
    		
    async def watcher(self, message):
    	get = self._db.get(__name__, "sniplist", [])
    	state = self._db.get("snips", "others")
    	args = message.text
    	argsraw = args.replace("$", "")
    	if getattr(message.to_id, "user_id", None) != message.from_id and args.find("$") != -1 and state == "on":
    		val = get.get(argsraw)
    		if isinstance(val, int) == True:
    			await message.edit("<code>Snip '" + argsraw + "' has been called.</code>")
    			fwd = await self._client.forward_messages(message.chat_id, val, BOTLOG_CHATID)
    			return
    		else:
    			await message.reply(val)
    			return