

var chats_page = 1;
var contacts_page = 1;
var messages_page = 1;
var current_name = ""; 
let phone_number;
let actualcc;
let chat_li = [];
let button_send;
var active_chat; 
let  number_select;
let advise; 
let empresa;
let chat_list = document.getElementById('chat_list');
let chat_box = document.getElementById('chat_box');
let user;
let total_unread = 0;
let options1 = {};
let options2 = {};

function select_empresa(){
   
    empresa = number_select.value;
    if(empresa != ''){
    advise.display = "none";
    add_chats(1);
    start();}
    else{
        chat_list.innerHTML = ' <p id="advise">Seleccione un canal de comunicacion</p>';
        chat_box.innerHTML = "";
        document.getElementById('chat_name').innerHTML = "";
        
    }
}

function  handleChatIntersection(entries, observer){
    entries.forEach( entry => {
        if(entry.isIntersecting){
            console.log(entry.target.innerHTML);
            messages_page += 1;
            showChat(messages_page, actualcc.phone_number);
        }
    });
    
}

function handleContactIntersection(entries, observer) {
    if(entries.length >  10)
    if(entries[entries.length - 5].isIntersecting){
        chats_page += 1;
        add_chats(chats_page);
    }
}

let observer = null;
let contactObserver = null;
let contactloader = document.getElementById('contactloader');


function start(){
    
    ciclo();
}



function ciclo(){
    setInterval(check, 1200);
}


async function contact_lookup(){
    await axios.get('/contact_lookup/',{
        params:{
            'user':user,
            'page': chats_page,
            'project': empresa
        }
    }).then((response) => {
        if(response.status == 200){
            const new_unread = parseInt(response.data['UNREAD_MESSAGES']);
            console.log(response);
            console.log(total_unread, new_unread);
            if(new_unread > total_unread){
                add_chats(1);
                
            }
        }
    }).catch((error) => {
        console.log(error);
    });
}
async function chat_lookup(){
    await axios.get('/chat_lookup/',{
        params:{
            'user':user,
            'page': chats_page,
            'project': empresa,
            'phone_number':actualcc.tel_usuario
        }
    }).then((response) => {
        if(response.status == 200){
            const new_unread = parseInt(response.data['UNREAD_MESSAGES']);
            console.log(total_unread, new_unread);
            if(new_unread > total_unread){
                showChat(1, actualcc.phone_number);
                
            }
        }
    }).catch((error) => {
        console.log(error);
    });
}

function check(){   
    if(actualcc != null){
        chat_lookup();
    }
    contact_lookup();
    ciclo;
}

window.onload = function() {
    user = document.getElementById('user').value;
    number_select = document.getElementById('number-select');
    chat_list = document.getElementById('chat_list');
    chat_box = document.getElementById('chat_box');
    number_select.onchange = select_empresa;
    advise = document.getElementById('advise');
    options1 = {
        root: document.getElementById('chat_box'),
        rootMargin: '500px',
        treshold: 0.1
    };
    options2 = {
        root: document.getElementById('chat_list'),
        rootMargin: '0px',
        treshold: 0.1
    };
    console.log('adding');
    
    let message_input = document.getElementById('message_input');
    
    observer = new IntersectionObserver(handleChatIntersection, options1);
    contactObserver = new IntersectionObserver(handleContactIntersection, options2);

    button_send = document.getElementById('send_button');
    const msg_input = document.getElementById('message_input');

    button_send.innerHTML = '<ion-icon name="mic"></ion-icon>';
    const inio = document.createElement('ion-icon');
    inio.name = 'mic';
    inio.style.fontsize = '1.8em';
    button_send.onclick = (e) => {
        showMessageScreen('Escriba Texto Antes de Enviar');
    };
    msg_input.oninput = send_button_change; 
    msg_input.onchange= send_button_change; 
    message_input.onkeypress = ( (e) =>{
        if(e.key === 'Enter'){
            button_send.click();
        }
    });
    
};

function send_button_change(event){
    var inio = document.createElement('ion-icon');
    
    if(document.getElementById('message_input').value != ""){
        button_send.innerHTML = '';
        inio.name = 'send';
        inio.font
        inio.style.fontSize = '1.4em';
        inio.setAttribute("transform", "rotate(45)");
        button_send.appendChild(inio);
        button_send.onclick = send_message;
    }
    else{
        button_send.innerHTML = '';
        inio.name = 'mic';
        inio.style.fontSize = '1.8em';
        inio.setAttribute("transform", "rotate(45)");
        button_send.appendChild(inio);
        button_send.onclick = (e) => {
            showMessageScreen('Escriba Texto Antes de Enviar');
        };
    }


}

