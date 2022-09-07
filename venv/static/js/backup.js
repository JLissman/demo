
/*{% if celeryStatus["availability"] == None %}
    <form action="celeryStatus"  method="post">
        <button id="celeryStartButton" name="action" value="start" type="submit">Start Celery Worker</button>
        </form>
{% else %}
    <form action="celeryStatus"  method="post">
        <button id="celeryStopButton" name="action" value="end">Kill Celery Worker</button>
        </form>
    {% endif %}*/



/*<script>
let startbutton = document.getElementById('celeryStartButton');
let endbutton = document.getElementById('celeryStopButton');



startbutton.addEventListener('click', (event) => {
    if(startbutton.innerText == "Starting..."){
        event.preventDefault()
        console.log("second start click")
    }
    else if(startbutton.innerText == "Start Celery Worker"){
    console.log("first start click")
    startbutton.innerText = "Starting..."
    }
});
endbutton.addEventListener('click', (event) =>{
    if(endbutton.innerText == "Stopping..."){
        event.preventDefault()
        console.log("second end click")
    }
    else if(endbutton.innerText == "Kill Celery Worker"){
        endbutton.innerText="Stopping..."
        console.log("first end click")
    }


});
</script>*/