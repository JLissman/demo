import database as db



#old - keeping just in case
def build_consultants(data):
    finalHTML = ""
    print(data)
    print(len(data))
    if(len(data) > 0):#8 indexes in datalist if only 1
        for consult in data:
            start = '<li class="entity-result"> <div class="searchResult"> <div class="result-img"> <img class="profile-img"src="' + \
                    consult["image_url"] + '"> </div> <div class="result-name"><a href="/profile?id='+str(consult["consult_id"])+'">' + consult["firstname"] +' '+ consult["lastname"] + '</a></div> <div class="result-role">' + consult["role"] + '</div> <div class="table"> <ul class="result-tags-list">'
            #tags = db.get_tags(consult["consult_id"])
            HTMLtags = ""
            for tag in consult["tags"]:
                HTMLtags = HTMLtags + '<li class="tag"><a class="competence-tag-link" href="/search?query=' + tag + '">'+ tag+'</a></li>'

            end = '</ul></div><div class="description">'+consult["description"]+'</div> <div class="result-location"><img class="location-tag"src="https://flyclipart.com/thumb2/location-pin-emoji-934877.png">' + \
                  consult["location"] + '</div></div></li>'
            finalHTML = finalHTML + start + HTMLtags + end;
        return finalHTML
    else:
        start = '<li class="entity-result"> <div class="searchResult"> <div class="result-img"> <img class="profile-img"src="' + \
                data["image_url"] + '"> </div> <div class="result-name"><a href="/profile?id='+str(data["consult_id"])+'">' + data["firstname"] +' '+ data["lastname"] + '</a></div> <div class="result-role">' + data["role"] + '</div> <div class="table"> <ul class="result-tags-list">'
            #tags = db.get_tags(consult["consult_id"])
        HTMLtags = ""
        for tag in data["tags"]:
            HTMLtags = HTMLtags + '<li class="tag"><a class="competence-tag-link" href="/search?query=' + tag + '">'+ tag+'</a></li>'

        end = '</ul></div><div class="description">'+data["description"]+'</div> <div class="result-location"><img class="location-tag"src="https://flyclipart.com/thumb2/location-pin-emoji-934877.png">' + \
                  data["location"] + '</div></div></li>'
        finalHTML = finalHTML + start + HTMLtags + end;
        return finalHTML




def build_consultants_v2(data):
    finalHTML = ""
    if(len(data) > 0):
        for id in data:
            if('www' in data[id]["image_url"] or 'http' in data[id]["image_url"] ):
                start = '<li class="entity-result"> <div class="searchResult"> <div class="result-img"> <img class="profile-img"src="' + \
                    data[id]["image_url"] + '"> </div> <div class="result-name"><a href="/profile?id='+ str(id) +'">' + data[id]["name"] + '</a></div> <div class="result-role">' + data[id]["role"] + '</div> <div class="table"> <ul class="result-tags-list">'
            else:
                start = '<li class="entity-result"> <div class="searchResult"> <div class="result-img"> <img class="profile-img"src="' + \
                    "{{ url_for('static', filename='"+data[id]["image_url"]+'\') }} '"> </div> <div class='result-name'><a href='/profile?id=\'"+ str(id) +'\'>' + data[id]["name"] + '</a></div> <div class="result-role">' + data[id]["role"] + '</div> <div class="table"> <ul class="result-tags-list">'


            #tags = db.get_tags(consult["consult_id"])
            HTMLtags = ""
            for tag in data[id]["tags"]:
                HTMLtags = HTMLtags + '<li class="tag"><a class="competence-tag-link" href="/search?query=' + tag + '">'+ tag+'</a></li>'

            end = '</ul></div><div class="description">'+data[id]["description"]+'</div> <div class="result-location"><img class="location-tag"src="https://flyclipart.com/thumb2/location-pin-emoji-934877.png">' + \
                  data[id]["location"] + '</div></div></li>'
            finalHTML = finalHTML + start + HTMLtags + end;
        return finalHTML
    else:
        return finalHTML

def build_tags():
    tags = db.get_all_tags()
    html_tags = ""
    for tag in tags:
        html_tags = html_tags + '<option value = "'+str(tag[1])+'"> '+str(tag[1])+' </ option>'
    return html_tags




def build_names():
    names = db.get_all_names()
    html_names = ""
    for name in names:
        html_names = html_names + '<option value = "'+str(name[0])+" "+str(name[1])+'"> '+str(name[0])+" "+str(name[1])+' </ option>'
    return html_names


def build_locations():
    locations = db.get_all_locations()
    html_locations = ""
    for location in locations:
        html_locations = html_locations + '<option value = "'+str(location[0])+'"> '+str(location[0])+' </ option>'
    return html_locations

def build_roles():
    roles = db.get_all_roles()
    html_roles = ""
    for role in roles:
        html_roles = html_roles + '<option value = "'+str(role[0])+'"> '+str(role[0])+' </ option>'
    return html_roles
