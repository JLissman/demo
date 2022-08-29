let inputfield = document.getElementById('search')
let dataOption = document.getElementById('programmingLanguages')
let optionNames = [...dataOption.options].map(o => o.text.toLowerCase());
let eventTriggers = ["keyup","keydown"]
let tags = []
let container = document.getElementById('searchtags-container');

eventTriggers.forEach(function(e){
    inputfield.addEventListener(e,(event)=>{
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
        inputfield.style.background ="white"
        inputfield.placeholder = "Search for tag"
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
        else if(event.key == "Enter"){
            document.getElementById('searchtags-container').style.display = "flex"
            event.preventDefault()
            var input = inputfield.value.toLowerCase()
            if(optionNames.includes(input)){
                addTag(input)
                inputfield.value = ""
                inputfield.placeholder = "Search for tag"
            }
            else{
                inputfield.value = ""
                inputfield.style.background ="#ce4242"
                inputfield.placeholder="Tag not found!"
            }
        }
        }});
});


function addTag(tag){
    if(tag.length != 0){
    const index = tags.indexOf(tag)
    if(index == -1){
        console.log("adding tag "+tag)
        container.innerHTML = container.innerHTML + "<div class='searchtag'>"+ tag +"<a href='#' class='removetag' onclick='removeTag(this)'>&#215;</a></div>"
        tags.push(tag)
    }
    else{
    console.log(tag+" already in list")
    }
}}

function removeTag(tag){
    tagName = tag.parentElement.innerText.slice(0, -1)
    const index = tags.indexOf(tagName);
    if (index > -1) {
        tags.splice(index, 1)
        container.innerHTML = container.innerHTML.replace(tag.parentElement.outerHTML, "")
    }
    console.log(tags.length)

}
