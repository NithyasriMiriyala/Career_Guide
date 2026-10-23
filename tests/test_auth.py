from backend import auth, database


def fresh():
    database.reset_memory_store()


def status_of(fn, *args):
    try:
        fn(*args)
    except auth.AuthError as e:
        return e.status
    return None


def test_hash_is_salted_and_verifies():
    s1, h1 = auth.hash_password("correct horse")
    s2, h2 = auth.hash_password("correct horse")
    assert s1 != s2 and h1 != h2
    assert auth.verify_password("correct horse", s1, h1)
    assert not auth.verify_password("wrong", s1, h1)


def test_register_then_login_returns_same_random_uid():
    fresh()
    uid = auth.register("Student@Example.com", "password123")
    assert len(uid) == 16 and uid != auth.email_key("student@example.com")
    assert auth.login("student@example.com", "password123") == uid


def test_password_is_never_stored_in_plain_text():
    fresh()
    auth.register("a@b.co", "supersecret1")
    doc = database.get_doc("users", auth.email_key("a@b.co"))
    assert "supersecret1" not in str(doc)


def test_old_data_is_kept_for_existing_email():
    fresh()
    key = auth.email_key("old@user.in")
    database.save_doc("profiles", key, {"name": "Old"})
    assert auth.register("old@user.in", "password123") == key


def test_duplicate_register_is_rejected():
    fresh()
    auth.register("dup@x.io", "password123")
    assert status_of(auth.register, "dup@x.io", "password123") == 409


def test_wrong_password_and_unknown_email_look_the_same():
    fresh()
    auth.register("me@x.io", "password123")
    assert status_of(auth.login, "me@x.io", "nope-nope") == 401
    assert status_of(auth.login, "ghost@x.io", "password123") == 401


def test_bad_input_is_rejected():
    fresh()
    assert status_of(auth.register, "not-an-email", "password123") == 400
    assert status_of(auth.register, "ok@x.io", "short") == 400


def test_lockout_after_five_wrong_attempts():
    fresh()
    auth.register("lock@x.io", "password123")
    for _ in range(auth.MAX_FAILS):
        assert status_of(auth.login, "lock@x.io", "wrong-pass") == 401
    assert status_of(auth.login, "lock@x.io", "password123") == 429