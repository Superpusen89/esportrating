# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

key = 'C60B2F253D948B27317D3EE293EE04ED'

#getLeagueListing
query_params1 = { 'key': key 
		       }
endpoint1 = 'http://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v0001/'



#getMatchHistory

endpoint2 = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v0001/'


#getMatchDetails
query_params = { 'key': 'C60B2F253D948B27317D3EE293EE04ED',
                'match_id': '992769598' 
		       }

endpoint3 = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v0001/'



#getPlayerSummaries
endpoint4 = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'


