$(document).ready(function() {

  // Hide "Add A Comment" button on page load
  $(".add-a-comment").hide()

  // Move form on reply button click
  $(".reply-btn").click(function() {
      var id = this.id
      $(`.reply-container-${id}`).append($(".add_comment_form"))
      $(".add_comment_form").find('form').attr("action", `/${id}/`)
      $(".add-a-comment").show()
  });

  // Move form to its original place on "Add A Comment" button click and hide it
  $(".add-a-comment").click(function() {
      var id = this.id
      $(`.reply-container-${id}`).append($(".add_comment_form"))
      $(".add_comment_form").find('form').attr("action", `/${id}/`)
      $(".add-a-comment").hide()
  })
});
