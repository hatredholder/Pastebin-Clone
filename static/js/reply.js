$(document).ready(function() {

  // Hide "Add A Comment" button on page load
  $(".add-a-comment").hide()

  // Move CommentForm on reply button click
  $(".reply-btn").click(function() {
      var id = this.id
      $(`.reply-form-container-${id}`).append($(".add_comment_form"))
      $(".add_comment_form").find('form').attr("action", `/${id}/`)
      $(".add-a-comment").show()
  });

  // Move CommentForm to its original place on "Add A Comment" button click and hide the button
  $(".add-a-comment").click(function() {
      var id = this.id
      $(`.reply-form-container-${id}`).append($(".add_comment_form"))
      $(".add_comment_form").find('form').attr("action", `/${id}/`)
      $(".add-a-comment").hide()
  })
});