async function send_message(){
    let message_input = document.getElementById('message_input');
    const message = message_input.value;
    console.log(actualcc);
    message_input.value = "";
    button_send.style.enable = "false";
    message_input.enable = "false";
    await axios.post('/send_text_message/', {
        'message':message,
        'from_number': actualcc.tel_empresa,
        'phone_number': actualcc.tel_usuario,
        'user': user
    })
    .then(async (response) => {
            console.log(response.data);
            if(response.status == 200){
                
                body = response.data;
                if(body['status'] == 'ok'){
                    setTimeout(()=> {
                        chat_box.innerHTML = "";
                        showChat(1, actualcc.tel_usuario);
                        chat_li.innerHTML = "";
                        add_chats(1);
                        button_send.style.enable = "true";
                        
                        message_input.enable = "true";
                    },900);
                }
            }
    })
    .catch((error) => {

    });
    
};

async function add_chats(page){
    total_unread = 0;
    console.log(user);
    chat_li = [];
    await axios.get('/chat_list/', {
        params:{
            'user':user,
            'page': chats_page,
            'project': empresa
        }
    }).then(function (response){
        console.log(response.data);
        
        if(response.status == 200){
            const data = response['data'];
            let sw = 1;
            data.forEach(contact => {
                
                let unread = 0;
                if(contact['UNREAD_MESSAGES'] == ''){
                    contact['UNREAD_MESSAGES'] = 0;
                }
                console.log(total_unread, contact['UNREAD_MESSAGES']);
                total_unread = total_unread + parseInt(contact['UNREAD_MESSAGES']);
                let label = "";
                let nombre = "";
                
                
                if(contact['TIPO'] == 'text'){
                    label = contact['CONTENIDO']['body'];
                    if(label == undefined){
                        label = "Plantilla";
                        label = contact['CONTENIDO']['BODY']['text'];
                    }
                    console.log(contact['CONTENIDO']);
                }
                if(contact['TIPO'] == 'document'){
                    label = 'Documento';
                }
                if(contact['TIPO'] == 'image'){
                    label = 'Imagen';
                }
                if(contact['PROFILE_NAME'] == ''){
                    nombre = contact['ORIGEN'];
                }
                if(contact['PROFILE_NAME'] != ''){
                    nombre = contact['PROFILE_NAME'];
                }
                
                
                let cc  = new ContactChat(label, contact['TIEMPO'], contact['CONVERSATION_ID'], contact['FECHA'], 
                    nombre, contact['UNREAD_MESSAGES'], contact['ORIGEN'], contact['TEL_EMPRESA'], contact['TEL_USUARIO']);
                    
                chat_li.push(cc);
                if(page == 1 && sw == 1){
                chat_list.innerHTML="";
                sw  = 0;
}
                cc.addContactChat(chat_list);
                cc.getElement().onclick = async function(){
                    actualcc = cc;
                    messages_page = 1;
                    chat_box.innerHTML = "";
                    console.log('\n\n\n\n');
                    console.log('Click para', contact['PROFILE_NAME']);
                    document.getElementById('chat_name').innerHTML = "<h4>"+ nombre+ "</h4>";
                    current_name = contact['PROFILE_NAME'];
                    
                    showChat(messages_page, contact['ORIGEN']);
                    
                    chat_list.childNodes.forEach(chat => {
                        chat.classList.remove('active');
                    });
                    
                    cc.contact_chat.classList.add('active');
                    console.log('\n\ncontacto:',contact);
                    try{
                        console.log('Removiendo vistos');
                        cc.removeUnread();
                        await axios.get('/update_seen/',{ params:{
                            'phone_number':contact['ORIGEN'],
                            'user':user,
                            'project':empresa
                        }}).then((response) => {
                            if(response.status == 200){
                                console.log('vistos actualizados');
                            }
                        }).catch((error) => {
                            console.log('error actualizando vistos');
                        });
                    
                    }catch(e){
                        console.log(e);
                    }
                    

                };
                contactObserver.observe(cc.getElement());
            });
        }
    })
    .catch(function (error){
      console.log(error);
    });
}

async function showChat(page, phone_number){
    console.log(user);
    let pages;
    let cinput = document.getElementById('chinput');
    cinput.style.display = "";
    console.log('Actualizando visto');
   
    
    await axios.get('/chat_window/', {
        params:{'phone_number':phone_number,
                'page':page,
                'user': user,
                'project':empresa}
    }).then((response) => {
        console.log(response);
        if(response.status == 200){
                
                if(page == 1){
                    let cw = new ChatWindow(user, phone_number);
                    active_chat = cw;
                }

                   
                    
                
                
                let messages = response['data'];
                console.log('recibidos: ', messages);
                
                active_chat.load_messages(messages, chat_box);
                
                
                if(chat_box.children.length > 0){
                    if(chat_box.children.length > 3){
                        observer.observe(chat_box.children[3]);
                    }
                }
            
        }
    }).catch(function(error){
        console.log('problemas cargando la pagina: '+error);
    });
   
    
}





