function ExecPythonCommand(pythonCommand){
    var request = new XMLHttpRequest()
    request.open("GET", "/" + pythonCommand, true)
    request.send()
}

//############ Add new Consult #############
let addConsultTagList=[]
eventTriggers = ["keyup","keydown"]
addNewConsultSubmitButton = document.getElementById('submitNewConsult')
document.querySelectorAll('.addField').forEach(item => {
    eventTriggers.forEach(trigger => {
        item.addEventListener(trigger, event => {
            if(trigger == "keyup"){
                item.style.backgroundColor ="white"
                item.placeholder = item.name
                event.preventDefault()
                }
                else{
                if(event.key == "Enter"){
                    event.preventDefault()
                    if(item.getAttribute('name') == "tags"){
                        if(optionNames.includes(item.value.toLowerCase())){
                            addTag(item.value,'addTagsContainer')
                            item.value = ""
                            item.placeholder = "Add new tag"
                            }
                    else{
                        item.value = ""
                        item.placeholder = "Tag not found"
                        }
                    }
                }
            }
        })
        })
        })

addNewConsultSubmitButton.addEventListener('click', (event)=>{
    event.preventDefault()
    filledFields = 0
    document.querySelectorAll('.addField').forEach(field =>{
        if(field.value.length > 0){
            filledFields++
        }
        else
        {
            field.style.backgroundColor ="red"
            field.placeholder = "Required Field"
        }
    })
    if(filledFields == 6 && addConsultTagList.length > 0){
    inputfield = document.getElementById('addNewConsult-tags')
    addConsultTagList.forEach(e =>inputfield.value = inputfield.value + ":" + e )
    document.getElementById('addNewConsultForm').submit()
    }})


//################# add / remove tag ##################
tagSubmitButton = document.getElementById('submitNewOrRemoveTag')
tagSelectField = document.getElementById('tagAddRemoveSelect')
tagTextField = document.getElementById('tagAddRemoveField')
tagRemoveFieldContainer = document.getElementById('addRemoveFieldChangerContainer')
let tagChangeForm = document.getElementById('tagChange')

tagSelectField.addEventListener('change', (event)=>{
    tagSubmitButton.innerText = tagSelectField.value
    console.log(tagSelectField.value)

    if(tagSelectField.value == 'Add Tag'){
        console.log("change to input")
        tagChangeForm.action = "admin/tag/add"
        tagRemoveFieldContainer.innerHTML = '<input id="tagAddRemoveField" text="text" name="tag" placeholder="Tagname">'
    }
    else if(tagSelectField.value =='Remove Tag'){
        console.log("change to select")
        tagChangeForm.action = "admin/tag/remove"
        tagRemoveFieldContainer.innerHTML = '<input list="programmingLanguages" id="tagAddRemoveField" text="text" name="tag" placeholder="Tagname">'
    }

})

tagSubmitButton.addEventListener('click', (event)=>{
    let tagTextField = document.getElementById('tagAddRemoveField')

    let dataOptionTags = document.getElementById('programmingLanguages');
    let tagOption = [...dataOptionTags.options].map(o => o.text.toLowerCase());
    event.preventDefault()
    operation = tagSelectField.value
    tag = tagTextField.value.toLowerCase()
    if (operation == 'Remove Tag' && tagOption.includes(tag)){
           tagChangeForm.submit()
    }
    else if (operation == 'Add Tag'){
        if(!tagOption.includes(tag)){
        tagChangeForm.submit()
        }else{
        alert("TAG ALREADY EXISTS")
        }
    }


})


//######### remove tag
removeTagNameField = document.getElementById('removeTagConsult')


removeTagNameField.addEventListener('change', (event)=>{
    consult_id = removeTagNameField.value
    tagContainers = document.getElementsByClassName('consultTagContainer')
    for(x=0;x<tagContainers.length;x++){
        if(tagContainers[x].getAttribute('value') == consult_id){
            regex = /[\'‘’\"“”]/g
            tags = tagContainers[x].innerText.replace(regex,"").replace("[","").replace("]","").split(",")
        }
    }
    if(tags.length > 0){
    tagDataList = document.getElementById('specificTagsConsult')
    tagDataList.innerHTML = ""
    tags.forEach(tag => tagDataList.innerHTML = tagDataList.innerHTML + '<option value="'+tag.trim()+'">'+tag.trim()+'</option>' )
    console.log(tags)
    }
    //tagOption = [...tagContainers].map(o => o.getAttribute('value'));
    //tagOption.forEach(function(container_id){
     //  if(container_id == consult_id){
      //
      //  }})

    })