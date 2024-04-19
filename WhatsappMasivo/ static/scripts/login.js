async function validateLogin(){
    user = document.getElementById('user').value.toUpperCase();
    password = document.getElementById('password').value;
   
    if(user == "" || password == ""){
        showMessageScreen('Sin usuario y/o contraseña');
    }
    else{
        elements = showLoadingScreen();
        console.log(user, password);
        await axios.post('/login/', {
                    'user':user,
                    'password':password 
                
            
        }).then(function (response){
            quitLoadingScreen(elements[0], elements[1], elements[2]);
            
            
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
            quitLoadingScreen(elements[0], elements[1], elements[2]);
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
