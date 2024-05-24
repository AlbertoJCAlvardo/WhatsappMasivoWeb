

var chats_page = 1;
var contacts_page = 1;
var messages_page = 1;
var current_name = ""; 
let chat_li = [];
var active_chat; 

let chat_list = document.getElementById('chat_list');
let chat_box = document.getElementById('chat_box');
let user;

let options1 = {};
let options2 = {};

function  handleChatIntersection(entries, observer){
    entries.forEach( entry => {
        if(entry.isIntersecting){
            console.log(entry.target.innerHTML);
            messages_page += 1;
            showChat(messages_page, active_chat.getId());
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
    setInterval(check, 30000);
}

function check(){   
    let d = new Date();
    console.log(d.toTimeString());
    for(var i = 1; i<= contacts_page; i++){
        add_chats(i);
    }
    ciclo;
}

window.onload = function() {
    user = document.getElementById('user').value;
    
    chat_list = document.getElementById('chat_list');
    chat_box = document.getElementById('chat_box');

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
    add_chats(1);
    start();

    observer = new IntersectionObserver(handleChatIntersection, options1);
    contactObserver = new IntersectionObserver(handleContactIntersection, options2);
    
};

async function add_chats(page){
    
    
    chat_li = [];
    await axios.get('/chat_list/', {
        params:{
            user:user,
            page: chats_page
        }
    }).then(function (response){
      
        if(response.status == 200){
            const data = response['data'];
            let sw = 1;
            data.forEach(contact => {
                
                console.log(contact);
                let label = "";
                let nombre = "";
                if(contact['TIPO'] == 'text'){
                    label = contact['CONTENIDO']['body'];
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
                                            nombre, contact['UNREAD_MESSAGES']);
                                            
                chat_li.push(cc);
                if(page == 1 && sw == 1){
                    chat_list.innerHTML="";
                    sw  = 0;
                }
                cc.addContactChat(chat_list);
                cc.getElement().onclick = function(){

                    document.getElementById('chat_name').innerHTML = "<h4>"+ nombre+ "</h4>";
                    current_name = contact['PROFILE_NAME'];
                    showChat(messages_page, contact['CONVERSATION_ID']);
                    chat_list.childNodes.forEach(chat => {
                        chat.classList.remove('active');
                    });
                    cc.contact_chat.classList.add('active');
                    
                    
                    axios.get('/update_seen/', {
                        params:{
                            'chat_id':contact['CONVERSATION_ID']
                        }
                    }).then( (response) => {
                        cc.removeUnread();
                    }).catch((error) => {
                        console.log(error);
                    });

                };
                contactObserver.observe(cc.getElement());
            });
        }
    })
    .catch(function (error){
      console.log(error);
    });
}

async function showChat(page, chat_id){
    let pages;
   
    await axios.get('/message_pages/', {
        params:{'chat_id': chat_id}
    }).then(function(response){
        if(response.status == 200){

            pages = response['data']['paginas'];
            console.log(response['data']);
            if(page <= pages + 1){


                
                axios.get('/chat_window/', {
                    params:{'chat_id':chat_id,
                            'page':page}
                }).then(function(response){
        
                    if(response.status == 200){
                        let cw = new ChatWindow(user, chat_id);
                        let messages = response['data'];
                        console.log(messages);
                        if(page == 1){
                            chat_box.innerHTML = "";
                            active_chat = cw;
                            
                        }
                        
                        cw.load_messages(messages, chat_box);
                        
                        
                        if(chat_box.children.length > 0){
                            if(chat_box.children.length > 3){
                                observer.observe(chat_box.children[3]);
                            }
                        }
                    }
                    
                }).catch(function(error){
                    console.log(error);
                });
            }
            console.log(page, pages);
        }
    })

   
   
    
}





class ChatWindow{
    constructor(name, chat_id){
        this.name = name;
        this.messages = [];
        this.chat_window = null;
        this.chat_id = chat_id;
    }

    async addMessage(parent, message_data){
        let message = document.createElement('div');
        message.classList.add('message')
        if(message_data['FLOW'] == 'RECIBIDO'){
            
            message.classList.add('friend_msg');
        }
        if(message_data['FLOW'] == 'ENVIADO'){
            message.classList.add('my_msg');
        }

        let content  = document.createElement('p');
       
        if(message_data['TIPO'] == 'text' || message_data['TIPO'] == 'template'){
            if(message_data['CONTENIDO'] instanceof Object){
             content.innerHTML = message_data['CONTENIDO']['body'] + '<br>';
            
            }
            else{
                content.innerHTML = message_data['CONTENIDO'] + '<br>';
               
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
        
        let hour = document.createElement('span');

        hour.innerHTML = message_data['TIEMPO'];

        content.appendChild(hour);
        message.appendChild(content);
        

        console.log(message_data['CONTENIDO'], parent.lastChild);
        parent.insertBefore(message, parent.firstChild);
      
    }


    load_messages(messages, parent){
        
        this.messages = this.messages.concat(messages);
        let cur_msgs = this.messages.length;
        
            
        let cur_date = new Date(messages[0]['FECHA']);
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
    getId(){
        return this.chat_id;
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
    constructor(content, sent_hour, chat_id, last_message_time, name, unread_messages){
        this.content = content;
        this.sent_hour = sent_hour;
        this.chat_id = chat_id;
        this.name = name;
        this.datetime = new Date(last_message_time);
        this.contact_chat = null;
        if(unread_messages != ''){
            this.unread_messages = parseInt(unread_messages); 
        }
        else{
            this.unread_messages = 0; 
        }
    }

    getDate(){
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
        if(message_p.getElementsByTagName('b').length > 0){
            message_p.removeChild(b);
            this.contact_chat.classList.remove('unread');
        }
    }

    getElement(){
        return this.contact_chat;
    }
}
