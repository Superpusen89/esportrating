# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

key = 'C60B2F253D948B27317D3EE293EE04ED'
steam_number = 76561197960265728

#getLeagueListing
query_params1 = { 'key': key 
		       }
endpoint1 = 'http://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001/'



#getMatchHistory

endpoint2 = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v0001/'


#getMatchDetails

endpoint3 = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v0001/'



#getPlayerSummaries
endpoint4 = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'


#getTeamInfoByTeamID


endpoint5 = 'http://api.steampowered.com/IDOTA2Match_570/GetTeamInfoByTeamID/v0001/'



#getMatchHistoryFromMatchID

endpoint6 = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v0001/'
param = '?key=C60B2F253D948B27317D3EE293EE04ED&league_id=65001&start_at_match_id=37584550'

