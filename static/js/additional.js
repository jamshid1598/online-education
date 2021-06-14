if (window.performance) {
    console.info("window.performance works fine on this browser");
    downloadCounter();
  }
  console.info(performance.navigation.type);
  if (performance.navigation.type == performance.navigation.TYPE_RELOAD) {
    console.info( "This page is reloaded" );
    downloadCounter();
  } else {
    console.info( "This page is not reloaded");
  }

  
  function downloadCounter(){
      console.log('Download Counter Method')
      var lang = document.getElementById('language_type').value;
      var url = '/' + lang.toString() + '/ajax/downloads/'
  
      fetch(url, {
          method:'POST',
          headers:{
              'Content-Type':'application/json',
              'Accept': 'application/json',
              'X-CSRFToken':csrftoken,
          },
      })
      .then((response) => {
         return response.json();
      })
      .then((data) => {
          var d_count = document.getElementById('Download_counted');
      
          console.log(data["instance"])
          d_count.innerHTML = data["instance"];
      });
  }
  

  function like_unlike($this){
    var slug = $this.dataset.slug
    
    console.log('slug:', slug)
  
  
    if (user == 'AnonymousUser'){
      console.log("User is not logged in")
      alert('You are not allowed for this action, please login/sign-up')
    }else{
      console.log("User is logged in")
      like_unlike_method(slug)
      }
      // download_counter(slug)	
  }
  
  
  function like_unlike_method(slug){
    console.log('User is authenticated, sending data...')
    var lang = document.getElementById('language_type').value;
    var url = '/' + lang.toString() + '/ajax/like/lesson/'
    // var url = '/ajax/like/lesson/'
  
    fetch(url, {
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'Accept': 'application/json',
        'X-CSRFToken':csrftoken,
      }, 
      body:JSON.stringify({'slug':slug})
    })
    .then((response) => {
       return response.json();
    })
    .then((data) => {
      console.log(data['success'])
      window.location.reload(); 
    });
  }
 