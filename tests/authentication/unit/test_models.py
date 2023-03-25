def test_user_model_str_method(create_test_user):
    """
    GIVEN a User model
    WHEN a User model is created
    THEN check if string conversion of create_test_user
    is equal to expected result
    """
    assert str(create_test_user) == "<User new_user>"


def test_user_model_clean_method(db, create_test_user):
    """
    GIVEN a User model
    WHEN a User model is created
    THEN check if User model contains avatar
    """
    assert create_test_user.avatar


def test_user_model_get_total_rating_method_is_zero(db, create_test_user):
    """
    GIVEN a User model
    WHEN get_total_rating method is called
    THEN check if method returns 0
    """
    assert create_test_user.get_total_rating() == 0


def test_user_model_get_total_rating_method_with_rated_paste(db, create_test_user):
    """
    GIVEN a User model and Paste(author=create_test_user, rating=1) model
    WHEN get_total_rating method is called
    THEN check if method returns 1
    """
    # TODO: Write this test after implementing create_paste_with_rating fixture


def test_user_model_get_total_rating_method_with_rated_comment(db, create_test_user):
    """
    GIVEN a User model and Comment(author=create_test_user, rating=1) model
    WHEN get_total_rating method is called
    THEN check if method returns 1
    """
    # TODO: Write this test after implementing create_comment_with_rating fixture
