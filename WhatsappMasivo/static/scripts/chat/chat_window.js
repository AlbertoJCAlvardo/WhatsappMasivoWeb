export default class ChatWindow{
    constructor(name, chat_id){
        this.name = name;
        this.messages = [];
        this.chat_window = null;
        this.chat_id = chat_id;
    }

    addMessage(parent, message_data){
        const message = docuement.createElement('div');
        message.classList.add('message')
        if(message_data['FLOW'] == 'RECIBIDO'){
            message.classList.add('friend_msg');
        }
        if(message_data['flow'] == 'ENVIADO'){
            message.classList.add('my_msg');
        }

        const content  = document.createElement('p');
        content.innerHTML = '::before '+message_data['text'] + '<br>';

        const hour = document.createElement('span');

        hour.innerHTML = message_data['hour'];

        content.appendChild(hour);
        message.appendChild(content);
        parent.appendChild(message);

    }


    load_messages(messages, parent){
        this.messages.concatenate(messages);
        parent.innerHTML = "";

        this.messages.forEach(element => {
            this.addMessage(parent, element);
        });
    }
    getId(){
        return this.chat_id;
    }
    
    
}
