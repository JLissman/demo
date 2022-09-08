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
                addTag(input,'searchtags-container')
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


function addTag(tag, elementId){
    tagContainer = document.getElementById(elementId);
    if(tag.length != 0){
    const index = tags.indexOf(tag)
    if(index == -1){
        console.log("adding tag "+tag)
        tagContainer.innerHTML = tagContainer.innerHTML + "<div class='searchtag'>"+ tag +"<a href='#' class='removetag' onclick='removeTag(this)'>&#215;</a></div>"
        if(elementId == 'searchtags-container'){
        tags.push(tag)}
        else if (elementId=='addTagsContainer'){
        addConsultTagList.push(tag)
        }
    }
    else{
    console.log(tag+" already in list")
    }

}}

function removeTag(tag){
    tagName = tag.parentElement.innerText.slice(0, -1)
    parent = tag.parentElement.parentElement.id
    console.log(parent)
    tagContainer = document.getElementById(parent);
    if(parent == 'searchtags-container'){
    const index = tags.indexOf(tagName);
    if (index > -1) {

        tags.splice(index, 1)
        tagContainer.innerHTML = tagContainer.innerHTML.replace(tag.parentElement.outerHTML, "")
    }}
    else if(parent =='addTagsContainer'){
    const index = addConsultTagList.indexOf(tagName);
    if (index > -1) {
        addConsultTagList.splice(index, 1)
        tagContainer.innerHTML = tagContainer.innerHTML.replace(tag.parentElement.outerHTML, "")
    }
    }

}
