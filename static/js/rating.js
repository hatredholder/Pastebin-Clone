 $(".rating-btn").click(function(e) {
    
    let data_key = $(this).attr("data-key")
    let data_rating = $(this).attr("data-rating")
  
    $.ajax({
        url: '/rating/',
        type: 'POST',
        data: {
            "data_key": data_key,
            "data_rating": data_rating
        },
        success: (response) => {

          // if success == false
          if (!response.success){

            // set rating to 0 so the rest of the code doesnt work
            data_rating = 0

            // send an alert
            $(".errors").html('<div class="alert alert-danger">You can\'t rate your own pastes/comments</div>')
          }
          
          // if LIKE button is pressed
          if (data_rating == 1) {

            // if like button is already pressed
            if ($(this).hasClass("btn-success")){
              $(this).addClass("btn-outline-secondary")
              $(this).removeClass("btn-success")
              $(this).children()[1]["innerText"] = parseInt($(this).children()[1]["innerText"]) - 1

            // if dislike button is already pressed
            } else if($($(this).parent().children()[1]).hasClass("btn-danger")) {
              $($(this).parent().children()[1]).removeClass("btn-danger")
              $($(this).parent().children()[1]).addClass("btn-outline-secondary")
              $($(this).parent().children()[1]).children()[1]["innerText"] = parseInt($(this).parent().children()[1]["innerText"]) - 1

              $(this).removeClass("btn-outline-secondary")
              $(this).addClass("btn-success")
              $(this).children()[1]["innerText"] = parseInt($(this).children()[1]["innerText"]) + 1
            }

            // if nothing is pressed
            else {
              $(this).removeClass("btn-outline-secondary")
              $(this).addClass("btn-success")
              $(this).children()[1]["innerText"] = parseInt($(this).children()[1]["innerText"]) + 1
            }
          }

          // if DISLIKE button is pressed
          if (data_rating == -1) {

            // if dislike button is already pressed
            if ($(this).hasClass("btn-danger")){
              $(this).addClass("btn-outline-secondary")
              $(this).removeClass("btn-danger")
              $(this).children()[1]["innerText"] = parseInt($(this).children()[1]["innerText"]) - 1

            // if like button is already pressed
            } else if($($(this).parent().children()[0]).hasClass("btn-success")) {
              $($(this).parent().children()[0]).removeClass("btn-success")
              $($(this).parent().children()[0]).addClass("btn-outline-secondary")
              $($(this).parent().children()[0]).children()[1]["innerText"] = parseInt($(this).parent().children()[0]["innerText"]) - 1

              $(this).removeClass("btn-outline-secondary")
              $(this).addClass("btn-danger")
              $(this).children()[1]["innerText"] = parseInt($(this).children()[1]["innerText"]) + 1
            }

            // if nothing is pressed
            else {
              $(this).removeClass("btn-outline-secondary")
              $(this).addClass("btn-danger")
              $(this).children()[1]["innerText"] = parseInt($(this).children()[1]["innerText"]) + 1
            }
          }

          // if rating is sent to document the user is on
          if (response["key"] == $(".document_id").text()){
           $(".rating").children()[1]["innerText"] = response["rating"]
          }
        }
    })
  });
