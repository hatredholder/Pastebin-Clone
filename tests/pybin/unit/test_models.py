import pybin.models as models


# Paste model


def test_paste_model_str_method(create_test_user):
    """
    GIVEN a test user
    WHEN a Paste model gets created with test user as author
    THEN check if string conversion of created model is equal to expected result
    """
    paste_short_content = models.Paste.objects.create(
        content="short content",
        author=create_test_user,
    )
    paste_long_content = models.Paste.objects.create(
        content="long content long content long content long content long content long content",
        author=create_test_user,
    )

    assert str(paste_short_content) == f"<Paste {create_test_user} - short content>"
    assert (
        str(paste_long_content)
        == f"<Paste {create_test_user} - long content long content long content long conten..>"
    )


# Comment model


def test_comment_model_clean_method(create_test_comment):
    """
    GIVEN a Comment object
    WHEN a Comment object gets created clean method is called and size gets set
    THEN check if size value is set
    """
    assert create_test_comment.size


def test_comment_model_str_method(create_test_user):
    """
    GIVEN a test user
    WHEN a Comment model gets created with test user as author
    THEN check if string conversion of created model is equal to expected result
    """
    comment_short_content = models.Comment.objects.create(
        content="short content",
        author=create_test_user,
    )
    comment_long_content = models.Comment.objects.create(
        content="long content long content long content long content long content long content",
        author=create_test_user,
    )

    assert str(comment_short_content) == f"<Comment {create_test_user} - short content>"
    assert (
        str(comment_long_content)
        == f"<Comment {create_test_user} - long content long content long content long conten..>"
    )


# Reply model


def test_reply_model_str_method(create_test_user, create_test_message):
    """
    GIVEN a test user and a test message object
    WHEN a Reply model is added to test message with test user as author
    THEN check if string conversion of added model is equal to expected result
    """
    reply_short_content = models.Reply(
        content="short content",
        author=create_test_user,
    )
    reply_long_content = models.Reply(
        content="long content long content long content long content long content long content",
        author=create_test_user,
    )

    create_test_message.replies.append(reply_short_content)
    create_test_message.replies.append(reply_long_content)
    create_test_message.save()

    assert str(reply_short_content) == f"<Reply {create_test_user} - short content>"
    assert (
        str(reply_long_content)
        == f"<Reply {create_test_user} - long content long content long content long conten..>"
    )


# Message model


def test_message_model_get_last_reply_creation_date_method(create_test_message, create_test_reply):
    """
    GIVEN a test user and a test reply object
    WHEN a Message model is created with test user as author
    THEN check if string conversion of created model is equal to expected result
    """
    assert create_test_message.get_last_reply_creation_date() == create_test_message.created

    create_test_message.replies.append(create_test_reply)
    create_test_message.save()

    assert create_test_message.get_last_reply_creation_date() != create_test_message.created


def test_message_model_str_method(create_test_user):
    """
    GIVEN a test user
    WHEN a Message model is created with test user as author
    THEN check if string conversion of created model is equal to expected result
    """
    message_short_content = models.Message.objects.create(
        content="short content",
        author=create_test_user,
        receiver=create_test_user,
    )
    message_long_content = models.Message.objects.create(
        content="long content long content long content long content long content long content",
        author=create_test_user,
        receiver=create_test_user,
    )

    assert str(message_short_content) == f"<Message {create_test_user} - short content>"
    assert (
        str(message_long_content)
        == f"<Message {create_test_user} - long content long content long content long conten..>"
    )
