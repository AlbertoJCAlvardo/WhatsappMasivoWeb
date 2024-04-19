
export default class ContactChat{
    constructor(content, sent_hour, chat_id, last_message_time, name, unread_messages){
        this.content = content;
        this.sent_hour = sent_hour;
        this.chat_id = chat_id;
        this.name = name;
        this.datetime = new Date(last_message_time);
        this.contact_chat = null;

    }

    getDate(){
        const date = datetime.toLocaleDateString('es-MX', { year: "numeric", month: "numeric", day: "numeric" });
        const today = (new Date()).toLocaleDateString('es-MX', { year: "numeric", month: "numeric", day: "numeric" });
      
        if(date === today){
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


    addContactChat(parent) {
       
        parent.removeAllCh
        const contact_chat = document.createElement('div');
        contact_chat.classList.add('block');

        if(this.unread_messages > 0){
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
        listHead.classList.add('message_p');

        const message_p_content = document.createElement('h4');
        message_p_content.innerHTML = this.content;
        message_p.appendChild(message_p_content);

        if(this.unread_messages > 0){
            const b = document.createElement('b');
            b.innerHTML = ''+this.unread_messages;
            message_p.appendChild(b);
        }
        
        listHead.appendChild(lhname);
        listHead.appendChild(lhtime);

        details.appendChild(listHead);
        details.appendChild(message_p);
        this.contact_chat = contact_chat;
        

        parent.appendChild(contact_chat);
    }

    getElement(){
        return this.contact_chat;
    }
}
