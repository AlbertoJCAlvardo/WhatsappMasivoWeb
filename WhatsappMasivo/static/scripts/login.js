var button_ingresar = document.getElementById('btn-ingresar');
document.addEventListener('keypress', function(event){
    if(event.key === "Enter"){
        console.log('Presionaron enter :D');
        validateLogin();
    }
});
document.addEventListener('change', (event) => {
    catchAutocompetion();
});
document.addEventListener('load', (event) => {
    catchAutocompetion();
});
window.onload = (event) =>{
    catchAutocompetion();
}


function catchAutocompetion(){
    const userbox = document.getElementById('user');
    const passwordbox = document.getElementById('password')
    const user = document.getElementById('user').value.toUpperCase();
    const password = document.getElementById('password').value;
   
    if(user != "" ){
        userbox.removeAttribute('placeholder');
        $('#spanuser').hide();
    }
    if(password != "" ){
        passwordbox.removeAttribute('placeholder');
        $('#spanpassword').hide();
    }
}


async function validateLogin(){
    user = document.getElementById('user').value.toUpperCase();
    password = document.getElementById('password').value;
   
    if(user == "" || password == ""){
        showMessageScreen('Sin usuario y/o contraseña');
    }
    else{
       let popup = showLoadingScreen();
        console.log(user, password);
        await axios.post('/login/', {
                    'user':user,
                    'password':password 

            
        }).then(function (response){
            quitLoadingScreen(popup);
            
            
            response = response['data'];
            console.log(response);
            if(response['message'] != 'ok'){
                showMessageScreen(response['message']);
            }
            else{
                console.log(response); 
                
                window.location = '/data_upload?user='+user+'&session_id='+response['session_id'];
                
            }
        })
        .catch(function (error){
            console.log(error);
            quitLoadingScreen(popup);
        });
        
    }

}


$(document).ready(function(){
    
    $(".login-div").find("input, textarea").on("keyup blur focus", function (e) {
        
        var $this = $(this);
        label = $this.prev("span");
          console.log(label);
          if($this.attr('id') == "password"){
            if ($this.val() !== '') {
                
                
                $('#spanpassword').hide();
                
              } else {
                $('#spanpassword').show();
                
              }
            
          } 
          if($this.attr('id') == "user"){
            if ($this.val() !== '') {
                
                $('#spanuser').hide();
                
              } else {
                $('#spanuser').show();
              }
            
          } 

          
       
    });

    
});
