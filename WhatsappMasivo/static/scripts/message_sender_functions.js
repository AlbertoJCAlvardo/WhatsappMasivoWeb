var selected_item;
let button_list = [];

function add_column(){
    let text_area = selected_item;
    console.log(text_area);
    if (text_area != document.getElementById("message-footer")){
        var select = document.getElementById('column-select');
        if (select.options[select.selectedIndex].text != "Datos"){
            
            const selectionEnd = text_area.selectionEnd; 
            const selectionStart = text_area.selectionStart;
            let value = text_area.value;
            let ini  = value.substring(0, selectionStart);
            let fin  = value.substring(selectionEnd, value.length);
            console.log(selectionStart, selectionEnd, value);
            console.log(value.length);
            let chori =  "{" + select.options[select.selectedIndex].text + "}";


            if(selectionEnd < value.length && value[selectionEnd] != ' '){
            chori += " ";
            }
            if(selectionStart > 0 && value[selectionStart] != ' '){
                chori = " "+ chori;
            } 
            
            text_area.value = ini + chori+fin;
            
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
    if(switch_status == 'text'){
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
}

function addZero(i) {
    if (i < 10) {i = "0" + i}
    return i;
  }


  function add_button(){

    let popup = document.getElementById('popup-windo')
    let formcont = document.createElement('div');
    let button_add = document.createElement('button');
    let button_close = document.createElement('button');

    formcont.classList.add('form-cont');
    formcont.classList.add('chat_message');
    formcont.innerHTML = "<input type='text' id='button-text' placeholder='Texto del Botón'/> <br> <input type='text' id='button-link' placeholder='Link del Botón'/>";
    button_add.innerHTML = "Insertar";
    button_close.innerHTML = 'Cancelar';
    formcont.appendChild(button_add);
    formcont.appendChild(button_close);
    button_add.onclick = () => {
        const urlexp = 'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)';
        const url_pattern = RegExp(urlexp);
        const spaces_regex = RegExp('[\t\n\v\f\r \u00a0\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u200b\u2028\u2029\u3000]+');
    
        let button_text = document.getElementById('button-text');
        let button_link = document.getElementById('button-link');
        
        
        
        if(button_text.value != '' && button_link.value != ''){
            let chat_message = document.getElementById('chat_message');
            let visual_btn = document.createElement('div');
            
            visual_btn.classList.add('visual-button');
            visual_btn.innerHTML = "<p>"+button_text.value+"<p/>"
            chat_message.appendChild(visual_btn);
            button_list.push({'text':button_text.value.normalize('NFD').replace(/[\u0300-\u036f]/g,""), 'url':button_link.value, 'type':'URL'});
            
            var delete_button = document.createElement('div');
            delete_button.innerHTML = '<ion-icon name="close-circle"></ion-icon>';
            delete_button.classList.add('delete-button');
            delete_button.onclick = () => {
                visual_btn.removeChild(delete_button);
                chat_message.removeChild(visual_btn);
                console.log(button_list);
                button_list = button_list.filter(element => element['text'] != button_text.value &&  element['url'] != button_link.value);
                console.log(button_list);
                console.log('\n\n');
            }
            visual_btn.onmouseover = () => {
                delete_button.classList.add('show-delete');
            };
            visual_btn.onmouseleave = () => {
                delete_button.classList.remove('show-delete');
            };

            visual_btn.appendChild(delete_button);
            popup.innerHTML = "";
            popup.classList.remove('open-popup');
        }
        else{
            showMessageScreen('Campos invalidos');
        }
    };
    button_close.onclick = () => {
        popup.classList.remove('open-popup');
    };
    popup.classList.add("popup-window");
    popup.appendChild(formcont);
    popup.classList.add('open-popup');
}



function enableSend(){
    let header = false;
    
    if(switch_status == 'text'){
        let m_header = document.getElementById('message-header');
        
        header = m_header.value != "" &&   m_header.value != " ";
    }    
    else{
        header = (up_img != null && switch_status == 'image') || (up_file != null && switch_status == 'file');
    }
    let m_body = document.getElementById('message-body');
    let m_footer = document.getElementById('message-footer');
    let btncheck = document.getElementById('check-btn');
    let btnsend = document.getElementById('send-btn');
    

    
    let body = m_body.value != "" &&   m_body.value != " ";
    let footer = m_footer.value != "" &&   m_footer.value != " " ;
    
   
    
    

    if (header && body && footer){
        btnsend.classList.add('display-button');
        if(switch_status == 'text'){
            btncheck.classList.add('display-button');
        }
    }
    
    else{
        
        btnsend.classList.remove('display-button');
        btncheck.classList.remove('display-button');
        
    }
}


function format_template(){


    let components = [];
    let template_body = {};
    let template_header = {};
    let template_footer = {};
    let template_buttons = null;

    template_header['type'] = 'HEADER';
    template_body['type'] = 'BODY';
    template_footer['type'] = 'FOOTER';

    
    switch(switch_status){
        case 'text':
            template_header['format'] = 'TEXT';
            template_header['text'] = document.getElementById('message-header').value;
            template_header['text'] = template_header['text'].replace('\n',"");

        break;
        case 'image':
            template_header['format'] = 'IMAGE';
          
        break;
        case 'file':
            template_header['format'] = 'DOCUMENT';
            
        break;
    }
    template_body['text'] = document.getElementById('message-body').value;
    template_body['text'] = template_body['text'].replace('\n\n',"\n");
    template_footer['text'] = document.getElementById('message-footer').value;

    if(button_list.length > 0){
        template_buttons = {'type': 'BUTTONS',
                            'buttons': button_list}        
    }

    components = [template_header,
                  template_body,
                  template_footer,
                  template_buttons
                ]
    return components;
}   
async function send_messages(){
    const from_number_text = document.getElementById('number-select').value;
    let from_number_dic = {

    }
    
    const components = format_template();
    let popup = showLoadingScreenMessage('Esperando la autorización de Meta');
        
    
    var status = 0;
    var template_name = "";
    var response = {};
    let file;
    let message_resource_id = null; 
    let file_data = {};
    const column_select = document.getElementById('number-select');
    
    
    switch(switch_status){
        case 'image':
          
            file_data = {
                'data': up_img,
                'name': fileName, 
                'extension': extension
            }
            file = up_img;
        break;
        case 'file':
 
            file_data = {
                'data': up_file,
                'name': fileName, 
                'extension': extension
            }
            file = up_file;
        break;
    }

    var file_switch = 1;

    if(switch_status != 'text'){
        var formData = new FormData();
        formData.append('file', file);
        formData.append('from_number', column_select.value)
        await axios.post('/upload_file/', formData,
            {headers: {'Content-Type':'multipart/form-data'}}
        ).then(async (response) => {
            response = response['data'];
            console.log('Uploaded file')
            console.log(response);
            file_data['permisions'] = response['permisions'];

            if(response['status']  !== 'ok'){
                file_switch = 0;
            } 
            else{
                 await axios.post('/register_template/', 
                    { 
                        message:{'components': components,
                                'type': switch_status,
                                'buttons': button_list.length
                                },
                        df: df,
                        file_data: file_data,
                        from_number: column_select.value,
                        timeout: 50000
                    }, 
                    ).then(async function (response){
                    response = response['data'];
                    
                    status = response['status'];
                    console.log(status);
                    template_name = response['template_name'];
                    display_id = response['display_ids'];
                    if(response['type'] != 'text'){
                        message_resource_id = response['resource_id']; 
                        
                    }
                    if (status !== 200){
                        
                        quitLoadingScreen(popup);
                        if(status !== 400){
                            popup = showLoadingScreenMessage('Fallo en el registro de mensajes<br>\n error: '+processText(response['error']));
                        }
                        else{
                            popup = showLoadingScreenMessage('Fallo en el registro de mensajes');
                        }
                        setTimeout(function(){
                            quitLoadingScreen(popup);
                        }, 5000);
                    }
                    else{
                        setTimeout(async () => {
                            showMessageScreen('Plantilla Registrada');
                        }, 1000);
                        console.log('Enviando Mensajes')
                        console.log('\nFrom number: ', column_select.value);
                        message.innerHTML = '<div class="loading-message">Mensaje autorizado, enviando mensajes</div>';
                        await axios.post('/send_messages/', {
                            df: df,
                            template_name:template_name,
                            message:{'components': components,
                                'type': switch_status,
                                'buttons': button_list.length,
            
                                },
                            user: document.getElementById('user').value,
                            from_number:column_select.value,
                            file_data: file_data
                        })
                        .then(function (response){
                            response = response['data'];
                            console.log(response);
                            popup.removeChild(message);
                            setTimeout(() => {
                                showMessageScreen('Mensajes enviados!<br>Total:'+response.message_count);
            
                            }, 5000);                
                            if(response.status !== 200){
                                quitLoadingScreen(popup);
                                popup = showLoadingScreenMessage('loading-message">Fallo enviando los mensajes'+response.error)
                                message.innerHTML = '<div class="loading-message">Fallo enviando los mensajes'+response.error+'</div>';
                            }
                            popup.appendChild(message)
                            
                            quitLoadingScreen(popup);
                           
                        })
                        .catch(function (error){
                            quitLoadingScreen(popup);
                                popup = showLoadingScreenMessage('loading-message">Fallo enviando los mensajes'+error);
                                quitLoadingScreen(popup);
                        }); 
                    }
                    
                
                })
                .catch(function (error){
                setTimeout(function(){
                        quitLoadingScreen(popup);
                        }, 5000)
                });
            }
        }).catch((error)=>{
            console.log(error);
            file_switch = 0;
        })
    }
    else{
        console.log('Registrando el template');
        await axios.post('/register_template/', 
            { 
                message:{'components': components,
                        'type': switch_status,
                        'buttons': button_list.length
                        },
                df: df,
                file_data: file_data,
                from_number: column_select.value
            }
            ).then(async function (response){
            response = response['data'];
            
            status = response['status'];
            console.log(status);
            template_name = response['template_name'];
            display_id = response['display_ids']
            if(response['type'] != 'text'){
                message_resource_id = response['resource_id']; 
                
            }
            if (status !== 200){
                
                quitLoadingScreen(popup);
                if(status !== 400){
                    popup = showLoadingScreenMessage('Fallo en el registro de mensajes<br>\n error: '+processText(response['error']));
                }
                else{
                    popup = showLoadingScreenMessage('Fallo en el registro de mensajes');
                }
                setTimeout(function(){
                    quitLoadingScreen(popup);
                }, 5000);
            }
            else{
                console.log('Enviando Mensajes')
                console.log('\nFrom number: ', column_select.value);
                message.innerHTML = '<div class="loading-message">Mensaje autorizado, enviando mensajes</div>';
                await axios.post('/send_messages/', {
                    df: df,
                    template_name:template_name,
                    message:{'components': components,
                        'type': switch_status,
                        'buttons': button_list.length,
    
                        },
                    user: document.getElementById('user').value,
                    from_number:column_select.value,
                    file_data: file_data
                })
                .then(function (response){
                    response = response['data'];
                    console.log(response);
                    popup.removeChild(message);
                    setTimeout(() => {
                        showMessageScreen('Mensajes enviados!<br>Total:'+response.message_count);
    
                    }, 3000);                
                    if(response.status !== 200){
                        quitLoadingScreen(popup);
                        popup = showLoadingScreenMessage('loading-message">Fallo enviando los mensajes'+response.error)
                        message.innerHTML = '<div class="loading-message">Fallo enviando los mensajes'+response.error+'</div>';
                    }
                    popup.appendChild(message)
                    setTimeout(function(){
                        quitLoadingScreen(popup);
                    }, 3000);
            
                })
                .catch(function (error){
                    quitLoadingScreen(popup);
                        popup = showLoadingScreenMessage('loading-message">Fallo enviando los mensajes'+error);
                        quitLoadingScreen(popup);
                }); 
            }
            
        
        })
        .catch(function (error){
        setTimeout(function(){
                quitLoadingScreen(popup);
                }, 5000)
        });
       
    }
    

   
   
    
    
}

function change_active(){
    if(document.activeElement == document.getElementById("message-header") || 
        document.activeElement == document.getElementById("message-body")){
        selected_item = document.activeElement;
       
    }
}



let switch_button = document.getElementById('header-switch');
let switch_status = "text";
let img_pos = 0;
let message_header_cont;
let img_button;
let file_button;
let up_img;
let up_file;
let outputfile;
let extension;
let fileName;

function getFileNameWithExt(event) {

    if (!event || !event.target || !event.target.files || event.target.files.length === 0) {
      return;
    }
    const name = event.target.files[0].name;
    const lastDot = name.lastIndexOf('.');
    fileName = name.substring(0, lastDot);
    const ext = name.substring(lastDot + 1);
    outputfile = fileName;
    extension = ext;
    
}

window.onload = function(){
    up_file = null;
    up_img = null;
    message_header_cont = document.getElementById('message-header-cont');
    df = document.getElementById('df').value;
    img_button = document.getElementById('img-button');

    file_button = document.getElementById('file-button');
    switch_button = document.getElementById('header-switch');
    file_button.addEventListener("change", getFileNameWithExt(event));
    img = switch_button.children[1];
    img.onmouseover = () => {
        show_button_description("Cambiar a Imagen");
    };
    img.onmouseout = () => {
        hide_button_description();
    };
    switch_button.onclick = function(){
        switch_btn();
    };
    switch_status = "text";
    img_pos = 0;
}

var uploaded_image = "";

function switch_btn(){
    var apagador = 0;
    img_pos = (img_pos + 1) % 3;
    if(switch_status == "text"  && apagador == 0){
        switch_status = "image";
        message_header_cont.classList.add('centered-content');
        message_header_cont.innerHTML = "";
       
        switch_button.removeChild(switch_button.lastElementChild);
        let img =  document.createElement('img');        
        img.src = img_arr[img_pos];
        img.onmouseover = () => {
            show_button_description("Cambiar a Documento");
        };
        img.onmouseout = () => {
            hide_button_description();
        };
        switch_button.appendChild(img);

        let btn = document.createElement('button');
        btn.innerHTML = "Añadir Imagen"; 

        img_button.onchange = event => {
           
            console.log('aaaa');
            let hdr_img = document.createElement('img');
            
            let  file = event.target.files[0];
            if(file){
                up_img = file;
                const name = file.name;
                const lastDot = name.lastIndexOf('.');
                fileName = name.substring(0, lastDot);
                const ext = name.substring(lastDot + 1);
                outputfile = fileName;
                extension = ext;
                
                let file_info = document.createElement('div');
                file_info.classList.add('uploaded-image');
                message_header_cont.innerHTML = ""; 
                hdr_img.src = URL.createObjectURL(file);
                file_info.appendChild(hdr_img);
                message_header_cont.appendChild(file_info);

            }
        };
        btn.addEventListener("click", () => {
            img_button.click();
        });
        message_header_cont.appendChild(btn);
         
        apagador = 1;
        

    }
    if(switch_status == "image" && apagador == 0){
        message_header_cont.classList = []
        switch_status = "file";
        
        switch_button.removeChild(switch_button.lastElementChild);
        let img =  document.createElement('img');
        img.src = img_arr[img_pos];
        
        img.onmouseover = () => {
            show_button_description( "Cambiar a texto");
        };
        img.onmouseout = () => {
            hide_button_description();
        };
        message_header_cont.classList.add('centered-content');
        switch_button.appendChild(img);
        message_header_cont.innerHTML = "";
        let btn = document.createElement('button');
        btn.innerHTML = "Añadir Documento"; 
        
        file_button.onchange = event => {
           
        
            let hdr_iframe = document.createElement('iframe');
            const  file = event.target.files[0];
            if(file){
                const name = file.name;
                const lastDot = name.lastIndexOf('.');
                fileName = name.substring(0, lastDot);
                const ext = name.substring(lastDot + 1);
                up_file = file;
               getFileNameWithExt(event);
                message_header_cont.innerHTML = ""; 
                /*
                if(extension == "pdf"){
                    let file_info = document.createElement('div');
                    file_info.classList.add('uploaded-file-box');
                    file_info.classList.add('centered-content');
                    hdr_iframe.src = URL.createObjectURL(file);
                    file_info.appendChild(hdr_iframe);
                    let p = document.createElement('p');
                    p.innerHTML = outputfile+'.'+extension;
                    file_info.appendChild(p);
                    message_header_cont.classList.add('centered-content');
                    message_header_cont.appendChild(hdr_iframe);
                }
                */
                if(extension == "csv" || extension == "xlsx"){
                    let file_info = document.createElement('div');
                    file_info.classList.add('uploaded-file-box');
                    
                    let auximg = document.createElement('img');
                    auximg.src = csv_img;
                    file_info.appendChild(auximg);
                    let p = document.createElement('p');
                    p.innerHTML = outputfile+'.'+extension;
                    file_info.appendChild(p);
                    message_header_cont.classList.add('centered-content');
                    message_header_cont.appendChild(file_info);
                }
                else{
                    let file_info = document.createElement('div');
                    file_info.classList.add('uploaded-file-box');
               
                    let auximg = document.createElement('img');
                    auximg.src = file_img;
                    file_info.appendChild(auximg);
                    let p = document.createElement('p');
                    p.innerHTML = outputfile+'.'+extension;
                    file_info.appendChild(p);
                    message_header_cont.classList.add('centered-content');
                    message_header_cont.appendChild(file_info);
                }
            }
        };
        btn.addEventListener("click", () => {
            
            file_button.click();
        });
        message_header_cont.appendChild(btn);
        
        apagador = 1;
        
    }

    if(switch_status == "file" && apagador == 0){
        message_header_cont.classList = []
        switch_status = "text";
        switch_button.removeChild(switch_button.lastElementChild);
        let img =  document.createElement('img');
        
        img.onmouseover = () => {
            show_button_description("Cambiar a imagen");
        };
        img.onmouseout = () => {
            hide_button_description();
        };
        img.src = img_arr[img_pos];
        switch_button.appendChild(img);
        message_header_cont.innerHTML = '<textarea placeholder="Encabezado" id="message-header" maxlength="25" onchange="enableSend()" oninput="enableSend()" onmouseup="change_active()" ></textarea>';
       
        apagador = 1;
    }
    if(document.getElementById('message-body').value != '' && document.getElementById('message-footer').value != ''){
        let cbutton = document.getElementById('check-btn');
        if(switch_status != 'text'){
            cbutton.style.display = 'none';
        }
        else{
            cbutton.style.display = '';
        }
    }
    
}

function show_button_description(text){
    let img_desc = document.getElementById('sw-description');
    img_desc.innerHTML = text;
    img_desc.style.display = '';
}
function hide_button_description(){
    let img_desc = document.getElementById('sw-description');
    img_desc.style.display = 'none';
}