class ChatWindow{
    constructor(name, phone_number){
        this.name = name;
        this.messages = [];
        this.chat_window = null;
        this.phone_number = phone_number;
    }

     addMessage(parent, message_data){
        
        let message = document.createElement('div');
        message.classList.add('message')
        if(message_data['FLOW'] == 'RECIBIDO'){
            
            message.classList.add('friend_msg');
        }
        if(message_data['FLOW'] == 'ENVIADO'){
            message.classList.add('my_msg');
        }
        
        console.log((message_data['CONTENIDO']));
        let content  = document.createElement('p');
        console.log(message_data['CONTENIDO']);
        if(message_data['FLOW'] == 'ENVIADO'){
            let contenido = message_data['CONTENIDO'];

            if(contenido != null && typeof(contenido) != 'string'){
                console.log(typeof(contenido));
                console.log(contenido["components"]);
                contenido['components'].forEach((component) => {
                   
                    if(component != null){
                        const type = component['type'];
                        switch(type){
                            case 'HEADER':
                                if(component['format'] == 'IMAGE'){
                                    let caption = document.createElement('p');
                                    var aux = document.createElement('div');
                                    axios.get('/image_api/', {
                                        params:{
                                                'id':component['display_id']}
                                        }).then(function(response){
                                                if(response.status == 200){
                                                
                                                aux.innerHTML = '<img src="data:'+response['data']['mime_type']+";charset=utf-8;base64,"+response['data']['base64']+'" />';
                                            
                                            }
                                        }).catch(function(error){
                                        console.log(error);
                                    });
                                    content.appendChild(aux);
                                    
                                }
                                if(component['format'] == 'TEXT'){
                                    var aux = document.createElement('p');
                                    aux.innerHTML = component['text'] + '<br>';
                                    content.appendChild(aux);
                                }
                                
                            break;
                            case 'BODY':
                                var aux = document.createElement('p');
                                aux.innerHTML = component['text'] + '<br>';
                                content.appendChild(aux);
                            break;

                            case 'FOOTER':
                                var aux = document.createElement('p');
                                aux.innerHTML = component['text'] + '<br>';
                                content.appendChild(aux);
                            break;

                        }
                    }
                });

            }
            else{
                var aux = document.createElement('p');
                aux.innerHTML = contenido + '<br>';
                content.appendChild(aux);
            }
        }
        else{
            if(message_data['TIPO'] == 'text' || message_data['TIPO'] == 'template'){
                if(message_data['CONTENIDO'] instanceof Object 

                ){
                content.innerHTML = message_data['CONTENIDO']['body'] + '<br>';
                
                }
                
            }

        

            if(message_data['TIPO'] == 'image'){
                
                let caption = document.createElement('p');

                axios.get('/image_api/', {
                    params:{
                            'id':message_data['CONTENIDO']['id']}
                    }).then(function(response){
                            if(response.status == 200){
    
                            content.innerHTML = '<img src="data:'+response['data']['mime_type']+";charset=utf-8;base64,"+response['data']['base64']+'" />';

                        }
                    }).catch(function(error){
                    console.log(error);
                });
                if(message_data['CONTENIDO']['caption'] != undefined){
                    caption.innerHTML  = message_data['CONTENIDO']['caption'] + '<br>';
                    content.appendChild(caption);
                }
            }
        }
        
        let hour = document.createElement('span');

        hour.innerHTML = message_data['TIEMPO'];

        content.appendChild(hour);
        message.appendChild(content);
        

        console.log(message_data['CONTENIDO'], parent.lastChild);
        parent.insertBefore(message, parent.firstChild);
      
    }


