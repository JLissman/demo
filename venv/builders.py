import database as db




def build_consultants(data):
    finalHTML = ""
    for consult in data:
        start = '<li class="entity-result"> <div class="searchResult"> <div class="result-img"> <img class="profile-img"src="' + \
                consult[4] + '"> </div> <div class="result-name">' + consult[1] +' '+ consult[2] + '</div> <div class="result-role">' + consult[3] + '</div> <div class="table"> <ul class="result-tags-list">'
        tags = db.get_tags(consult[0])
        HTMLtags = ""
        for tag in tags:
            HTMLtags = HTMLtags + '<li class="tag">' + tag[0] + '</li>'

        end = '</ul></div><div class="description">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ligula urna,pharetra id accumsan sit amet, congue sed erat. Integer sed finibus enim. Donec sit amet bibendumsapien. </div> <div class="result-location"><img class="location-tag"src="https://flyclipart.com/thumb2/location-pin-emoji-934877.png">' + \
              consult[5] + '</div></div></li>'
        finalHTML = finalHTML + start + HTMLtags + end;
    return finalHTML



def build_tags():
    tags = db.get_all_tags()
    html_tags = ""
    for tag in tags:
        html_tags = html_tags + '<option value = "'+tag[0]+'"> '+tag[0]+' </ option>'
    return html_tags