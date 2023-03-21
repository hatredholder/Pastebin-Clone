 $(".captcha-reload").click(function(e) {
    
    $.ajax({
        url: '/site/captcha/reload/',
        type: 'GET',
        success: (response) => {
          // Find the captcha-image, and refresh it
          // (https://stackoverflow.com/questions/1077041/refresh-image-with-a-new-one-at-the-same-url)
          $(document).find(".captcha-image").attr("src", "/site/captcha/?" + new Date().getTime()) 
        }
    })
  });
