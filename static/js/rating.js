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
          
          // if like button is pressed
          if (data_rating == 1) {

            // if button is already green
            if ($(this).hasClass("btn-success")){
              $(this).addClass("btn-outline-secondary")
              $(this).removeClass("btn-success")
              $(this).children()[1]["innerText"] = parseInt($(this).children()[1]["innerText"]) - 1

            // if not already green
            } else {
              $(this).removeClass("btn-outline-secondary")
              $(this).addClass("btn-success")
              $(this).children()[1]["innerText"] = parseInt($(this).children()[1]["innerText"]) + 1
            }

          }

          // if dislike button is pressed
          if (data_rating == -1) {

            // if button is already red
            if ($(this).hasClass("btn-danger")){
              $(this).addClass("btn-outline-secondary")
              $(this).removeClass("btn-danger")
              $(this).children()[1]["innerText"] = parseInt($(this).children()[1]["innerText"]) - 1

            // if not already red
            } else {
              $(this).removeClass("btn-outline-secondary")
              $(this).addClass("btn-danger")
              $(this).children()[1]["innerText"] = parseInt($(this).children()[1]["innerText"]) + 1
            }

          }
          console.log(response["key"])
          console.log(response["rating"])
          console.log(response["likes"])
          console.log(response["dislikes"])
        }
    })
  });