    load_messages(messages, parent){
        console.log('Intenado cargar mensajes.');
        this.messages = this.messages.concat(messages);
        let cur_msgs = this.messages.length;
        console.log(this.messages.length);
        if(this.messages.length > 0){
            console.log('Cargando mensajes.');
            console.log(messages);
            let cur_date = new Date(this.messages[0]['FECHA']);
            let today = new Date();
            messages.forEach(element => {
                let f_mensaje = new Date(element['FECHA']);
               
                if(f_mensaje.getDate() <  cur_date.getDate() && f_mensaje.getDate() <  today.getDate()){
                    
                    let cuadro_fecha = document.createElement('div');
                    cuadro_fecha.classList.add('date-box');
                    cuadro_fecha.innerHTML = "<span class='date-text'>"+this.getDate(cur_date)+"</span>";
                    parent.insertBefore(cuadro_fecha, parent.firstChild);
                    cur_date = f_mensaje;
                }
                this.addMessage(parent, element);
            });
            
            if(cur_msgs <= 30){
                parent.scrollTo(0, parent.scrollHeight);
            }
        }
    }
    getId(){
        return this.chat_id;
    }
    getPhoneNumber(){
        return this.phone_number;
    }
    getDate(datetime){
        
        const date = datetime.toLocaleDateString('es-MX', { year: "numeric", month: "numeric", day: "numeric" });
        const today = (new Date()).toLocaleDateString('es-MX', { year: "numeric", month: "numeric", day: "numeric" });
      
        if(date === today){
            return "Hoy";
            return datetime.toLocaleTimeString('es-MX', {hour:'2-digit', minute: '2-digit', hour12:true}).toUpperCase();
        }

        if(date ===
            new Date(new Date().setDate(
                new Date().getDate()-1)).toLocaleTimeString(
                    'es-MX', { year: "numeric", month: "numeric", day: "numeric" })){
            return 'Ayer';
        }

        const tdy = new Date();
        const daysOfWeek = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'];
        if(tdy.getDate() - datetime.getDate()  < 7 &&
            datetime.getMonth() === tdy.getMonth() &&
            datetime.getYear() === tdy.getYear()){
                return daysOfWeek[datetime.getDay()];
            }
        return date;
    }
    
}


class ContactChat{
    constructor(content, sent_hour, chat_id, last_message_time, name, unread_messages, origen, tel_empresa, tel_usuario){
        this.content = content;
        this.sent_hour = sent_hour;
        this.chat_id = chat_id;
        this.name = name;
        this.datetime = new Date(last_message_time + " " + sent_hour);
        this.contact_chat = null;
        this.origen = origen;
        this.tel_empresa = tel_empresa;
        this.tel_usuario = tel_usuario;
        if(unread_messages != ''){
            this.unread_messages = parseInt(unread_messages); 
        }
        else{
            this.unread_messages = 0; 
        }
    }

    getDate(){
        console.log("Last message date ", this.datetime);
        let datetime = this.datetime;
        const date = this.datetime.toLocaleDateString('es-MX', { year: "numeric", month: "numeric", day: "numeric" });
        const today = (new Date()).toLocaleDateString('es-MX', { year: "numeric", month: "numeric", day: "numeric" });
      
        if(date === today){
            return this.datetime.toLocaleTimeString('es-MX', {hour:'2-digit', minute: '2-digit', hour12:true}).toUpperCase();
        }

        if(date ===
            new Date(new Date().setDate(
                new Date().getDate()-1)).toLocaleTimeString(
                    'es-MX', { year: "numeric", month: "numeric", day: "numeric" })){
            return 'Ayer';
        }

        const tdy = new Date();
        const daysOfWeek = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'];
        if(tdy.getDate() - datetime.getDate()  < 7 &&
            datetime.getMonth() === tdy.getMonth() &&
            datetime.getYear() === tdy.getYear()){
                return daysOfWeek[this.datetime.getDay()];
            }
        return date;
    }


    addContactChat(parent) {
        const contact_chat = document.createElement('div');
        contact_chat.classList.add('block');
        if(this.unread_messages > 0 ){
            contact_chat.classList.add('unread')
        }
        const details  = document.createElement('div');
        details.classList.add('details');

        const listHead  = document.createElement('div');
        listHead.classList.add('listHead');
        const lhname = document.createElement('h4');
        lhname.innerHTML = this.name;
        const lhtime = document.createElement('p');
        lhtime.classList.add('time')
        lhtime.innerHTML = this.getDate()

        

        const message_p  = document.createElement('div');
        message_p.classList.add('message_p');

        const message_p_content = document.createElement('p');
        message_p_content.innerHTML = this.content;
        message_p.appendChild(message_p_content);

        if(this.unread_messages != '0'){
            const b = document.createElement('b');
            b.innerHTML = ''+this.unread_messages;
            message_p.appendChild(b);
        }
        
        listHead.appendChild(lhname);
        listHead.appendChild(lhtime);

        details.appendChild(listHead);
        details.appendChild(message_p);
        this.contact_chat = contact_chat;
        
        
        contact_chat.appendChild(details);

        parent.appendChild(contact_chat);

        

    }

    removeUnread(){
        let details = this.contact_chat.getElementsByClassName('details')[0];
        let message_p = details.getElementsByClassName('message_p')[0];
        let b = message_p.getElementsByTagName('b')[0];
        this.unread_messages = 0;
        if(message_p.getElementsByTagName('b').length > 0){
            message_p.removeChild(b);
            this.contact_chat.classList.remove('unread');
        }
    }

    getElement(){
        return this.contact_chat;
    }
}
