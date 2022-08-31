let inputfieldTag = document.getElementById('searchTags');
let dataOptionTags = document.getElementById('programmingLanguages');
let tagOption = [...dataOptionTags.options].map(o => o.text.toLowerCase());

let inputfieldName = document.getElementById('searchName');
let dataOptionNames = document.getElementById('nameList');
let nameOptions = [...dataOptionNames.options].map(o => o.text.toLowerCase());

let inputfieldTitle = document.getElementById('searchTitle');
let dataOptionTitle = document.getElementById('titleList');
let titleOptions = [...dataOptionTitle.options].map(o => o.text.toLowerCase());

let inputfieldLocation = document.getElementById('searchLocation');
let dataOptionLocation = document.getElementById('locationList');
let locationOptions = [...dataOptionLocation.options].map(o => o.text.toLowerCase());

let eventTriggers = ["keyup","keydown","click"];
let tags = [];
let names = [];
let roles = [];
let locations = [];
let container = document.getElementById('searchtags-container');

let button = document.getElementById('advSearchButton');

eventTriggers.forEach(function(e){
    console.log(e)
    inputfieldTag.addEventListener(e,(event)=>{
        /* do not not trigger on space in case of search like 'java enterprise'
        if(event.key == " "){
            var input = inputfield.value.toLowerCase().slice(0, -1)
            if(optionNames.includes(input)){
                console.log("Found "+input)
                addTag(input)
            }
        }*/
        if(e == "keyup"){
            event.preventDefault()
        }else{
        button.innerText = "Search"
        inputfieldTag.style.background ="white"
        inputfieldTag.placeholder = "Search for tag"
        /*
        if(event.key =="Enter" && event.shiftKey){
            event.preventDefault()
            if(tags.length > 0){
            searchString = "/search?query="
            for(let x = 0; x < tags.length; x++){
                if(x==tags.length-1){
                console.log("x"+x)
                console.log("tags"+tags.length)
                searchString = searchString + tags[x]
                }
                else{
                searchString = searchString + tags[x]+","
            }
            window.location = searchString; }//setTimeout(() => { function() , 5000);
            }}
            */
        if(event.key == "Enter"){
            document.getElementById('searchtags-container').style.display = "flex"
            event.preventDefault()
            var input = inputfieldTag.value.toLowerCase()
            if(tagOption.includes(input)){
                addTag(input)
                inputfieldTag.value = ""
                inputfieldTag.placeholder = "Search for tag"
            }
            else{
                inputfieldTag.value = ""
                inputfieldTag.style.background ="#ce4242"
                inputfieldTag.placeholder="Tag not found!"
            }
        }
        }});
        inputfieldName.addEventListener(e, (event) =>{
        if(e == "keyup"){
            event.preventDefault()
        }else{
            button.innerText = "Search"
            if(event.key == "Enter"){
                document.getElementById('searchtags-container').style.display = "flex"
                event.preventDefault()
                var input = inputfieldName.value.toLowerCase()
                if(nameOptions.includes(input)){
                    addTag(input)
                    inputfieldName.value = ""
                    inputfieldName.placeholder = "Search for Name"
                }
                else{
                    inputfieldName.value = ""
                    inputfieldName.style.background ="#ce4242"
                    inputfieldName.placeholder="Name not found!"
                }
        }
        }


        });
        inputfieldTitle.addEventListener(e, (event) =>{
        if(e == "keyup"){
            event.preventDefault()
        }

        console.log("inputfieldTitle eventlistener")


        });
        inputfieldLocation.addEventListener(e, (event) =>{
        if(e == "keyup"){
            event.preventDefault()
        }
        console.log("inputfieldLocation eventlistener")


        });
        button.addEventListener(e, (event)=>{
        event.preventDefault()
        console.log("button click")
        if(tags.length > 0){
            searchString = "/search?query="
            for(let x = 0; x < tags.length; x++){
                if(x==tags.length-1){
                console.log("x"+x)
                console.log("tags"+tags.length)
                searchString = searchString + tags[x]
                }
                else{
                searchString = searchString + tags[x]+","
            }
            window.location = searchString; }//setTimeout(() => { function() , 5000);
        }else{
            button.innerText = "No filters added"
        }
        });
});


function addTag(tag){
    if(tag.length != 0){
    const index = tags.indexOf(tag);
    if(index == -1){
        console.log("adding tag "+tag);
        container.innerHTML = container.innerHTML + "<div class='searchtag'>"+ tag +"<a href='#' class='removetag' onclick='removeTag(this)'>&#215;</a></div>";
        tags.push(tag);
    }
    else{
    console.log(tag+" already in list");
    }
}}

function removeTag(tag){
    tagName = tag.parentElement.innerText.slice(0, -1);
    const index = tags.indexOf(tagName);
    if (index > -1) {
        tags.splice(index, 1);
        container.innerHTML = container.innerHTML.replace(tag.parentElement.outerHTML, "");
    }
    console.log(tags.length);

}
