var selected_item;


function add_column(){
    let text_area = selected_item;
    console.log(text_area);
    if (text_area != document.getElementById("message-footer")){
        var select = document.getElementById('column-select');
        if (select.options[select.selectedIndex].text != "Datos"){
            text_area.value = text_area.value + "{" + select.options[select.selectedIndex].text + "} ";
        }
        else{
            alert("Seleccione una columna")
        }
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

async function check_message(){

    hdr = document.getElementById('message-header').value;
    bdy = document.getElementById('message-body').value;
    ftr = document.getElementById('message-footer').value;

    df = document.getElementById('test').value;
    var flag = 0;
    await axios.post('/check_message/', {
        
        message:bdy,
        test: df
    })
    .then(function (response){
        body = response.data['message'];
        flag = flag + 1;
    })
    .catch(function (error){
        
        console.log(error)
    });
    await axios.post('/check_message/', {
        
        message:hdr,
        test: df
    })
    .then(function (response){
        header = response.data['message'];

        flag += 1;
    })
    .catch(function (error){
        
        console.log(error)
    });
    
    console.log(flag);
    if(flag == 2){
        popup = document.getElementById('popup-windo')
        
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
        aux.innerHTML = '<div id="aux" class="test-message">'+
                        '<div class="msg-content">'+
                        '<div class="msg-header" >'+ processText(header)+'</div>'+
                        '<div class="msg-body">'+ processText(body)+'</div>'+
                        '<div class="msg-footer">'+ processText(ftr)+'</div></div></div>';
        if(popup.children.length < 1 ){
            popup.appendChild(aux);
        
            popup.classList.add('open-popup');
            setTimeout(function(){
                popup.classList.remove('open-popup');
                popup.removeChild(aux);
            }, 3000)
        }
    }


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
    
    let m_header = document.getElementById('message-header');
    let m_body = document.getElementById('message-body');
    let m_footer = document.getElementById('message-footer');

    let btnsend = document.getElementById('send-btn');
    let btncheck = document.getElementById('check-btn');

    let header = m_header.value != "" &&   m_header.value != " ";
    let body = m_body.value != "" &&   m_body.value != " ";
    let footer = m_footer.value != "" &&   m_footer.value != " " ;
    
   
    
    

    if (header && body && footer){
        btnsend.classList.add('display-button');
        btncheck.classList.add('display-button');
    }
    else{
        
        btnsend.classList.remove('display-button');
        btncheck.classList.remove('display-button');
        
    }
}

async function send_messages(){
    
    bdy = document.getElementById('message-body').value;
    hdr = document.getElementById('message-header').value;
    ftr = document.getElementById('message-footer').value;
    msg = hdr + '\n' +  bdy + '\n' + ftr;
    
    df = document.getElementById('df').value;

    
    let popup = document.getElementById('popup-windo');
    var aux = document.createElement("null");
    var message = document.createElement('null');

    aux.innerHTML = '<div id="loader" class="loader"></div>';
    message.innerHTML = '<div class="loading-message">Esperando autorizacion de Meta...</div>';
    
    
    popup.appendChild(aux);
    popup.appendChild(message)
    popup.classList.add('open-popup');
        
    
    var status = 0;
    var template_name = "";
    var response = {};
    await axios.post('/register_template/', {
        message:{'header':hdr,
                 'body':bdy,
                 'footer':ftr
                },
        df: df
    }).then(function (response){
        response = response['data'];
        console.log(response);
        status = response['status'];

        template_name = response['template_name'];
        if (status !== 200){
            
            popup.removeChild(message);
            message.innerHTML = '<div class="loading-message">Fallo en el registro de mensajes<br>\n error: Mensaje Rechazado por Meta</div>';
            if(status !== 400){
                
                message.innerHTML = '<div class="loading-message">Fallo en el registro de mensajes<br>\n error: '+processText(response['error'])+'</div>'; 
            }
            popup.appendChild(message)
            setTimeout(function(){
                popup.removeChild(aux);
                popup.removeChild(message);
                popup.classList.remove('open-popup');
                
            }, 5000)
            
        }
    })
    .catch(function (error){
       setTimeout(function(){
                console.log(error);
                popup.classList.remove('open-popup');
                if(popup.contains(aux)){
                    popup.removeChild(aux);
                }
                if(popup.contains(aux)){
                    popup.removeChild(message);
                }
            }, 5000)
    });

    if(status == 200){
        console.log('\nPrueba: ', response);
        message.innerHTML = '<div class="loading-message">Mensaje autorizado, enviando mensajes</div>';
        await axios.post('/send_messages/', {
            template_name:template_name,
            df: df,
            message:msg,
            message_dic:{'header':hdr,
                         'body':bdy,
                         'footer':ftr
                        },
            user: document.getElementById('user').value
        })
        .then(function (response){
        
            response = response['data'];
            console.log(response);
            popup.removeChild(message);
            message.innerHTML = '<div class="loading-message">Mensajes enviados!<br>Total:'+response.message_count+'</div>';
            if(response.status !== 200){
                message.innerHTML = '<div class="loading-message">Fallo enviando los mensajes'+response.error+'</div>';
            }
            popup.appendChild(message)
            setTimeout(function(){
                popup.classList.remove('open-popup');
                popup.removeChild(aux);
                popup.removeChild(message);
            }, 3000);
    
        })
        .catch(function (error){
            
        }); 
    }
   
    
    
}

function change_active(){
    if(document.activeElement == document.getElementById("message-header") || 
        document.activeElement == document.getElementById("message-body")){
        selected_item = document.activeElement;
       
    }
}
