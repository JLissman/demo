
    <script type="text/javascript" src="{{ url_for('static', filename='js/searchResults.js')}}"></script>


    function searchResults(data) {
        console.log("running script")
        data = {{data|tojson}}
        console.log(data[0][2])
        for (let x = 0; x <= data.length;x++) {
            console.log("working on " + x + " result")
            let start = '<li className="entity-result"> <div className="searchResult"> <div className="result-img"> <img className="profile-img"src="' + data[x][4] + '"> </div> <div className="result-name">' + data[x][1] + '</div> <div className="result-role">' + data[x][2] + '</div> <div className="table"> <ul className="result-tags-list">'
            let tags = data[x][3].split(",")
            HTMLtags = ""
            for (let y = 0; y < tags.length; y++){
                HTMLtags = HTMLtags + '<li className="tag">' + tags[y] + '</li>'
                }
            let end = '</ul></div><div className="description">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam ligula urna,pharetra id accumsan sit amet, congue sed erat. Integer sed finibus enim. Donec sit amet bibendumsapien. </div> <div className="result-location"><img className="location-tag"src="https://flyclipart.com/thumb2/location-pin-emoji-934877.png">'+data[x][5]+'</div></div></li>'

        finishedHTML = start + HTMLtags + end;
        console.log(finishedHTML)
        }
    document.getElementById("results").innerHTML = document.getElementById("results").innerHTML + finishedHTML;
    }