

function add_column(){
    var text_area = document.getElementById('message');
    var select = document.getElementById('column-select');
    if (select.options[select.selectedIndex].text != "Datos"){
        text_area.value = text_area.value + "{" + select.options[select.selectedIndex].text + "} ";
    }
    else{
        alert("Seleccione una columna")
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

function check_message(){
    msg = document.getElementById('message').value;
    df = document.getElementById('test').value;
    
    axios.post('/check_message/', {
        
        message:msg,
        test: df
    })
    .then(function (response){
        popup = document.getElementById('popup-windo')
        message = response.data['message'];
        const d = new Date();
        let h = addZero(d.getHours());
        let m = addZero(d.getMinutes());
        let half = "";
        if(h<=12){
            half = "a.m"
        }
        else{
            half = "p.m"
            h = h%12;
        }

        var aux = document.createElement("null");
        aux.innerHTML = '<div id="aux" class="test-message"> <p>'+processText(message)+'</p><div class="hour">'+h+':'+m+' '+half+'</div></div>';
        if(popup.children.length < 1 ){
            popup.appendChild(aux);
        
            popup.classList.add('open-popup');
            setTimeout(function(){
                popup.classList.remove('open-popup');
                popup.removeChild(aux);
            }, 3000)
        }
        
    })
    .catch(function (error){
        console.log(error)
    });

}

function processText(text){
    var parts = text.split(" ");
    console.log(parts);
    for (let i = 0; i<parts.length; i++){
        if (parts[i].length > 25){
            let le = parts[i].length;
            let aux = "";
            
            

            for(let j=0; j< le%25; j++){
                aux+= parts[i].substring(j*25,j*25+25) + "\n";
                
            }
            console.log(aux);
            parts[i] = aux;
        }
    }
    return parts.join(" ");
}

function addZero(i) {
    if (i < 10) {i = "0" + i}
    return i;
  }



function enableSend(){
    

    let textarea = document.getElementById('message');
    let btnsend = document.getElementById('send-btn');
    let btncheck = document.getElementById('check-btn');
    console.log("Dx");
    var oraciones = textarea.value.split(" ");
    
    if (textarea.value != ""){
        console.log("a");
        btnsend.classList.add('display-button');
        btncheck.classList.add('display-button');
    }
    else{
        console.log("b");
        btnsend.classList.remove('display-button');
        btncheck.classList.remove('display-button');
        
    }
}

function check(element) {
    var textarea2 = document.getElementById("message"),
      event = new Event('change');
    textarea2.value = element.value;
    textarea2.dispatchEvent(event);
    console.log("aa");
  };


function send_messages(){
    msg = document.getElementById('message').value;
    df = document.getElementById('df').value;

    console.log('aaaa');
    let popup = document.getElementById('popup-windo');
    var aux = document.createElement("null");
    aux.innerHTML = '<div id="loader" class="loader"></div>';
    if(popup.children.length < 1 ){
        popup.appendChild(aux);
    
        popup.classList.add('open-popup');
        
    }
    

    axios.post('/send_messages/', {
        message:msg,
        df: df
    })
    .then(function (response){
        
        popup.classList.remove('open-popup');
        popup.removeChild(aux);
        alert('Mensajes enviados con exito')

    })
    .catch(function (error){
        popup.classList.remove('open-popup');
        popup.removeChild(aux);
    
        alert('Fallo en el envio de mensajes')
        
    }); 
    
}