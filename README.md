# Discord Bot
The discord bot allows members of a server to share administrator powers. Members are able to vote in order to use administrator powers such as muting or unmuting.
The bot sends a poll to the server whenever a member wants to use an administrator power.  If a certain amount of people vote in favor for using the admin power, then
the power is used.  For certain powers like muting, the bot only mutes the muted member for a ceratin predetermined amount of time.  The JSON file above is used to
store time logs for when the member was intially muted.  After the predetermined time has elapsed, the member will be unmuted. 
